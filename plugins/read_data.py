#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:33:49 2020

@author: Frank Foerste
ffoerste@physik.tu-berlin.de
"""

##############################################################################
import numpy as np
from larch.io import read_ascii
import matplotlib.pyplot as plt
plt.ioff()
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["xtick.top"] = True
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["ytick.right"] = True
plt.rcParams["axes.grid.which"] = "both"
import base64
import io
##############################################################################
### define ###
##############################################################################
class read_data(object):
    """
    This class helps to read in different data types, .dat, .xdi are currently
    supported.
    """

    def __init__(self, source = "SYNCHROTRON"):
        print('read_data class initialized')
        self.source = source
        self.supported_beamlines = {"SYNCHROTRON" : ["CATACT KIT", 
                                                     "PETRA III Extension Beamline P65",
                                                     "ELETTRA XAFS", "SLRI", "ESRF BM 23", 
                                                     "SOLEIL ROCK", "SOLEIL SAMBA",
                                                     "SLS", "DELTA",
                                                      ],
                                     "LABORATORY" : ["TU Berlin",
                                                     ]
                                     }
        self.beamline_key_words = {"SYNCHROTRON" : {"CATACT KIT" : ["catexp",],
                                                    "PETRA III Extension Beamline P65" : ["PETRA III Extension Beamline P65",],
                                                    "ELETTRA XAFS" : ["Project Name:"],
                                                    "SLRI" : ["BL8: X-ray Absorption Spectroscopy"],
                                                    "ESRF BM 23" : ["#ZapEnergy"],
                                                    "SOLEIL ROCK" : ["Synchrotron SOLEIL"],
                                                    "SOLEIL SAMBA" : ["# Energy, Theta, XMU, FLUO, REF, FLUO_RAW, I0, I1, I2, I3"],
                                                    "SLS" : ["#posX	SAI01-MEAN	SAI02-MEAN"],
                                                    "DELTA" : ["# created:"]
                                           },
                          "LABORATORY" : {"TU Berlin" : ["# Energies_eV"],
                                          }
                          }
        # self.energy_key_words = ["0", ]
        self.reset_2_default()
        
    
    def reset_2_default(self,):
        self.beamline = None ### variable to determine if a beamline was matched
        self.meta_data_dict = {}
        self.source = 'SYNCHROTRON'
        
    
    def extract_header(self, data_path = None):
        """
        Function to exctract data from the header

        Parameters
        ----------
        data_path : str
            Path to the loaded data.

        Returns
        -------
        dictionary
            containing all the found meta data

        """
        ### enable header extraction mode
        ### determine beamline
        if data_path:
            self.process_data(data_path = data_path)
        ### fill all the meta data contained in the files provided by the facilities
        ### into the dictionary
        self.meta_data_dict = {}
        self.meta_data_dict['Header'] = self.header
        self.meta_data_dict['Beamline'] = self.beamline
        coll_code = ''
        if self.beamline == "CATACT KIT":
            self.meta_data_dict['Facility'] = 'KIT Light Source'
            for line in self.header:
                line = line.replace('\n','')
                if '#F' in line: coll_code += line.split()[-1] + ' '
                elif '#E' in line: coll_code += line.split()[-1]
                elif '#D' in line: 
                    coll_code += line.replace('#D ','')
                    self.meta_data_dict['Coll.code'] = coll_code
                elif '#C' in line: self.meta_data_dict['Owner'] = line.split()[-1]
            ### no further needed (as for 20230314) meta data in file
        elif self.beamline == "PETRA III Extension Beamline P65":
            self.meta_data_dict['Facility'] = "DESY"
            self.meta_data_dict['Beamline'] = "P65"
            ### no further needed (as for 20230314) meta data in file
        elif self.beamline == "ELETTRA XAFS":
            self.meta_data_dict['Facility'] = "ELETTRA XAFS"
            self.meta_data_dict['Beamline'] = "XAFS"
            for line in self.header:
                line = line.replace('\n','')
                if 'Project Name' in line: self.meta_data_dict["Coll.code"] = line.split()[-1]
            ### no further needed (as for 20230314) meta data in file
        elif self.beamline == "SLRI":
            self.meta_data_dict['Facility'] = "SLRI"
            for line in self.header:
                line = line.replace('\n','')
                if '#B' in line: self.meta_data_dict["Beamline"] = line.split(':')[0].replace('#','')
                elif '#Transmission' in line: 
                    self.meta_data_dict["Acq. mode"] = "Transmission"
            ### no further needed (as for 20230314) meta data in file
        elif self.beamline == "ESRF BM 23":
            self.meta_data_dict['Facility'] = "ESRF"
            ### no further needed (as for 20230314) meta data in file
        elif self.beamline == "SOLEIL ROCK":
            self.meta_data_dict['Facility'] = "SOLEIL"
            for line in self.header:
                line = line.replace('\n','')
                if '#Sample temperature' in line:
                    try: self.meta_data_dict["Temperature"] = int(line.split('=')[-1])
                    except: pass
            ### no further needed (as for 20230314) meta data in file
        elif self.beamline == "SOLEIL SAMBA":
            self.meta_data_dict['Facility'] = "SOLEIL"
            ### no further meta data in file
        elif self.beamline == "SLS":
            self.meta_data_dict['Facility'] = "SLS"
            self.meta_data_dict['Beamline'] = "SLS SuperXAS"
            ### no further meta data in file
        elif self.beamline == "TU Berlin":
            self.meta_data_dict['Facility'] = "TU Berlin"
            ### no further meta data in file
            
        ### This dict only represents the URL Widget names, not important for 
        ### read out only for reference
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
        
        
    def process_data(self, data_path):
        """
        This function determines the datafile. If it is .hdf it will open
        the hdf-file with h5py, else it will open the datafile and read out 
        the lines and checking for distinct keywords and starting the readout.

        Parameters
        ----------
        data_path : str
            absolute path to the xdi file.

        Returns
        -------
        None.

        """
        self.data_path = data_path
        self.data_type = self.data_path.split('.')[-1]
        if self.data_type in ['h5', 'hdf', 'hdf5']:
            self.load_hdf(self)
        else:
            self.read_out_file()
        

    def read_out_file(self,):
        """
        This function reads every line of the file and checks, if any known
        keyword is in the file. When succesful, the beamline is stored and the
        specified load_data function is called.

        Returns
        -------
        None.

        """
        ### resetting to default, clear all data
        self.reset_2_default()
        ### use larch to read out data and the header of the file
        self.larch_data = read_ascii(self.data_path)
        self.header = self.larch_data.header
        ### now check the header for keywords for the specific beamlines
        for line in self.header:
            for beamline in self.supported_beamlines[self.source]:
                for keyword in self.beamline_key_words[self.source][beamline]:
                    if keyword in line:
                        self.beamline = beamline
                        break
        ### if a beamline was found, e
        if self.beamline:
            print('beamline found:\t', self.beamline)
            self.extract_header()
            self.load_data()
        else:
            print('no beamline found, going to numpy extraction mode')
            self.data = read_ascii(self.data_path).data[:2]
            ### check unit of energy, if value below 100 it is most likely keV
            ### --> change it to eV by multipying it with 1000
            if self.data[0,0] < 100:
                self.data[0] *= 1000
            
    
    def load_data(self,):
        """
        This function opens the data file and returns the data in the form of
        array([energy, mu])

        Returns
        -------
        numpy.array
            array([energy, mu])

        """
        data = self.larch_data.data
        if self.beamline == "CATACT KIT":
            self.larch_data.energy = data[0, :]*1000
            self.larch_data.I0 = data[6, :]
            self.larch_data.transmission = data[5, :]
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "PETRA III Extension Beamline P65":
            self.larch_data.energy = data[1, :]
            self.larch_data.I0 = data[12, :]
            self.larch_data.transmission = data[11, :]
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "ELETTRA XAFS":
            self.larch_data.energy = data[0, :]
            self.larch_data.I0 = data[3, :]
            self.larch_data.transmission = data[2, :]
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "SLRI":
            self.larch_data.energy = data[0, :]
            self.larch_data.I0 = data[4, :]
            self.larch_data.transmission = data[3, :]
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "ESRF BM 23":
            self.larch_data.energy = data[0, :]*1000
            self.larch_data.I0 = data[2, :]
            self.larch_data.transmission = data[1, :]
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "SOLEIL ROCK":
            self.larch_data.energy = data[0, :]
            self.larch_data.mu = data[1, :]
        elif self.beamline == "SOLEIL SAMBA":
            self.larch_data.energy = data[0, :]
            self.larch_data.I0 = data[8, :]
            self.larch_data.transmission = data[6, :]
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "SLS":
            self.larch_data.energy = data[0, :]*1000
            self.larch_data.I0 = data[3, :]
            self.larch_data.transmission = data[2, :]
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "TU Berlin":
            self.larch_data.energy = data[0, :]
            self.larch_data.mu = data[1, :]
        elif self.beamline == "DELTA":
            self.larch_data.energy = data[0, :]
            self.larch_data.mu = data[1, :]
        
        ### check unit of energy, if value below 100 it is most likely keV
        ### --> change it to eV by multipying it with 1000
        if self.larch_data.energy[0] < 100:
            self.larch_data.energy *= 1000
        ### convert data to numpy array with [energy, mu]
        self.data = np.array([self.larch_data.energy, self.larch_data.mu])
        ### create raw plot
        self.create_raw_plot_base64()
    
    
    def load_hdf(self,):
        print("Will be implemented.")
        
        
    def create_raw_plot_base64(self, plot_data = False):
        ### define figures
        self.fig_raw_data = plt.figure("Preview Raw Data", figsize=(10, 6.25))
        self.fig_raw_data.clf()
        self.ax_raw_data = self.fig_raw_data.subplots()
        self.ax_raw_data.grid()
        major_ticks = np.arange(self.data[0,0], self.data[0,-1], 100)
        minor_ticks = np.arange(self.data[0,0], self.data[0,-1], 20)

        ### plot raw data
        self.ax_raw_data.plot(self.data[0], self.data[1],
                              label="Measurement",
                              color = "#003161")
        
        self.ax_raw_data.set_xlabel(r" Energy | eV")
        self.ax_raw_data.set_ylabel(r"$\mu (E)$ | a.u.")
        self.ax_raw_data.set_xlim(self.data[0,0], self.data[0,-1])
        self.ax_raw_data.legend(loc = 'best')
        self.ax_raw_data.set_xticks(major_ticks)
        self.ax_raw_data.set_xticks(minor_ticks, minor=True)
        if plot_data:
            self.fig_raw_data.canvas.draw()
            self.fig_raw_data.canvas.flush_events()
        buffer = io.BytesIO()
        self.fig_raw_data.savefig(buffer, format="jpeg")
        data = base64.b64encode(buffer.getbuffer()).decode("ascii")
        self.meta_data_dict["PreviewRawData"] = "data:image/jpeg;base64,{}".format(data)
