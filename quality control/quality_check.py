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
from larch import xafs
import json
from larch import Group
# from larch.io import read_ascii
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
##############################################################################
### define ###
##############################################################################


class check_quality(object):
    """ 
    This class implements the automated checkers for the quality criteria
    of XAFS measurements
    """
    def __init__(self, quality_criteria_json):
        print('quality criteria function initialized')
        with open(quality_criteria_json, 'r') as f:
            self.quality_criteria = json.load(f)
            
        self.fig_data = plt.figure('processed data')
        self.fig_data.clf()
        self.ax_data = self.fig_data.subplots()
        self.ax_data.grid()
        
        self.fig_k = plt.figure('k')
        self.fig_k.clf()
        self.ax_k = self.fig_k.subplots()
        self.ax_k.grid()
        
    
    
    def load_data(self,  measurement_data, 
                  source = 'SYNCHROTRON', 
                  mode = 'ABSORPTION',
                  processed = 'RAW', 
                  plot = True):
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
        self.plot = plot
        self.source = source
        self.mode = mode
        self.processed = processed
        self.quality_criteria = self.quality_criteria[self.source][self.mode][self.processed]
        self.data = Group()
        self.data.energy = measurement_data[:,0]
        self.data.mu = measurement_data[:,1]
        
    
    def preprocess_data(self,):
        """
        This function preprocesses the data, finds the edge, fits the pre and post
        edge.
        """
        edge = xafs.find_e0(self.data.energy, self.data.mu, group = self.data)
        # index = np.where(self.data.energy == edge)
        # self.data.energy = self.data.energy[index[0][0]-550:]
        # self.data.mu = self.data.mu[index[0][0]-550:]
        # index = np.where(self.data.energy == edge)[0][0]
        ### calculate the edge position
        xafs.pre_edge(energy = self.data.energy,
                      mu = self.data.mu,
                      e0 = self.data.e0,
                      group = self.data,
                      pre1 = -140,
                       pre2 = -10,
                      make_flat = True,
                      nvict = 3
                      )  
        ### estimate pre and post edge
        xafs.autobk(energy = self.data.energy, 
                    mu = self.data.mu,
                    group = self.data)
        
        xafs.xftf(k = self.data.k, 
                  chi = self.data.chi,
                  group = self.data)
                  
                  
        ### estimate noise
        # xafs.estimate_noise(k = self.data.k,
        #                     chi = self.data.chi,
        #                     group = self.data,
        #                     )
        return self.data
    
    
    def plot_results(self, ):
        ### plot data
        self.ax_data.plot(self.data.energy, self.data.mu, label = 'measurement edge scan')
        self.ax_data.plot(self.data.e0, self.data.mu[np.where(self.data.e0 == self.data.energy)], 'r*', label = 'edge position')
        self.ax_data.plot(self.data.energy, self.data.pre_edge, label = 'pre edge estimation')
        self.ax_data.plot(self.data.energy, self.data.post_edge, label = 'post edge estimation')
        self.ax_data.plot(self.data.energy, self.data.flat, label = 'flattened normed edge scan')
        self.ax_data.set_xlabel('energy | keV')
        self.ax_data.set_ylabel('absorption | a.u.')
        self.ax_data.set_xlim(self.data.energy[0], self.data.energy[-1])
        self.ax_data.legend()
        
        self.ax_k.plot(self.data.k, self.data.chi, label = 'k')
        self.ax_k.set_xlabel(u'\u03c7(k) | \u212b⁻¹')
        self.ax_k.set_ylabel('k\u03c7(k) | a.u.')
        self.ax_k.set_xlim(self.data.k[0], self.data.k[-1])
        self.ax_k.legend()
        
        
    def check_edge_step(self,):
        """
        this function automatically evaluates the edge step of the given data
        """
        if self.quality_criteria['edge step']['min'] <= self.data.edge_step <= self.quality_criteria['edge step']['max']:
            print('\u2705 edge step of good quality: ', self.data.edge_step)
            return True
        else:
            print("\u274e edge step doesn't meet standards: ", self.data.edge_step)
            return False
        
        
    def check_energy_resolution(self,):
        """
        this function automatically evaluates the energy resolution of the 
        given data
        """
        self.data.energy_resolution = self.data.energy[1]-self.data.energy[0]
        if self.quality_criteria['energy resolution']['min'] <= self.data.energy_resolution <= self.quality_criteria['energy resolution']['max']:
            print('\u2705 energy resolution of good quality: ', self.data.energy_resolution, 'eV')
            return True
        else:
            print("\u274e energy resolution doesn't meet standards: ", self.data.energy_resolution, 'eV')
            return False
        
        
    def check_k(self,):
        """
        this function automatically evaluates the k range of the given data
        """
        if self.quality_criteria['k max']['min'] <= self.data.k[-1] <= self.quality_criteria['k max']['max']:
            print(u'\u2705 k max of good quality: ', self.data.k[-1], u"\u212b⁻¹")
            return True
        else:
            print(u"\u274e k max doesn't meet standards: ", self.data.k[-1], u"\u212b⁻¹")
            return False
        
    
    def estimate_noise(self,):
        """
        this function automatically estimates the noise in the k regime of 
        the given data
        """
        
        if self.quality_criteria['noise']['min'] <= self.data.k[-1] <= self.quality_criteria['noise']['max']:
            print(u'\u2705 k max of good quality: ', self.data.k[-1], u"\u212b⁻¹")
            return True
        else:
            print(u"\u274e k max doesn't meet standards: ", self.data.k[-1], u"\u212b⁻¹")
            return False
        
    
    def create_data_json(self,):
        data={"owner_group":"Technische Universität Berlin",
              "access_groups":"None",
              "creation_location":"Berlin, Germany", #added manually to openapi.json (using https://editor.swagger.io/)
              "principal_investigator":"Sebastian Praetz", #added manually to openapi.json
              "dataset_name":"test " + datetime.now().strftime("%Y-%m-%d-%H_%M_%S"),
              "type":"raw",
              "is_published":False,
              "creation_time":str(datetime.now().isoformat()),
              "source_folder":"None",
              "owner":"None",
              "contact_email":"ffoerste@physik.tu-berlin.de",
              "scientific_metadata":{"energy": {"value": list(self.data.energy), "unit": "eV"},
                                     "mu": {"value": list(self.data.mu), "unit": "a.u."},
                                     "source": "LABORATORY",
                                     "mode": "ABSORPTION",
                                     "processed": "RAW",}
              }
        with open(os.path.abspath(os.path.curdir)+'/example data/LABORATORY/evaluatiob.json', 'w') as tofile: ### !TODO path to be given to class
            json.dump(data, tofile,
                      indent = 4,
                      ensure_ascii = False)
        
### define data input
cq_json = os.path.abspath(os.path.curdir)+'/Criteria.json'

folder = os.path.abspath(os.path.curdir)+'/example data/LABORATORY/'
files = glob(folder+'*.dat')
files = [os.path.abspath(os.path.curdir)+'/example data/LABORATORY/Co 5 mu.dat']

### !TODO cut spectra
### 10 % pre edge and 40% post edge for laboratory (EXAFS 600 eV)

for file in files:
    qc_list = []
    meas_data = np.loadtxt(file, skiprows = 1)
    cq = check_quality(quality_criteria_json=cq_json)
    cq.load_data(meas_data)
    data = cq.preprocess_data()
    cq.plot_results()
    qc_list.append(cq.check_edge_step())
    qc_list.append(cq.check_energy_resolution())
    qc_list.append(cq.check_k())
    # if all(qc_list):
    #     cq.create_data_json()
    
        
