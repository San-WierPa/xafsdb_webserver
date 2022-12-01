#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:33:49 2020

@author: frank
"""

##############################################################################
# import h5py
from glob import glob

# from time import time
import matplotlib

matplotlib.use("tkagg")
import json

import matplotlib.pyplot as plt
# import larch
# from larch.io import read_ascii
import numpy as np
from larch import Group, Interpreter, fitting, xafs
from PIL import Image

plt.ioff()
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["xtick.top"] = True
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["ytick.right"] = True
plt.rcParams["axes.grid.which"] = "both"
import base64
# print('running on ', platform)
import io
import os
from datetime import datetime
from sys import platform

##############################################################################
### define ###
##############################################################################


class check_quality(object):
    """
    This class implements the automated checkers for the quality criteria
    of XAFS measurements
    """

    def __init__(self, quality_criteria_json):
        print("quality criteria function initialized")
        with open(quality_criteria_json, "r") as f:
            self.quality_criteria = json.load(f)

    def load_data(
        self,
        measurement_data,
        source="SYNCHROTRON",
        mode="ABSORPTION",
        processed="RAW",
        name=None,
        plot=True,
    ):
        """
        This function loads the data to process it further.

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

        Returns
        -------
        None.

        """
        if name is None:
            self.name = "sample"
        else:
            self.name = name
        self.plot = plot
        self.source = source
        self.mode = mode
        self.processed = processed
        self.quality_criteria_sample = self.quality_criteria[self.source][self.mode][
            self.processed
        ]
        self.data = Group()
        self.data.energy = measurement_data[:, 0]
        self.data.mu = measurement_data[:, 1]

    def preprocess_data(
        self,
    ):
        """
        This function preprocesses the data, finds the edge, fits the pre and post
        edge.
        """
        edge = xafs.find_e0(self.data.energy, self.data.mu, group=self.data)
        # index = np.where(self.data.energy == edge)
        # self.data.energy = self.data.energy[index[0][0]-550:]
        # self.data.mu = self.data.mu[index[0][0]-550:]
        # index = np.where(self.data.energy == edge)[0][0]
        ### calculate the edge position
        xafs.pre_edge(
            energy=self.data.energy,
            mu=self.data.mu,
            e0=self.data.e0,
            group=self.data,
            pre1=-140,
            pre2=-30,
            make_flat=True,
            nvict=3,
        )
        ### estimate pre and post edge
        xafs.autobk(energy=self.data.energy, mu=self.data.mu, group=self.data)

        xafs.xftf(k=self.data.k, chi=self.data.chi, group=self.data)

        ### estimate noise #TODO
        xafs.estimate_noise(
            k=self.data.k,
            chi=self.data.chi,
            group=self.data,
            rmin=self.data.r.max() - self.data.r.max() * 0.25,
            rmax=self.data.r.max(),
            # kweight = 1,
            # kmin = self.data.k.min(),
            # kmax = self.data.k.max(),
            # dk = 4,
            # dk2 = 1,
            # kstep = self.data.k[1]-self.data.k[0],
            # kwindow = 'kaiser',
            # nfft = 2048,
            _larch=Interpreter(),
        )
        return self.data

    def plot_background(self, show=False, save_path=None):
        ### define figures
        self.fig_data = plt.figure("{}".format(self.name), figsize=(10, 6.25))
        self.fig_data.clf()
        self.ax_data = self.fig_data.subplots()
        self.ax_data.grid()
        major_ticks = np.arange(self.data.energy[0], self.data.energy[-1], 100)
        minor_ticks = np.arange(self.data.energy[0], self.data.energy[-1], 20)

        ### plot data
        self.ax_data.plot(
            self.data.energy, self.data.mu, label="Measuement {}".format(self.name)
        )
        self.ax_data.plot(
            self.data.e0,
            self.data.mu[np.where(self.data.e0 == self.data.energy)],
            "r*",
            label="edge position",
        )
        self.ax_data.plot(
            self.data.energy, self.data.pre_edge, label="Pre Edge Background"
        )
        self.ax_data.plot(
            self.data.energy, self.data.post_edge, label="Post Edge Background"
        )
        self.ax_data.plot(
            self.data.energy,
            self.data.flat,
            label="Flattened Normalized {}".format(self.name),
        )
        self.ax_data.set_title(self.name)
        self.ax_data.set_xlabel(r" Energy | eV")
        self.ax_data.set_ylabel(r"$\mu (E)$ | a.u.")
        self.ax_data.set_xlim(self.data.energy[0], self.data.energy[-1])
        self.ax_data.set_ylim(0.0)
        self.ax_data.legend(loc=1)
        self.ax_data.set_xticks(major_ticks)
        self.ax_data.set_xticks(minor_ticks, minor=True)
        if show:
            self.fig_data.show()
        if save_path:
            self.fig_data.savefig(save_path)
        return self.fig_data

    def plot_k(self, show=False, save_path=None):
        self.fig_k = plt.figure("k {}".format(self.name), figsize=(10, 6.25))
        self.fig_k.clf()
        self.ax_k = self.fig_k.subplots()
        self.ax_k.grid()
        data = self.data.k**2 * self.data.chi
        self.ax_k.plot(self.data.k, data, label="data")
        self.ax_k.set_title(self.name)
        self.ax_k.set_xlabel("k | $\AA^{-1}$")
        self.ax_k.set_ylabel(r"$k^2\chi(k) | \AA^{-1}$")
        self.ax_k.set_xlim(self.data.k[0], self.data.k[-1])
        self.ax_k.legend(loc=1)
        self.ax_k.set_xticks(np.arange(self.data.k[0], self.data.k[-1], 2))
        self.ax_k.set_xticks(
            np.arange(self.data.k[0], self.data.k[-1], 0.5), minor=True
        )
        self.ax_k.set_ylim(-np.max(data) - 0.01, np.max(data) + 0.01)
        if show:
            self.fig_k.show()
        if save_path:
            self.fig_k.savefig(save_path)
        return self.fig_k

    def plot_R(self, show=False, save_path=None):
        self.fig_R = plt.figure("r {}".format(self.name), figsize=(10, 6.25))
        self.fig_R.clf()
        self.ax_R = self.fig_R.subplots()
        self.ax_R.grid()
        self.ax_R.plot(self.data.r, np.abs(self.data.chir), label="data")
        self.ax_R.set_title(self.name)
        self.ax_R.set_xlabel(r"$R(\AA)$")
        self.ax_R.set_ylabel(r"$\left| \chi(R) \right| \AA^{-3}$")
        self.ax_R.set_xlim(self.data.r[0], self.data.r[-1])
        self.ax_R.legend(loc=1)
        self.ax_R.set_xticks(np.arange(self.data.r[0], self.data.r[-1], 2))
        self.ax_R.set_xticks(
            np.arange(self.data.r[0], self.data.r[-1], 0.5), minor=True
        )
        self.ax_R.set_ylim(0)
        if show:
            self.fig_R.show()
        if save_path:
            self.fig_R.savefig(save_path)
        return self.fig_R

    def check_edge_step(
        self,
    ):
        """
        this function automatically evaluates the edge step of the given data
        """
        if (
            self.quality_criteria_sample["edge step"]["min"]
            <= self.data.edge_step
            <= self.quality_criteria_sample["edge step"]["max"]
        ):
            print("\u2705 edge step of good quality: ", self.data.edge_step)
            return True, self.data.edge_step
        else:
            print("\u274e edge step doesn't meet standards: ", self.data.edge_step)
            return False, self.data.edge_step

    def check_energy_resolution(
        self,
    ):
        """
        this function automatically evaluates the energy resolution of the
        given data
        """
        self.data.energy_resolution = self.data.energy[1] - self.data.energy[0]
        if (
            self.quality_criteria_sample["energy resolution"]["min"]
            <= self.data.energy_resolution
            <= self.quality_criteria_sample["energy resolution"]["max"]
        ):
            print(
                "\u2705 energy resolution of good quality: ",
                self.data.energy_resolution,
                "eV",
            )
            return True, self.data.energy_resolution
        else:
            print(
                "\u274e energy resolution doesn't meet standards: ",
                self.data.energy_resolution,
                "eV",
            )
            return False, self.data.energy_resolution

    def check_k(
        self,
    ):
        """
        this function automatically evaluates the k range of the given data
        """
        if (
            self.quality_criteria_sample["k max"]["min"]
            <= self.data.k[-1]
            <= self.quality_criteria_sample["k max"]["max"]
        ):
            print("\u2705 k max of good quality: ", self.data.k[-1], "\u212b⁻¹")
            return True, self.data.k[-1]
        else:
            print("\u274e k max doesn't meet standards: ", self.data.k[-1], "\u212b⁻¹")
            return False, self.data.k[-1]

    def estimate_noise(
        self,
    ):
        """
        this function automatically estimates the noise in the k regime of
        the given data
        """

        if (
            self.quality_criteria_sample["noise"]["min"]
            <= self.data.epsilon_k
            <= self.quality_criteria_sample["noise"]["max"]
        ):
            print("\u2705 estimated noise of good quality: ", self.data.epsilon_k)
            return True, self.data.epsilon_k
        else:
            print(
                "\u274e estimated noise doesn't meet standards: ", self.data.epsilon_k
            )
            return False, self.data.epsilon_k

    def create_data_json(
        self,
    ):
        data = {
            "owner_group": "Technische Universität Berlin",
            "access_groups": "None",
            "creation_location": "Berlin, Germany",  # added manually to openapi.json (using https://editor.swagger.io/)
            "principal_investigator": "Sebastian Praetz",  # added manually to openapi.json
            "dataset_name": "test " + datetime.now().strftime("%Y-%m-%d-%H_%M_%S"),
            "type": "raw",
            "is_published": False,
            "creation_time": str(datetime.now().isoformat()),
            "source_folder": "None",
            "owner": "None",
            "contact_email": "ffoerste@physik.tu-berlin.de",
            "scientific_metadata": {
                "energy": {"value": list(self.data.energy), "unit": "eV"},
                "mu": {"value": list(self.data.mu), "unit": "a.u."},
                "source": "LABORATORY",
                "mode": "ABSORPTION",
                "processed": "RAW",
            },
        }
        with open(
            os.path.abspath(os.curdir)
            + "/example data/LABORATORY/{}.json".format(self.name),
            "w",
        ) as tofile:
            json.dump(data, tofile, indent=4, ensure_ascii=False)

    def first_shell_fit(
        self,
    ):
        pars = fitting.param_group(
            amp=fitting.param(1.0, vary=True),
            del_e0=fitting.param(0.0, vary=True),
            sig2=fitting.param(0.0, vary=True),
            del_r=fitting.guess(0.0, vary=True),
        )
        # path1 = xafs.feffpath('fit_path_test.dat',
        #                       s02    = 'amp',
        #                       e0     = 'del_e0',
        #                       sigma2 = 'sig2',
        #                       deltar = 'del_r')

        # trans = xafs.feffit_transform(kmin=3,
        #                               kmax=17,
        #                               kw=2,
        #                               dk=4,
        #                               window='kaiser',
        #                               rmin=1.4,
        #                               rmax=3.0)
        # define dataset to include data, pathlist, transform
        # dset = xafs.feffit_dataset(data=self.data, pathlist=[path1], transform=trans)
        # perform fit!
        # out = xafs.feffit(pars, dset)
        # print(xafs.feffit_report(out))
        # try:
        #     fout = open('doc_feffit1.out', 'w')
        #     fout.write("%s\n" % feffit_report(out))
        #     fout.close()
        # except:
        #     print('could not write doc_feffit1.out')

    def encode_base64_figure(self, figure):
        buffer = io.BytesIO()
        figure.savefig(buffer, format="jpeg")
        data = base64.b64encode(buffer.getbuffer()).decode("ascii")
        return f"data:image/jpeg;base64,{data}"

    def decode_base64_figure(self, base64_string):
        image_base64 = base64_string.replace("data:image/jpeg;base64,", "")
        image_base64 = base64.b64decode(image_base64)
        image_data = io.BytesIO(image_base64)
        image = Image.open(image_data)
        return image


## end examples/feffit/doc_feffit1.lar
test_cq = False
if test_cq:
    ### define data input
    cq_json = os.path.abspath(os.curdir) + "/Criteria.json"

    folder = os.path.abspath(os.curdir) + "/example data/LABORATORY/"
    files = glob(folder + "*.dat")[0:1]
    # files = [os.path.abspath(os.curdir)+'/example data/LABORATORY/Ni-K-Ni-foil-2mu.dat']
    # files = ['/home/frank/Doktorarbeit/DAPHNE/Quality Criteria/example data/LABORATORY/Co 5 mu.dat']
    # files = ['/home/frank/Doktorarbeit/DAPHNE/Measurement Data/Laboratory/foils/Ni-K-Ni-foil-2mu.dat']

    ### TODO Spektrum beschneiden  >>> Sache des Users
    ### 10 %
    ### EXAFS 600 eV
    cq = check_quality(quality_criteria_json=cq_json)
    for file in files:
        print("file:\t", file)
        if "win" in platform:
            name = file.split("\\")[-1].split(".")[0]
        else:
            name = file.split("/")[-1].split(".")[0]
        qc_list = []
        meas_data = np.loadtxt(file, skiprows=1)
        cq.load_data(meas_data, source="LABORATORY", name=name)
        data = cq.preprocess_data()
        fig_data = cq.plot_background(show=True, save_path=None)
        fig_data_base64 = cq.encode_base64_figure(fig_data)
        fig_k = cq.plot_k(show=True, save_path=None)
        fig_k_base64 = cq.encode_base64_figure(fig_k)
        fig_R = cq.plot_R(show=True, save_path=None)
        fig_R_base64 = cq.encode_base64_figure(fig_R)
        qc_list.append(cq.check_edge_step())
        qc_list.append(cq.check_energy_resolution())
        qc_list.append(cq.check_k())
        qc_list.append(cq.estimate_noise())
        if all(np.array(qc_list)[:, 0]):
            print("quality approved")
        #     cq.create_data_json()
        else:
            print("data not approved")
        cq.first_shell_fit()
        image_data = cq.decode_base64_figure(base64_string=fig_data_base64)
        image_k = cq.decode_base64_figure(base64_string=fig_k_base64)
        image_R = cq.decode_base64_figure(base64_string=fig_R_base64)
