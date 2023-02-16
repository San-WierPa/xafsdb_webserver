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

    def __init__(
        self,
    ):
        pass

    def load_xdi(self, path):
        """
        load a xdi file

        Parameters
        ----------
        path : str
            absolute path to the xdi file.

        Returns
        -------
        array([energy, mu])
        """

        data = np.loadtxt(path, skiprows=42)
        return np.array([data[:, 1], np.log(data[:, 11] / data[:, 12])]).T

    def load_dat(self, path):
        """
        load a dat file

        Parameters
        ----------
        path : str
            absolute path to the dat file.

        Returns
        -------
        array([energy, mu])
        """

        data = np.loadtxt(path, skiprows=1)
        return np.array([data[:, 0], data[:, 1]]).T
