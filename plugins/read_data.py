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

    def __init__(self, source):
        print('read_data class initialized')
        self.source = source
        self.supported_facilities = {"SYNCHROTRON" : ["CATACT KIT", 
                                                      "PETRA III Extension Beamline P65",
                                                      "Elettra", "SLRI", "BM 23 ESRF", 
                                                      "ROCK Soleil", "SAMBA Soleil",
                                                      "SLS", 
                                                      ],
                                     "LABORATORY" : ["TU Berlin",
                                                     ]
                                     }
        self.key_words = {"SYNCHROTRON" : {"CATACT KIT" : ["catexp",],
                                           "PETRA III Extension Beamline P65" : ["PETRA III Extension Beamline P65",],
                                           "Elettra" : ["Project Name:"],
                                           "SLRI" : ["BL8: X-ray Absorption Spectroscopy"],
                                           "BM 23 ESRF" : ["#ZapEnergy"],
                                           "ROCK Soleil" : ["Synchrotron SOLEIL"],
                                           "SAMBA Soleil" : ["# Energy, Theta, XMU, FLUO, REF, FLUO_RAW, I0, I1, I2, I3"],
                                           "SLS" : ["#posX	SAI01-MEAN	SAI02-MEAN"],
                                           },
                          "LABORATORY" : {"TU Berlin" : ["# Energies_eV"],
                                          }
                          }
        self.facility = None
    
    
    def extract_header(self, ):
        """
        Function to exctract data from the header

        Parameters
        ----------
         : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
    
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
        keyword is in the file. When succesful, the facility is stored and the
        specified load_data function is called.

        Returns
        -------
        None.

        """
        with open(self.data_path, 'r') as f:
            for line in f:
                for facility in self.supported_facilities[self.source]:
                    for keyword in self.key_words[self.source][facility]:
                        if keyword in line:
                            print('line with key word: ', line)
                            self.facility = facility
                            break
        if self.facility:
            print('facility found:\t', self.facility)
            self.load_data()
        else:
            print('no keyword found')
                
    
    def load_data(self,):
        """
        This function opens the data file and returns the data in the form of
        array([energy, mu])

        Returns
        -------
        numpy.array
            array([energy, mu])

        """
        if self.facility == "CATACT KIT":
            data = np.loadtxt(self.data_path, skiprows = 35)
            self.data = np.array([data[:, 0]*1000, np.log(data[:, 5] / data[:, 6])]).T
        elif self.facility == "PETRA III Extension Beamline P65":
            data = np.loadtxt(self.data_path, skiprows=45)
            self.data = np.array([data[:, 1], np.log(data[:, 11] / data[:, 12])]).T
        elif self.facility == "Elettra":
            data = np.loadtxt(self.data_path, skiprows=25)
            self.data = np.array([data[:, 0], np.log(data[:, 2] / data[:, 3])]).T
        elif self.facility == "SLRI":
            data = np.loadtxt(self.data_path, skiprows=20)
            self.data = np.array([data[:, 0], np.log(data[:, 3] / data[:, 4])]).T
        elif self.facility == "BM 23 ESRF":
            data = np.loadtxt(self.data_path, skiprows=20)
            self.data = np.array([data[:, 0]*1000, np.log(data[:, 1] / data[:, 2])]).T
        elif self.facility == "ROCK Soleil":
            data = np.loadtxt(self.data_path, skiprows=20)
            self.data = np.array([data[:, 0], data[:,1]]).T
        elif self.facility == "SAMBA Soleil":
            data = np.loadtxt(self.data_path, skiprows=5)
            self.data = np.array([data[:, 0], np.log(data[:, 6] / data[:, 8])]).T
        elif self.facility == "SLS":
            data = np.loadtxt(self.data_path, skiprows=5)
            self.data = np.array([data[:, 0]*1000, np.log(data[:, 2] / data[:, 3])]).T
        elif self.facility == "TU Berlin":
            data = np.loadtxt(self.data_path, skiprows=3)
            self.data = np.array([data[:, 0], data[:, 1]]).T
        
    
    def load_hdf(self,):
        print("Will be implemented soon. Stay tuned you awesome dude!")
                

