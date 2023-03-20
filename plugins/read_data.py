#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:33:49 2020

@author: Frank Foerste
ffoerste@physik.tu-berlin.de
"""

##############################################################################
import numpy as np

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
                                                      "ELETTTRA XAFS", "SLRI", "ESRF BM 23", 
                                                      "SOLEIL ROCK", "SOLEIL SAMBA",
                                                      "SLS", "DELTA",
                                                      ],
                                     "LABORATORY" : ["TU Berlin",
                                                     ]
                                     }
        self.key_words = {"SYNCHROTRON" : {"CATACT KIT" : ["catexp",],
                                           "PETRA III Extension Beamline P65" : ["PETRA III Extension Beamline P65",],
                                           "ELETTTRA XAFS" : ["Project Name:"],
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
        self.beamline = None ### variable to determine if a beamline was matched
        self.header_extraction = False ### variable set True if header of file should be extracted
        self.meta_data_dict = {}
    
    def extract_header(self, data_path):
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
        self.header_extraction = True
        ### determine beamline
        self.process_data(data_path = data_path)
        ### fill all the meta data contained in the files provided by the facilities
        ### into the dictionary
        self.meta_data_dict = {}
        self.meta_data_dict['Beamline'] = self.beamline
        coll_code = ''
        if self.beamline == "CATACT KIT":
            self.meta_data_dict['Facility'] = 'KIT Light Source'
            with open(data_path, 'r') as f:
                for line in f:
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
            with open(data_path, 'r') as f:
                for line in f:
                    line = line.replace('\n','')
                    if 'Project Name' in line: self.meta_data_dict["Coll.code"] = line.split()[-1]
            ### no further needed (as for 20230314) meta data in file
        elif self.beamline == "SLRI":
            self.meta_data_dict['Facility'] = "SLRI"
            with open(data_path, 'r') as f:
                for line in f:
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
            with open(data_path, 'r') as f:
                for line in f:
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
                      "reference": "Reference",}
        ### disable header extraction mode
        self.header_extraction = False
        print(self.meta_data_dict)
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
        print("data_path from process_data:", data_path)
        self.data_type = self.data_path.split('.')[-1]
        #print("self.data_type from process_data:", self.data_type)
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
        with open(self.data_path, 'r') as f:
            for line in f:
                for beamline in self.supported_beamlines[self.source]:
                    for keyword in self.key_words[self.source][beamline]:
                        if keyword in line:
                            # print('line with key word: ', line)
                            self.beamline = beamline
                            break
        if self.beamline:
            # print('beamline found:\t', self.beamline)
            if not self.header_extraction:
                self.load_data()
        else:
            print('no beamline found, going to numpy extraction mode')
            self.data = np.loadtxt(self.data_path)
                
    
    def load_data(self,):
        """
        This function opens the data file and returns the data in the form of
        array([energy, mu])

        Returns
        -------
        numpy.array
            array([energy, mu])

        """
        if self.beamline == "CATACT KIT":
            data = np.loadtxt(self.data_path, skiprows = 35)
            self.data = np.array([data[:, 0]*1000, np.log(data[:, 5] / data[:, 6])]).T
        elif self.beamline == "PETRA III Extension Beamline P65":
            data = np.loadtxt(self.data_path, skiprows=45)
            self.data = np.array([data[:, 1], np.log(data[:, 11] / data[:, 12])]).T
        elif self.beamline == "Elettra":
            data = np.loadtxt(self.data_path, skiprows=25)
            self.data = np.array([data[:, 0], np.log(data[:, 2] / data[:, 3])]).T
        elif self.beamline == "SLRI":
            data = np.loadtxt(self.data_path, skiprows=20)
            self.data = np.array([data[:, 0], np.log(data[:, 3] / data[:, 4])]).T
        elif self.beamline == "ESRF BM 23":
            data = np.loadtxt(self.data_path, skiprows=20)
            self.data = np.array([data[:, 0]*1000, np.log(data[:, 1] / data[:, 2])]).T
        elif self.beamline == "SOLEIL ROCK":
            data = np.loadtxt(self.data_path, skiprows=20)
            self.data = np.array([data[:, 0], data[:,1]]).T
        elif self.beamline == "SOLEIL SAMBA":
            data = np.loadtxt(self.data_path, skiprows=5)
            self.data = np.array([data[:, 0], np.log(data[:, 6] / data[:, 8])]).T
        elif self.beamline == "SLS":
            data = np.loadtxt(self.data_path, skiprows=5)
            self.data = np.array([data[:, 0]*1000, np.log(data[:, 2] / data[:, 3])]).T
        elif self.beamline == "TU Berlin":
            data = np.loadtxt(self.data_path, skiprows=3)
            self.data = np.array([data[:, 0], data[:, 1]]).T
        
    
    def load_hdf(self,):
        print("Will be implemented soon. Stay tuned you awesome dude!")
