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
from larch.io import read_ascii, read_xdi

folder = '/home/frank/Doktorarbeit/DAPHNE/Measurement Data/SYNCHROTRON'
files = glob(folder+'/SOLARIS*.dat')

for file in files:
    test = read_ascii(file)
    name = file.split('/')[-1].replace('.dat','')
    print('working on ', name)
    fig = plt.figure(name)
    fig.clf()
    axes = fig.subplots(5,5)
    iterator = 0
    for row in axes:
        for i, ax in enumerate(row):
            if (iterator + i) < 23:
                # ax.plot(test.data[iterator+i])
                ax.plot(test.energy, test.data[iterator+i]/test.sr)
                ax.set_title(iterator+i)
        iterator += 5
    fig.show()
