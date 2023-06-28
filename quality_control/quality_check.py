#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:33:49 2020

@author: Frank Foerste
ffoerste@physik.tu-berlin.de
"""

##############################################################################
### import packages ###
##############################################################################
import json
from glob import glob

import matplotlib.pyplot as plt
import numpy as np
from larch import Group, Interpreter, fitting, xafs, xray
from PIL import Image

plt.ioff()
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["xtick.top"] = True
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["ytick.right"] = True
plt.rcParams["axes.grid.which"] = "both"
import base64
import io
import os
from datetime import datetime
from sys import path, platform

##############################################################################
### import custom packages ###
##############################################################################
path.append("/".join(os.path.abspath(os.curdir).split("/")[:-1]))
from plugins.read_data import read_data


##############################################################################
### define quality check and testing feature ###
##############################################################################
class check_quality(object):
    """
    This class implements the automated routines to check the quality criteria
    of XAFS measurements. The evaluation is based on larch
    https://xraypy.github.io/xraylarch/
    """

    def __init__(self, quality_criteria_json, verbose = False):
        
        self.verbose = verbose
        if self.verbose:
            print("+++++++++++++++++++++++++++++++++++++++++")
            print("+ quality criteria function initialized +")
            print("+          verbose mode active          +")
            print("+++++++++++++++++++++++++++++++++++++++++")
        with open(quality_criteria_json, "r") as f:
            self.quality_criteria = json.load(f)
            
    
    def shorten_data(self,):
        '''
        functionality to cut the last index of the data to avoid unwanted behaviour
        in k
        '''
        self.data.energy = self.data.energy[:-1]
        self.data.mu = self.data.mu[:-1]
        self.data.flat = self.data.flat[:-1]
        self.data.pre_edge = self.data.pre_edge[:-1]
        self.data.post_edge = self.data.post_edge[:-1]
        self.data.k = self.data.k[:-1]
        self.data.chi = self.data.chi[:-1]
        
        
    def clip_data(self, data, minimum = -5, maximum = 5):
        '''
        functionality to clip k-data to minimum and maximum to avoid unwanted 
        behaviour in k
        
        Parameters
        ----------
        minimum : float
            minimum value to clip data.k
        maximum : float
            maximum value to clip data.k
        '''
        return np.clip(data, a_min = -5, a_max = 5)


    def load_data(self, measurement_data, source="SYNCHROTRON",
                  mode="ABSORPTION", processed="RAW", 
                  name=None, plot=True,
                  ):
        """
        This function loads the data given by the read_data plugin to process 
        it.

        Parameters
        ----------
        measurement_data : array
            the measurement data, has to be [energy, mu] with same shape
        source : string, optional
            type of the utilized x-Ray source, either SYNCHROTRON or LABORATORY
        mode : string, optional
            mode of measurement, either ABSORPTION or FLUORESCENCE
        processed : string, optional
            data processing status, either RAW or PROCESSED
        plot : boolean, optional
            if True, the data and processing will be plotted
        """
        if name is None:
            self.name = "sample"
        else:
            self.name = name
        ### store the parameters in the class
        self.plot = plot
        self.source = source
        self.mode = mode
        self.processed = processed
        ### read the correct quality criteria correspondend to the sample
        self.quality_criteria_sample = self.quality_criteria[self.source][self.mode][self.processed]
        ### initialize the larch Group to evaluate the data
        self.data = Group()
        ### add energy and absorption to the larch Group
        self.data.energy = measurement_data[0, :]
        self.data.mu = measurement_data[1, :]


    def preprocess_data(self):
        """
        This function preprocesses the data, finds the edge, fits the pre and post
        edge.
        """
        ### find the edge energy E0 of the absorption data
        xafs.find_e0(self.data.energy, self.data.mu, group=self.data)
        ### perform an energy calibration
        ### for this guess the element edge and retrieve the edge energy from
        ### the database of larch mostly based on Elam
        ### https://xraypy.github.io/xraylarch/xray.html
        element_n_edge = xray.guess_edge(self.data.e0)
        edge_E_DB = xray.xray_edge(*element_n_edge)[0]
        self.data.energy -= (self.data.e0 - edge_E_DB)
        # print('difference:', (self.data.e0 - edge_E_DB))
        self.data = Group(mu = self.data.mu, energy = self.data.energy)
        xafs.find_e0(self.data.energy, self.data.mu, group=self.data)
        ### retrieve the array index of E0 to determine low cut energy
        edge_index = np.where(self.data.energy == self.data.e0)[0][0]
        cut_index = edge_index - 150
        ### if the data below edge is not sufficient, set index to 0 to avoid
        ### using data from the end of the array
        if cut_index < 0: cut_index = 0
        if cut_index > edge_index//2: cut_index = (cut_index + edge_index//2) // 2
        ### cut the energy and absorption in the pre-edge region
        self.data.element_n_edge = element_n_edge
        self.data.energy = self.data.energy[cut_index:]
        self.data.mu = self.data.mu[cut_index:]
        ### calculate the edge position
        xafs.pre_edge(energy = self.data.energy,
                      mu = self.data.mu,
                      e0 = self.data.e0,
                      group = self.data,
                      pre1 = -150,
                      pre2 = -30,
                      norm1 = 50,
                      norm2 = 700,
                      make_flat = True,
                      nvict = 3,
                      )
        ### estimate pre and post edge and correct the background
        xafs.autobk(energy=self.data.energy, mu=self.data.mu, group=self.data,
                    rbkg = 1.0,
                    clamp_lo = 10,
                    clamp_hi = 1,
                    dk = 1.,
                    kweight = 2,
                    win = 'hanning',
                    )
        ### calculate k**2*chi to determine the k-range for Fourier R transformation
        data = self.data.k**2 * self.data.chi
        ### get root positions to capture whole fluctuation periods
        positive = np.where(np.clip(np.diff(np.sign(data[(self.data.k > 2)&(self.data.k < 13)])), 0, np.inf))[0]
        negative = np.where(np.clip(np.diff(np.sign(data[(self.data.k > 2)&(self.data.k < 13)])), -np.inf,0))[0]
        ### determine kmin and kmax and cap kmax to 15
        self.kmin = self.data.k[(self.data.k > 2)&(self.data.k < 13)][positive[0]]
        self.kmax = self.data.k[(self.data.k > 2)&(self.data.k < 13)][negative[-1]]
        # self.kmin = self.data.k[self.data.k > 2][positive[0]]
        # self.kmax = self.data.k[self.data.k > 2][negative[-1]]
        if self.kmax > 13: self.kmax = 13
        ### transform data to R
        xafs.xftf(k=self.data.k, chi=self.data.chi, group=self.data,
                  dk = 1,
                  kmin = self.kmin,
                  kmax = self.kmax,
                  kweight = 2,
                  rmax_out = 12,
                  window = 'hanning',
                  )

        ### estimate noise with larch, this is but a estimation and should be
        ### regarded with caution!
        ### TODO
        xafs.estimate_noise(k=self.data.k,
                            chi=self.data.chi,
                            group=self.data,
                            rmin=self.data.r.max() - self.data.r.max() * 0.25,
                            rmax=self.data.r.max(),
                            _larch=Interpreter(),
                            )
        return self.data


    def plot_data(self, data_type = 'RAW', 
                  show = False, save_path = None):
        """
        generic function to generate plots of different data types

        Parameters
        ----------
        data_type : str, optional
            type of data to beplotted. Either "RAW", "NORMALIZED", "k", "R" or 
            "BACKGROUND". The default is 'RAW'.
        show : bool, optional
            True if the plots shall be plotted in an extra window (for debugging).
            The default is False.
        save_path : str, optional
            absolute path to a folder, where the plots shall be saved.
            The default is None.

        Returns
        -------
        matplotlib.figure
            matplotlib figure with the data plotted.
        """
        
        ### define figure
        self.fig_data = plt.figure("{} {}".format(data_type, self.name), figsize=(10, 6.25))
        self.fig_data.clf()
        self.ax_data = self.fig_data.subplots()
        self.ax_data.grid()
        ### calculate default ticks
        major_ticks = np.arange(self.data.energy[0], self.data.energy[-1], 100)
        minor_ticks = np.arange(self.data.energy[0], self.data.energy[-1], 20)
        ### legend location
        loc = 'lower right'
        ### plot data depending on type
        if data_type == 'RAW' or data_type == "BACKGROUND":
            ### plotting
            self.ax_data.plot(self.data.energy, self.data.mu,
                              label="Measurement {}".format(self.name),
                              color = "#003161")
            self.ax_data.plot(self.data.e0,
                              self.data.mu[np.where(self.data.e0 == self.data.energy)],
                              marker = "*", color = "#69398B", 
                              label="edge position",)
            ### if background shall be plotted
            if data_type == "BACKGROUND":
                self.ax_data.plot(self.data.energy, self.data.pre_edge, 
                                  label="Pre Edge Background")
                self.ax_data.plot(self.data.energy, self.data.post_edge, 
                                  label="Post Edge Background")
                self.ax_data.plot(self.data.energy, self.data.flat,
                                  label="Flattened Normalized {}".format(self.name),)
            ### labelling
            self.ax_data.set_xlabel(r"Energy | eV")
            self.ax_data.set_ylabel(r"$\mu (E)$ | a.u.")
            ### set ticks
            self.ax_data.set_xticks(major_ticks)
            self.ax_data.set_xticks(minor_ticks, minor=True)
            ### limiting
            self.ax_data.set_xlim(self.data.energy[0], self.data.energy[-1])
        elif data_type == 'NORMALIZED':
            ### plotting
            self.ax_data.plot(self.data.energy, self.data.flat, 
                              label="{} {}".format(data_type, self.name),
                              color = "#003161")
            self.ax_data.plot(self.data.e0,
                              self.data.flat[np.where(self.data.e0 == self.data.energy)],
                              marker = "*", color = "#69398B", 
                              label="edge position",)
            ### labelling
            self.ax_data.set_xlabel(r"Energy | eV")
            self.ax_data.set_ylabel(r"$\mu (E)$ | a.u.")
            ### set ticks
            self.ax_data.set_xticks(major_ticks)
            self.ax_data.set_xticks(minor_ticks, minor=True)
            ### limiting
            self.ax_data.set_xlim(self.data.e0-30, self.data.e0+100)
            self.ax_data.set_ylim(0)
            # self.ax_data.set_xlim(self.data.energy[0], self.data.energy[-1])
        elif data_type == 'k':
            ### calculate specific ticks
            major_ticks = np.arange(self.data.k[0], self.data.k[-1], 2)
            minor_ticks = np.arange(self.data.k[0], self.data.k[-1], 0.5)
            ### calculate data k**2*chi
            data = self.data.k**2 * self.data.chi 
            data = self.clip_data(data)
            ### plotting
            self.ax_data.plot(self.data.k, data, 
                              label="{}".format(data_type),
                              color = "#003161")
            ### labelling
            self.ax_data.set_xlabel(r"k | $\AA^{-1}$")
            self.ax_data.set_ylabel(r"$k^2\chi(k) | \AA^{-1}$")
            ### set ticks
            self.ax_data.set_xticks(major_ticks)
            self.ax_data.set_xticks(minor_ticks, minor=True)
            ### limiting
            if self.data.k.max() > 15: xmax = 15
            else: xmax = self.data.k.max()
            # self.ax_data.set_xlim(self.data.k[0], self.data.k[-1])
            self.ax_data.set_xlim(0, xmax)
            ymin = np.min(data[len(data)//8:-len(data)//8]) - 0.01
            ymax = np.max(data[len(data)//8:-len(data)//8]) + 0.01
            # if ymin < -3: ymin = -3
            # if ymax > 3: ymax = 3
            self.ax_data.set_ylim(ymin, ymax)
            loc = 'upper left'
        elif data_type == 'R':
            ### calculate specific ticks
            major_ticks = np.arange(self.data.r[0], self.data.r[-1], 2)
            minor_ticks = np.arange(self.data.r[0], self.data.r[-1], 0.5)
            ### plotting
            self.ax_data.plot(self.data.r, np.abs(self.data.chir), 
                              label="{}".format(data_type), color = "#003161")
            ### labelling
            self.ax_data.set_xlabel(r"$R(\AA)$")
            self.ax_data.set_ylabel(r"$\left| \chi(R) \right| \AA^{-3}$")
            ### set ticks
            self.ax_data.set_xticks(major_ticks)
            self.ax_data.set_xticks(minor_ticks, minor=True)
            ### limiting
            self.ax_data.set_xlim(0, 6)
            self.ax_data.set_ylim(0)
            ### legend positioning
            loc = 'upper right'
            # self.ax_data.set_xlim(self.data.r[0], self.data.r[-1])
        ### set title
        self.ax_data.set_title(self.name)
        ### set legend
        self.ax_data.legend(loc = loc)
        ### show figure if desired
        if show:
            self.fig_data.show()
        if save_path:
            self.fig_data.savefig(save_path)
        return self.fig_data
    

    def check_edge_step(self, ):
        """
        this function automatically evaluates the edge step of the given data
        """
        if (self.quality_criteria_sample["edge step"]["min"]
            <= self.data.edge_step
            <= self.quality_criteria_sample["edge step"]["max"]):
            if self.verbose:
                print("\u2705 edge step of good quality: {:.2f}".format(self.data.edge_step))
            return True, self.data.edge_step
        else:
            if self.verbose:
                print("\u274e edge step doesn't meet standards: {:.2f}".format(self.data.edge_step))
            return False, self.data.edge_step


    def check_energy_resolution(self, ):
        """
        this function automatically evaluates the energy resolution of the
        given data
        """
        self.data.energy_resolution = self.data.energy[1] - self.data.energy[0]
        if (self.quality_criteria_sample["energy resolution"]["min"]
            <= self.data.energy_resolution
            <= self.quality_criteria_sample["energy resolution"]["max"]):
            if self.verbose:
                print("\u2705 energy resolution of good quality: {:.2f}eV".format(self.data.energy_resolution))
            return True, self.data.energy_resolution
        else:
            if self.verbose:
                print("\u274e energy resolution doesn't meet standards: {:.2f}eV".format(self.data.energy_resolution))
            return False, self.data.energy_resolution


    def check_k(self, ):
        """
        this function automatically evaluates the k range of the given data
        """
        if (self.quality_criteria_sample["k max"]["min"]
            <= self.data.k[-1]
            <= self.quality_criteria_sample["k max"]["max"]):
            if self.verbose:
                print("\u2705 k max of good quality: {:.2f}\u212b⁻¹".format(self.data.k[-1]))
            return True, self.data.k[-1]
        else:
            if self.verbose:
                print("\u274e k max doesn't meet standards: {:.2f}\u212b⁻¹".format(self.data.k[-1]))
            return False, self.data.k[-1]


    def estimate_noise(self, ):
        """
        this function automatically estimates the noise in the k regime of
        the given data
        """

        if (self.quality_criteria_sample["noise"]["min"]
            <= self.data.epsilon_k
            <= self.quality_criteria_sample["noise"]["max"]):
            if self.verbose:
                print("\u2705 estimated noise of good quality: {:.2f}".format(self.data.epsilon_k))
            return True, self.data.epsilon_k
        else:
            if self.verbose:
                print("\u274e estimated noise doesn't meet standards: {:.2f}".format(self.data.epsilon_k))
            return False, self.data.epsilon_k


    def create_data_json(self, owner = '', owner_group = '', access_group = '',
                         creation_location = '', principal_investigator = '',
                         data_name = '', data_type = '',
                         is_published = False, source_folder = '',
                         contact_email = '', source = 'SYNCHROTRON',
                         measurement_mode = 'ABSORPTION',
                         ):
        """
        This function creates a json file from the loaded data

        Parameters
        ----------
        owner : str, optional
            name of the researcher which performed the measurement. The default is ''.
        owner_group : str, optional
            name of the research group which performed the measurement. The default is ''.
        access_group : str, optional
            name of the group which has access to thed ata. The default is ''.
        creation_location : str, optional
            name of the location measured, should be 'Facility, City, Country'. The default is ''.
        principal_investigator : str, optional
            name of the researcher which performed the measurement. The default is ''.
        data_name : str, optional
            unique an descriptive nane of the data. The default is ''.
        data_type : str, optional
            type of the data, either RAW, PREPROCESSED or PROCESSED. The default is 'RAW'.
        is_published : bool, optional
            If the data is already published. The default is False.
        source_folder : str, optional
            Path to the folder. The default is ''.
        contact_email : str, optional
            contact e-mail of the owner. The default is ''.
        source : str, optional
            type of the source, either SYNCHROTRON or LABORATORY. The default is 'SYNCHROTRON'.
        measurement_mode : str, optional
            Mode of measurement, either ABSORPTION or FLUORESCENCE. The default is 'ABSORPTION'.
        """
        data = {"owner": owner,
                "principal_investigator": principal_investigator,
                "owner_group": owner_group,
                "access_groups": access_group,
                "creation_location": creation_location,
                "dataset_name": data_name + datetime.now().strftime("%Y-%m-%d-%H_%M_%S"),
                "type": data_type,
                "is_published": is_published,
                "creation_time": str(datetime.now().isoformat()),
                "source_folder": source_folder,
                "contact_email": contact_email,
                "scientific_metadata": {
                "energy": {"value": list(self.data.energy), "unit": "eV"},
                "mu": {"value": list(self.data.mu), "unit": "a.u."},
                "source": source,
                "mode": measurement_mode,
                "processed": data_type,},
                }
        with open(os.path.abspath(os.curdir)+ "/example data/LABORATORY/{}.json".format(self.name),"w") as tofile:
            json.dump(data, tofile, indent=4, ensure_ascii=False)


    def first_shell_fit(self, ):
        """
        Function to automatically fit the first shell with larch. Not yet 
        implemented #TODO
        """
        pars = fitting.param_group(amp=fitting.param(1.0, vary=True),
                                   del_e0=fitting.param(0.0, vary=True),
                                   sig2=fitting.param(0.0, vary=True),
                                   del_r=fitting.guess(0.0, vary=True),
                                   )


    def encode_base64_figure(self, figure):
        """
        encode a matplotlib figure to base64 for storage

        Parameters
        ----------
        figure : matplotlib.figure
            matplotlib figure with relevant data.

        Returns
        -------
        str
            base64 encoded string of the figure.

        """
        buffer = io.BytesIO()
        figure.savefig(buffer, format="jpeg")
        data = base64.b64encode(buffer.getbuffer()).decode("ascii")
        return f"data:image/jpeg;base64,{data}"


    def decode_base64_figure(self, base64_string):
        """
        decode a matplotlib figure from base64 

        Parameters
        ----------
        base64_string : str
            base64 encoded matplotlib.figure

        Returns
        -------
        image
            image of the matplotlib.figure

        """
        image_base64 = base64_string.replace("data:image/jpeg;base64,", "")
        image_base64 = base64.b64decode(image_base64)
        image_data = io.BytesIO(image_base64)
        image = Image.open(image_data)
        return image


class check_quality_control(object):
    """
    This checks the quality control for a given facility type. It looks for data
    in the example data folder.
    Supported facility_type are LABORATORY; SYNCHROTRON and must be a string.
    The plot_ variables have to be BOOLEAN. They define, if a dataset is plotted
    or not.
    """

    def __init__(self, facility_type, 
                 plot_raw_data = False, plot_normalized_data = False,
                 plot_k = False, plot_R = False, plot_background = False,
                 save_figure_path = None,
                 verbose = False):
        """
        Parameters
        ----------
        facility_type : str
            type of the facility, either SYNCHROTRON or LABORATORY.
        plot_raw_data : bool, optional
            plot µ(E)_measured. The default is False.
        plot_normalized_data : bool, optional
            plot µ(E)_normalized. The default is False.
        plot_k : bool, optional
            plot chi(k). The default is False.
        plot_R : bool, optional
            plot chi(R). The default is False.
        save_figure_path : str, optional
            absolute path to the folder where figures shall be stored.
            The default is None.
        verbose : bool, optional
            if True certain data are printed
        """
        ### store the given data in the self instance
        self.facility_type = facility_type
        self.plot_raw_data = plot_raw_data
        self.plot_normalized_data = plot_normalized_data
        self.plot_k = plot_k
        self.plot_R = plot_R
        self.plot_background = plot_background
        self.save_figure_path = save_figure_path
        self.verbose = verbose
        ### initialize the read_data plugin with the facility type
        ### !!! only one type allowed per init
        self.read_data = read_data(source = facility_type)
        ### perform the quality control
        self.results = self.check_data()


    def check_data(self, ):
        """
        This function reads out the quality criteria from the Criteria.json,
        search for all files in the specific examples data folder and checks
        the quality for each sample iterative. If verbose mode is activated
        the results are printed.

        """
        ### read out quality criteria
        cq_json = os.path.abspath(os.curdir) + "/Criteria.json"
        ### check out all files
        folder = os.path.abspath(os.curdir) + f"/example data/{self.facility_type}/"
        # folder = '/home/frank/Doktorarbeit/DAPHNE/Measurement Data/SYNCHROTRON/'
        # files = sorted(glob(folder+'*.xdi'))#[2:3]
        files = sorted(glob(folder+'*.h5'))#[2:3]
        ### initialize the check_quality class
        cq = check_quality(quality_criteria_json=cq_json, verbose=self.verbose)
        ### analyse the quality for each file in the files list
        for file in files:
            if self.verbose:
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print('working on {}'.format(file.split('/')[-1]))
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                print("file:\t", file.split('/')[-1])
            ### transform the name variable corresponding to the host platform
            if "win" in platform:
                name = file.split("\\")[-1].split(".")[0]
            else:
                name = file.split("/")[-1].split(".")[0]
            ### initialize the quality control list to store quality data of
            ### the analysed file
            self.qc_list = []
            ### read out the data of the file
            self.read_data.process_data(data_path = file)
            cq.load_data(self.read_data.data, source=self.facility_type, name=name)
            if self.verbose:
                print('meas data loaded:', self.read_data.data.shape)
                print('energy:', self.read_data.data[0])
                print('mu:', self.read_data.data[1])
            self.data = cq.preprocess_data()
            if self.verbose:
                print('guessed element and edge: ', cq.data.element_n_edge)
                print('E0: {:.0f}eV'.format(cq.data.e0))
                print('k-range: {:.1f}-{:.1f}'.format(cq.kmin, cq.kmax))
            if self.save_figure_path: show = False
            else:
                show = True
                save_path= None
            
            if self.plot_raw_data:
                if self.save_figure_path: save_path = self.save_figure_path+'/RAW/{}_RAW.png'.format(name)
                fig_raw_data = cq.plot_data(data_type='RAW',
                                            show = show, 
                                            save_path = save_path)
                fig_raw_data_base64 = cq.encode_base64_figure(fig_raw_data)
                image_data = cq.decode_base64_figure(base64_string=fig_raw_data_base64)
            if self.plot_normalized_data:
                if self.save_figure_path: save_path = self.save_figure_path+'/NORMALIZED/{}_NORMALIZED.png'.format(name)
                fig_normalized_data = cq.plot_data(data_type = 'NORMALIZED',
                                                   show = show,
                                                   save_path = save_path)
                fig_normalized_data_base64 = cq.encode_base64_figure(fig_normalized_data)
                image_data = cq.decode_base64_figure(base64_string=fig_normalized_data_base64)
            if self.plot_k:
                if self.save_figure_path: save_path = self.save_figure_path+'/k/{}_k.png'.format(name)
                fig_k = cq.plot_data(data_type = 'k',
                                     show=show, save_path = save_path)
                fig_k_base64 = cq.encode_base64_figure(fig_k)
                image_k = cq.decode_base64_figure(base64_string=fig_k_base64)
            if self.plot_R:
                if self.save_figure_path: save_path = self.save_figure_path+'/R/{}_R.png'.format(name)
                fig_R = cq.plot_data(data_type = 'R',
                                     show=show, save_path = save_path)
                fig_R_base64 = cq.encode_base64_figure(fig_R)
                image_R = cq.decode_base64_figure(base64_string=fig_R_base64)
            if self.plot_background:
                if self.save_figure_path: save_path = self.save_figure_path+'/BACKGROUND/{}_BACKGROUND.png'.format(name)
                fig_background = cq.plot_data(data_type = 'BACKGROUND',
                                     show=show, save_path = save_path)
                fig_background_base64 = cq.encode_base64_figure(fig_background)
                image_background = cq.decode_base64_figure(base64_string=fig_background_base64)
            
            self.qc_list.append(cq.check_edge_step())
            self.qc_list.append(cq.check_energy_resolution())
            self.qc_list.append(cq.check_k())
            self.qc_list.append(cq.estimate_noise())
            
            if self.verbose:
                if all(np.array(self.qc_list)[:, 0]):
                    print("quality approved")
                else:
                    print("data not matchs all quality criteria, please check")
            self.read_data.print_mu()
            # cq.first_shell_fit()
        return cq.data
            
if __name__ == '__main__':
    test = check_quality_control(facility_type = 'SYNCHROTRON', 
                          plot_raw_data = True,
                          plot_normalized_data = True,
                          plot_R = True,
                          plot_k = True,
                          plot_background = True,
                          save_figure_path = os.environ['HOME']+'/Doktorarbeit/DAPHNE/Quality Criteria/evaluated',
                          verbose = True,
                          )
    pass