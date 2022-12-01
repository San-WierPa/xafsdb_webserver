#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 15:19:22 2021

@author: frank
"""
import json
import os


criteria = {'SYNCHROTRON': {'ABSORPTION' : {'RAW' : {'edge step' : {'min' : 0.5,  # alias: edge jump 
                                                                            'max' : 2.,
                                                                            'unit' : '1',
                                                                            'documentation' : 'height of the detected edge step'},
                                                              'k max' : {'min' : 15.,
                                                                         'max' : 20.,
                                                                         'unit' : '1/angstrom',
                                                                         'documentation' : 'considered angular wavenumber'},
                                                              'noise' : {'min' : 0, ### not that clear, depends on method, Abhijeet will "figure it out"
                                                                         'max' : 0.1, ### further discussion needed --> research methods define criteria (example SNR)
                                                                         'unit' : '1',
                                                                         'documentation' : 'noise of the measurement'},
                                                              'energy resolution' : {'min' : 0.2,
                                                                                     'max' : 2.,
                                                                                     'unit' : 'eV',
                                                                                     'documentation' : 'energy resolution of the measured spectrum in eV'},},
                                           'PROCESSED' : {'amplitude reduction factor' : {'Z-ranges' : {'[10,40[' : {'min' : 0.7,
                                                                                                                     'max' : 1.},
                                                                                                        '[40,80[' : {'min' : 0.7, 
                                                                                                                     'max' : 1.},},
                                                                                          'unit' : '1',
                                                                                          'documentation' : 'amplitude factor from the processed spectrum'},
                                                          },
                                            },
                            },
            ### Laboratory values are only blind values. No decision up to now
            'LABORATORY': {'ABSORPTION' : {'RAW' : {'edge step' : {'min' : 0.5,  # alias: edge jump 
                                                                                        'max' : 2.,
                                                                                        'unit' : '1',
                                                                                        'documentation' : 'height of the detected edge step'},
                                                             'k max' : {'min' : 10.,
                                                                        'max' : 20.,
                                                                        'unit' : '1/angstrom',
                                                                        'documentation' : 'considered angular wavenumber'},
                                                             'noise' : {'min' : 0, ### not that clear, depends on method, Abhijeet will "figure it out"
                                                                        'max' : 0.2, ### further discussion needed --> research methods define criteria (example SNR)
                                                                        'unit' : '1',
                                                                        'documentation' : 'noise of the measurement'},
                                                             'energy resolution' : {'min' : 0.2,
                                                                                    'max' : 2.,
                                                                                    'unit' : 'eV',
                                                                                    'documentation' : 'energy resolution of the measured spectrum in eV'},},
                                           'PROCESSED' : {'amplitude reduction factor' : {'Z-ranges' : {'[10,40[' : {'min' : 0.7,
                                                                                                                     'max' : 1.},
                                                                                                        '[40,80[' : {'min' : 0.7, 
                                                                                                                     'max' : 1.},},
                                                                                          'unit' : '1',
                                                                                          'documentation' : 'amplitude factor from the processed spectrum'},
                                                          },
                                           },
                           },
            }

criteria_path = os.path.abspath(os.path.curdir)+'/Criteria.json'
with open(criteria_path, 'w') as tofile:
    json.dump(criteria, fp = tofile, indent = 4,
              ensure_ascii = False)
