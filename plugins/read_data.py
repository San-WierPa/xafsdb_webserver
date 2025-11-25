"""
@authors: Frank Foerste and Sebastian Paripsa
ffoerste@physik.tu-berlin.de, paripsa@uni-wuppertal.de
"""

import numpy as np
from larch.io import read_ascii, read_xdi, read_specfile
import h5py
import matplotlib.pyplot as plt
import base64
import io
plt.ioff()
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["xtick.top"] = True
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["ytick.right"] = True
plt.rcParams["axes.grid.which"] = "both"


class ReadData(object):
    """
    This class helps to read in different data types, .dat, .xdi are currently
    supported. A support for default detection of data by larch is also 
    implemented.
    """

    def __init__(self, source = "SYNCHROTRON", update_erange="",
                 scan_number = 0, verbose = False):
        """
        Initializing the ReadData class. This class helps to read in different 
        data types for XAS measurements, currently .dat, .xdi, .spec are 
        supported. A support for default detection of data by larch is also 
        implemented.

        Parameters
        ----------
        source : str, optional
            Type of source. Either SYNCHROTRON or LABORATORY. 
            The default is "SYNCHROTRON".
	update_erange: dict, optional
	    Updated energy range.
        scan_number : int, str, optional
            Number or name of the scan to check. Important for .mca, .spec and
            .h5 (from ESRF) For other file types this parameter is ignored.
            The default is 0.
        verbose : bool, optional
            Activate or deactivate the verbose mode. The default is False.
        """
        
        # give the class a version, x.y.date(YYYYMMDD)
        self.version = '0.1.20230612'
        self.scan_number = scan_number 
        self.verbose = verbose
        if self.verbose:
            print('ReadData class initialized -- v{}'.format(self.version))
        self.source = source
        # initialize dictionaries with supported beamlines and their specific
        # keywords by whom the beamline is identified. These are characteristic
        # for each file and has to be adapted when a change of syntax occurs
        # in the beamline datasets
        self.supported_beamlines = {"SYNCHROTRON" : ["CATACT KIT", 
                                                     "PETRA III Extension Beamline P65",
                                                     "PETRA III Extension Beamline P64",
                                                     "ELETTRA XAFS", "SLRI", "ESRF BM 23", 
                                                     "SOLEIL ROCK", "SOLEIL SAMBA",
                                                     "SLS", "DELTA", "SOLARIS",
                                                      ],
                                     "LABORATORY" : ["TU Berlin",
                                                     ]
                                     }
        self.beamline_key_words = {"SYNCHROTRON" : {"CATACT KIT" : ["catexp",],
                                                    "PETRA III Extension Beamline P65" : ["PETRA III Extension Beamline P65",],
                                                    "PETRA III Extension Beamline P64" : ["##  0 - Position",],
                                                    "ELETTRA XAFS" : ["Project Name:"],
                                                    "SLRI" : ["BL8: X-ray Absorption Spectroscopy"],
                                                    "ESRF BM 23" : ["# ZapEnergy"],
                                                    "SOLEIL ROCK" : ["Synchrotron SOLEIL"],
                                                    "SOLEIL SAMBA" : ["#  Energy, Theta, XMU, FLUO, REF, FLUO_RAW, I0, I1, I2, I3"],
                                                    "SLS" : ["# posX	SAI01-MEAN	SAI02-MEAN"],
                                                    "DELTA" : ["#  created:"],
                                                    "SOLARIS" : ['# C Acquisition started']
                                           },
                          "LABORATORY" : {"TU Berlin" : ["#  Energies_eV"],
                                          }
                          }
        # initialize the class to default
        self.reset_2_default()
        self.update_erange=update_erange

    def reset_2_default(self,):
        """
        Function to set all relevant data to default.
        """
        # set the beamline to None as undetected
        self.beamline = None 
        self.meta_data_dict = {}
        # the default source type is SYNCHROTRON. This is changed, when data
        # is read
        self.source = 'SYNCHROTRON'

    def process_data(self, data_path):
        """
        This function determines the datafile. If it is .hdf it will open
        the hdf-file with h5py, else it will open the datafile and read out
        the lines and checking for distinct keywords and starting the readout.

        Parameters
        ----------
        data_path : str
            absolute path to the xdi file.
        """
        self.data_path = data_path
        self.data_type = self.data_path.suffix
        if self.data_type in ['h5', 'hdf', 'hdf5']:
            self.load_hdf()
        elif self.data_type in ['.spec']:
            self.load_specfile()
        else:
            self.read_out_file()

    def read_out_file(self,):
        """
        This function reads every line of the file and checks, if any known
        keyword is in the file. When succesful, the beamline is stored and the
        specified load_data function is called.
        """
        # resetting to default, clear all data
        self.reset_2_default()
        # use larch to read out data and the header of the file
        self.larch_data = read_ascii(self.data_path)
        self.header = self.larch_data.header
        # now check the header for keywords for the specific beamlines
        for line in self.header:
            for beamline in self.supported_beamlines[self.source]:
                for keyword in self.beamline_key_words[self.source][beamline]:
                    if keyword in line:
                        self.beamline = beamline
                        break
        # if a beamline was found, e
        if self.beamline:
            if self.verbose:
                print('beamline found:\t', self.beamline)
            print('beamline found:\t', self.beamline)
            self.extract_header()
            self.load_data()
        else:
            print('no beamline found, going to numpy extraction mode')
            self.data = read_ascii(self.data_path).data[:2]
            # check unit of energy, if value below 100 it is most likely keV
            # --> change it to eV by multipying it with 1000
            if self.data[0,0] < 100:
                self.data[0] *= 1000
            self.meta_data_dict["E_range_min"] = self.data[0,0]
            self.meta_data_dict["E_range_max"] = self.data[0,-1]
            self.create_raw_plot_base64()


    def extract_header(self, data_path=None):
        """
        Function to exctract data from the header of the given datafile. This
        is of course specific for each beamline and has to be adapted and
        extended if changes in the beamline data occurs or new beamlines to be
        supported. Also until now only a limited set of metadata is read out.
        Namely: ['Facility', 'Beamline', 'Owner', 'Coll.code', 'Acq. mode',
                 'Temperature']

        Parameters
        ----------
        data_path : str
            Path to the loaded data.

        Returns
        -------
        dictionary
            containing all the found meta data

        """
        # enable header extraction mode
        # determine beamline
        if data_path:
            self.process_data(data_path=data_path)
        # fill all the meta data contained in the files provided by the facilities
        # into the dictionary
        self.meta_data_dict['Header'] = self.header
        self.meta_data_dict['Header_str'] = '\n'.join(self.header)
        self.meta_data_dict['Beamline'] = self.beamline
        coll_code = ''
        
        # SYNCHROTRON
        if self.beamline == "CATACT KIT":
            self.meta_data_dict['Facility'] = 'KIT Light Source'
            for line in self.header:
                line = line.replace('\n','')
                if '# F' in line: coll_code += line.split()[-1] + ' '
                elif '# E' in line: coll_code += line.split()[-1]
                elif '# D' in line: 
                    coll_code += line.replace('# D ','')
                    self.meta_data_dict['Coll.code'] = coll_code
                elif '# C' in line: self.meta_data_dict['Owner'] = line.split()[-1]
            # no further needed (as for 20230314) meta data in file
        elif self.beamline == "PETRA III Extension Beamline P65":
            self.meta_data_dict['Facility'] = "DESY"
            self.meta_data_dict['Beamline'] = "P65"
            # no further needed (as for 20230314) meta data in file
        elif self.beamline == "ELETTRA XAFS":
            self.meta_data_dict['Facility'] = "ELETTRA XAFS"
            self.meta_data_dict['Beamline'] = "XAFS"
            for line in self.header:
                line = line.replace('\n','')
                if 'Project Name' in line: self.meta_data_dict["Coll.code"] = line.split()[-1]
            # no further needed (as for 20230314) meta data in file
        elif self.beamline == "SLRI":
            self.meta_data_dict['Facility'] = "SLRI"
            for line in self.header:
                line = line.replace('\n','')
                if '# B' in line: self.meta_data_dict["Beamline"] = line.split(':')[0].replace('# ','')
                elif '# Transmission' in line: 
                    self.meta_data_dict["Acq. mode"] = "Transmission"
            # no further needed (as for 20230314) meta data in file
        elif self.beamline == "ESRF BM 23":
            self.meta_data_dict['Facility'] = "ESRF"
            # no further needed (as for 20230314) meta data in file
        elif self.beamline == "SOLEIL ROCK":
            self.meta_data_dict['Facility'] = "SOLEIL"
            for line in self.header:
                line = line.replace('\n','')
                if '# Sample temperature' in line:
                    try: self.meta_data_dict["Temperature"] = int(line.split('=')[-1])
                    except: pass
            # no further needed (as for 20230314) meta data in file
        elif self.beamline == "SOLEIL SAMBA":
            self.meta_data_dict['Facility'] = "SOLEIL"
            # no further meta data in file
        elif self.beamline == "SLS":
            self.meta_data_dict['Facility'] = "SLS"
            self.meta_data_dict['Beamline'] = "SLS SuperXAS"
            # no further meta data in file
        elif self.beamline == "SOLARIS":
            self.meta_data_dict['Facility'] = "SOLARIS"
            self.meta_data_dict['Beamline'] = "PIRX"  # TODO
            # no further meta data in file
            
            
        # LABORATORY
        elif self.beamline == "TU Berlin":
            self.meta_data_dict['Facility'] = "TU Berlin"
            # no further meta data in file
            
        # This dict is only for reference
        # it represents the xafsdb Widget meta data keys, not important for 
        # read out
        dummy_dict = {"owner_group": "Owner group",
                      "owner": "Owner",
                      "contact_email": "Contact email",
                      "Abstract": "Abstract",
                      "coll_code": "Coll.code",
                      "physical_state": "Phys.state",
                      "crystal_orientation": "Crystal orientation",
                      "temperature": "Temperature",
                      "pressure": "Pressure",
                      "sample_environment": "Sample environment",
                      "general_remarks": "General remarks",
                      "facility": "Facility",
                      "beamline": "Beamline",
                      "aquisition_mode": "Acq. mode",
                      "crystals": "Crystals",
                      "mirrors": "Mirrors",
                      "detectors": "Detectors",
                      "element_input": "Element",
                      "edge_input": "Edge",
                      "max_k_range": "Max k-range",
                      "doi": "DOI",
                      "EnergyColumn": "Energy Column",
                      "I_zeroColumn": "I0 Column",
                      "TransmissionColumn": "Transmission Column",
                      "MuColumn": "Mu Column",
                      "reference": "Reference",}
        return self.meta_data_dict
        
        
    def load_data(self,):
        """
        This function opens the data file and returns the data in the form of
        array([energy, mu]) depending of the found beamline. This has to be 
        adapted and extended if changes in the beamline data occurs or new 
        beamlines to be supported.

        Returns
        -------
        numpy.array
            array([energy, mu])
        """
        entries = [entry.lower() for entry in dir(self.larch_data)]
        print(f"entries - {entries}")
        # SYNCHROTRON
        if self.beamline == "CATACT KIT":
            self.larch_data.energy = self.larch_data.data[0, :]
            self.larch_data.I0 = self.larch_data.data[6, :]
            self.larch_data.transmission = self.larch_data.data[5, :]
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "PETRA III Extension Beamline P64":
            self.larch_data.energy = self.larch_data.data[0]
            self.larch_data.transmission = self.larch_data.data[1]
            self.larch_data.I0 = self.larch_data.data[3]
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "PETRA III Extension Beamline P65":
            if "mono_energy" in entries:
                self.larch_data.energy = self.larch_data.mono_energy
            elif "energy_enc" in entries:
                self.larch_data.energy = self.larch_data.energy_enc
            elif "e_enc" in entries:
                self.larch_data.energy = self.larch_data.e_enc
            if "vfc03" in entries:
                self.larch_data.I0 = self.larch_data.vfc03
            elif "i0" in entries:
                self.larch_data.I0 = self.larch_data.i2
            if "vfc02" in entries:
                self.larch_data.transmission = self.larch_data.vfc02
            elif "i2" in entries:
                self.larch_data.transmission = self.larch_data.i0
            if "_ev" in entries:
                self.larch_data.energy = self.larch_data.energy
                self.larch_data.mu = self.larch_data._ev
            try:
                self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
                if np.isnan(self.larch_data.mu).any() or np.isinf(self.larch_data.mu).any():
                    print("changing dataset, darn P65 always something special!")
                    self.larch_data.transmission = self.larch_data.i0
                    self.larch_data.I0 = self.larch_data.i1
                    self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
            except:
                print("no transmission data loaded")
        elif self.beamline == "ELETTRA XAFS":
            self.larch_data.energy = self.larch_data.data[0, :]
            self.larch_data.I0 = self.larch_data.data[3, :]
            self.larch_data.transmission = self.larch_data.data[2, :]
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "SLRI":
            self.larch_data.energy = self.larch_data.data[0, :]
            self.larch_data.I0 = self.larch_data.data[4, :]
            self.larch_data.transmission = self.larch_data.data[3, :]
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "ESRF BM 23":
            self.larch_data.energy = self.larch_data.data[0, :]
            self.larch_data.I0 = self.larch_data.data[2, :]
            self.larch_data.transmission = self.larch_data.data[1, :]
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "SOLEIL ROCK":
            entries = [entry.lower() for entry in dir(self.larch_data)]
            if "energy" in entries:
                self.larch_data.energy = self.larch_data.energy
            if "normalized" in entries:
                self.larch_data.mu = self.larch_data.normalized
            elif "i0" in entries:
                self.larch_data.I0 = self.larch_data.i1
            if "vfc02" in entries:
                self.larch_data.transmission = self.larch_data.vfc02
            elif "i1" in entries:
                self.larch_data.transmission = self.larch_data.i0
            
            if "shifted" in entries:
                self.larch_data.energy = self.larch_data.shifted
                self.larch_data.mu = self.larch_data.normalized
            try:
                self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
            except:
                print("no transmission data loaded")
        elif self.beamline == "SOLEIL SAMBA":
            self.larch_data.energy = self.larch_data.data[0, :]
            self.larch_data.I0 = self.larch_data.data[8, :]
            self.larch_data.transmission = self.larch_data.data[6, :]
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "SLS":
            self.larch_data.energy = self.larch_data.data[0, :]
            self.larch_data.I0 = self.larch_data.data[3, :]
            self.larch_data.transmission = self.larch_data.data[2, :]
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "DELTA":
            self.larch_data.energy = self.larch_data.data[0, :]
            self.larch_data.mu = self.larch_data.data[1, :]
        elif self.beamline == "SOLARIS":
            self.larch_data.mu = self.larch_data.d2/self.larch_data.sr
        
        # LABORATORY
        elif self.beamline == "TU Berlin":
            self.larch_data.energy = self.larch_data.data[0, :]
            self.larch_data.mu = self.larch_data.data[1, :]
        
        # check unit of energy, if value below 100 it is most likely keV
        # --> change it to eV by multipying it with 1000
        self.larch_data.energy = self.keV2eV(self.larch_data.energy)
        # sort the energy to be strictly increasing (for scipy spline in larch.autobk)
        energy_sorted_idx = self.larch_data.energy.argsort()
        self.larch_data.energy = self.larch_data.energy[energy_sorted_idx]
        self.larch_data.mu = self.larch_data.mu[energy_sorted_idx]
        diff_E = np.diff(self.larch_data.energy)
        mean_diff = diff_E.mean()
        remove_idx = np.where(diff_E>(mean_diff/10))
        # convert NaN to 0
        self.larch_data.energy = np.nan_to_num(self.larch_data.energy, posinf=0,
                                               neginf=0)
        self.larch_data.mu = np.nan_to_num(self.larch_data.mu, posinf=0,
                                            neginf=0)
        
        if self.beamline == "PETRA III Extension Beamline P65":
            self.larch_data.energy = self.larch_data.energy[remove_idx]
            self.larch_data.mu = self.larch_data.mu[remove_idx]
        
        # convert data to numpy array with [energy, mu]
        self.data = np.array([self.larch_data.energy, self.larch_data.mu])
        # set e-range
        self.meta_data_dict['E_range_min'] = np.round(self.data[0,0], decimals=1)
        self.meta_data_dict['E_range_max'] = np.round(self.data[0,-1], decimals=1)
        # create raw plot
        self.create_raw_plot_base64()

    def load_hdf(self,):
        """
        This function reads out h5 files. At the moment (20230614) only ESRF is
        providing their measurement data in an h5 file for the user. So only
        ESRF h5 format is supported. If more facilities are providing h5 files
        either a standard form is given or the facility has to be automatically 
        determined and a adapted procedure has to be developed.
        """
        # first check if a scan number is provided. If not set it to default
        # '1.1'
        self.header = ""

        if type(self.scan_number) == int:
            self.scan_number = '1.1'
            if self.verbose:
                print('No scan number for hdf5 files provided, setting to default 1.1')
        # now open the h5 and retrieve the measurement data
        with h5py.File(self.data_path, 'r') as f:
            self.h5_energy = f[self.scan_number]['measurement']['energy_cenc'][()]
            self.h5_mu = f[self.scan_number]['measurement']['mu_trans'][()]
        # check if energy is in eV
        self.h5_energy = self.keV2eV(self.h5_energy)
        # convert data to numpy array with [energy, mu]
        self.data = np.array([self.h5_energy, self.h5_mu])
        # set e-range
        self.meta_data_dict['E_range_min'] = np.round(self.data[0,0], decimals=1)
        self.meta_data_dict['E_range_max'] = np.round(self.data[0,-1], decimals=1)
        # create raw plot
        self.create_raw_plot_base64()


    def load_specfile(self,):
        """
        This function reads out spec files using the larch function 
        read_specfile. The scan number has to be provided, otherwise the default
        scan number = 0 is selected and loaded.as is a 
        """
        self.larch_data = read_specfile(self.data_path, scan=self.scan_number)
        self.larch_data.energy = self.larch_data.Energy
        self.larch_data.mu = self.larch_data.RingCurrent #  TODO this is not correct!!! No example data for implementation...
        #  check if energy is in eV
        self.larch_data.energy = self.keV2eV(self.larch_data.energy)
        #  convert data to numpy array with [energy, mu]
        self.data = np.array([self.larch_data.energy, self.larch_data.mu])
        #  set e-range
        self.meta_data_dict['E_range_min'] = np.round(self.data[0,0], decimals=1)
        self.meta_data_dict['E_range_max'] = np.round(self.data[0,-1], decimals=1)
        #  create raw plot
        self.create_raw_plot_base64()
        
        
    def create_raw_plot_base64(self, plot_data=False):
        """
        This function plots the read out data and creates a base64 string for 
        storing the plot.

        Parameters
        ----------
        plot_data : bool, optional
            To plot or not to plot the data, that is the question. The default 
            is False.
        """
        #  cut out e_min and e_max
        if self.update_erange:
            try:
                self.E_range_min = float(self.update_erange.get("E_range_min").replace(",", "."))
                self.E_range_max = float(self.update_erange.get("E_range_max").replace(",", "."))
                self.meta_data_dict["E_range_min"] = self.E_range_min
                self.meta_data_dict["E_range_max"] = self.E_range_max
                energy = self.data[0]
                mu = self.data[1]
                mu = mu[self.E_range_min <= energy]
                energy = energy[self.E_range_min <= energy]
                mu = mu[self.E_range_max >= energy]
                energy = energy[self.E_range_max >= energy]
                self.data = np.array([energy, mu])
            except (TypeError,AttributeError):
                print("Update of e-range not possible!")
        #  define figures
        self.fig_raw_data = plt.figure("Preview Raw Data", figsize=(10, 6.25))
        self.fig_raw_data.clf()
        self.ax_raw_data = self.fig_raw_data.subplots()
        self.ax_raw_data.grid()
        major_ticks = np.arange(self.data[0,0], self.data[0,-1], 100)
        minor_ticks = np.arange(self.data[0,0], self.data[0,-1], 20)

        # plot the raw data and label the axes and set the legend in the 
        # lower right corner
        self.ax_raw_data.plot(self.data[0], self.data[1],
                              label="Measurement",
                              color="#003161")
        
        self.ax_raw_data.set_xlabel(r" Energy | eV")
        self.ax_raw_data.set_ylabel(r"$\mu (E)$ | a.u.")
        self.ax_raw_data.set_xlim(self.data[0,0], self.data[0,-1])
        self.ax_raw_data.legend(loc = 'lower right')
        self.ax_raw_data.set_xticks(major_ticks)
        self.ax_raw_data.set_xticks(minor_ticks, minor=True)
        # create a widget and plot the data if specified
        if plot_data:
            self.fig_raw_data.canvas.draw()
            self.fig_raw_data.canvas.flush_events()
        # transform the matplotlib.figure to a base64 string and store it in
        # the meta-data dictionary
        buffer = io.BytesIO()
        self.fig_raw_data.savefig(buffer, format="jpeg")
        data = base64.b64encode(buffer.getbuffer()).decode("ascii")
        self.meta_data_dict["PreviewRawData"] = "data:image/jpeg;base64,{}".format(data)
    
        
    def keV2eV(self, energy):
        """
        This function checks if the energy loaded is in eV. If it is not in eV
        than the energy is most likely in keV and has to be converted from
        keV to eV by multiplying the given energy array with 1000.

        Parameters
        ----------
        energy : array
            array which contains the energy.

        Returns
        -------
        the energy in eV
        """
        if energy[0] < 100:
            return energy*1000
        else:
            return energy
        
    
    def print_mu(self):
        """
        Important function to draw a cow saying mu.
        """
        print("|¯¯¯¯¯|¯¯¯¯¯|¯¯¯¯¯|¯¯¯¯¯|")
        print("|\|/          (__)      |")
        print("|     `\------(oo)      |")
        print("|       ||    (__) <(mu)|")
        print("|       ||w--||     \|/ |")
        print("|   \|/                 |")
        print("|¯¯¯¯¯|¯¯¯¯¯|¯¯¯¯¯|¯¯¯¯¯|")
        print("QC succesfully performed")
