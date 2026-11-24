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
import re
from pathlib import Path
from types import SimpleNamespace
from plugins.selected_spectrum import calculate_spectrum
from plugins.column_labels import recover_column_labels
from plugins.text_table import read_text_table, suggest_columns
plt.ioff()
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["xtick.top"] = True
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["ytick.right"] = True
plt.rcParams["axes.grid.which"] = "both"


class ReadData(object):
    """
    Read numeric XAS text tables (.xdi, .dat, .txt, .spec and other text
    extensions) by content, and retain supported NeXus/HDF5 loading.
    """

    def __init__(self, source = "SYNCHROTRON", update_erange="",
                 scan_number = 0, verbose = False, column_selection=None, preview_columns=False):
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
            Zero-based position of the text scan/table. Repeated SPEC scan IDs
            are separate entries. The default is the first nonempty scan (0).
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
        self.column_selection = column_selection or None
        if self.column_selection and self.column_selection.get('scan') not in (None,''):
            self.scan_number=self.column_selection['scan']
        self.preview_columns = preview_columns
        # initialize dictionaries with supported beamlines and their specific
        # keywords by whom the beamline is identified. These are characteristic
        # for each file and has to be adapted when a change of syntax occurs
        # in the beamline datasets
        self.supported_beamlines = {"SYNCHROTRON" : ["CATACT KIT", 
                                                     "PETRA III Extension Beamline P64",
                                                     "PETRA III Extension Beamline P65",
                                                     "ELETTRA XAFS",
                                                     "SLRI",
                                                     "ESRF BM 23", 
                                                     "SOLEIL ROCK",#
                                                     "SOLEIL SAMBA",
                                                     "SLS",
                                                     "DELTA",
                                                     "SOLARIS",
                                                      ],
                                     "LABORATORY" : ["TU Berlin",
                                                     ]
                                     }
        self.beamline_key_words = {
            "SYNCHROTRON" : {
                "CATACT KIT" : ["catexp",],
                "PETRA III Extension Beamline P64" : ["##  0 - Position",],
                "PETRA III Extension Beamline P65" : ["PETRA III Extension Beamline P65",
                                                      "PETRA III P65"],
                "ELETTRA XAFS" : ["Project Name:"],
                "SLRI" : ["BL8: X-ray Absorption Spectroscopy"],
                "ESRF BM 23" : ["#ZapEnergy",
                                "eneenc   mu_trans   mu_fluo   mu_ref"],
                "SOLEIL ROCK" : ["Synchrotron SOLEIL",
                                 "rock-soleil"],
                "SOLEIL SAMBA" : ["#  Energy, Theta, XMU, FLUO, REF, FLUO_RAW, I0, I1, I2, I3"],
                "SLS" : ["#posX	SAI01-MEAN	SAI02-MEAN"],
                "DELTA" : ["#  created:"],
                "SOLARIS" : ['# C Acquisition started', '#C Acquisition started']
                },
            "LABORATORY" : {
                "TU Berlin" : ["#  Energies_eV"],
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
        # Integration fix: normalize string/Path inputs before using .suffix.
        # Original larch202530 behavior is preserved in _integration_archive.
        self.data_path = Path(data_path)
        self.data_type = self.data_path.suffix.lower()
        if self.data_type in ['.h5', '.hdf', '.hdf5', '.nxs'] or self._is_hdf5_file():
            self.load_hdf()
        else:
            self.read_out_file()

    def _is_hdf5_file(self):
        try:
            with self.data_path.open('rb') as data_file:
                return data_file.read(8) == b'\x89HDF\r\n\x1a\n'
        except OSError:
            return False

    def read_out_file(self,):
        """
        This function reads every line of the file and checks, if any known
        keyword is in the file. When succesful, the beamline is stored and the
        specified load_data function is called.
        """
        # resetting to default, clear all data
        self.reset_2_default()
        # Read the complete header and numeric table without a fixed row offset.
        table=read_text_table(self.data_path,scan=self.scan_number)
        self.larch_data=table
        self.meta_data_dict['File_reading']=table.read_info
        self.meta_data_dict['Scans']=table.scans
        self.meta_data_dict['Column_units']=table.column_units
        self.header = self.larch_data.header
        # now check the header for keywords for the specific beamlines
        source_order = [self.source] + [
            source for source in self.supported_beamlines if source != self.source
        ]
        for line in self.header:
            normalized_line = re.sub(r'#\s+#', '##', ' '.join(line.split()))
            for source in source_order:
                for beamline in self.supported_beamlines[source]:
                    for keyword in self.beamline_key_words[source][beamline]:
                        normalized_keyword = re.sub(r'#\s+#', '##', ' '.join(keyword.split()))
                        if normalized_keyword in normalized_line:
                            self.source = source
                            self.beamline = beamline
                            break
        # Preview raw columns before any beamline-specific signal assumptions.
        if self.preview_columns:
            self.data = None
            self.meta_data_dict['Column_selection_required'] = True
            self.extract_header()
            return
        # Explicit selections take precedence over beamline recipes.
        if self.column_selection:
            self.apply_column_selection()
            self.extract_header()
            self.finish_selected_spectrum()
            return
        # if a beamline was found, extract data
        if self.beamline:
            if self.verbose:
                print('beamline found:\t', self.beamline)
            self.extract_header()
            try:
                self.load_data()
            except (AttributeError,IndexError,KeyError) as exc:
                self.meta_data_dict['Legacy_mapping_note']='The older beamline recipe did not match this header; named columns were used.'
                self.prepare_named_spectrum()
        else:
            if self.verbose:
                print('no beamline found, going to numpy extraction mode')
            self.prepare_named_spectrum()


    def prepare_named_spectrum(self):
        choice=suggest_columns(self.larch_data.array_labels,self.beamline)
        if not choice['confident']:
            raise ValueError('The file was read, but its energy and absorption columns need confirmation. Choose numbered columns in Column selection and click Apply columns.')
        selection={key:choice[key] for key in ('energy','signal_a','signal_b','formula')}
        unit=self.larch_data.column_units[choice['energy']]
        self.data,metadata=calculate_spectrum(self.larch_data.data,self.larch_data.array_labels,selection,declared_energy_unit=unit)
        names=list(self.larch_data.array_labels)
        reference=next((names.index(label) for label in ['mu_ref','murefer','muref','reference_mu','reference'] if label in names),None)
        reference_selection=None
        if reference is not None:
            reference_selection=dict(selection,signal_a=reference,signal_b=reference,formula='raw')
        elif 'i1' in names and 'i2' in names:
            reference_selection=dict(selection,signal_a=names.index('i1'),signal_b=names.index('i2'),formula='log_ratio')
        elif 'ion1' in names and 'ion2' in names:
            reference_selection=dict(selection,signal_a=names.index('ion1'),signal_b=names.index('ion2'),formula='log_ratio')
        if reference_selection:
            ref_data,ref_meta=calculate_spectrum(self.larch_data.data,names,reference_selection,declared_energy_unit=unit)
            common,sample_index,reference_index=np.intersect1d(self.data[0],ref_data[0],return_indices=True)
            if len(common)<10: raise ValueError('Fewer than 10 matching finite sample/reference energies remain.')
            self.data=np.array([common,ref_data[1,reference_index],self.data[1,sample_index]])
            metadata['reference_input']=ref_meta
        else:
            metadata['reference_input']='Same selected signal; no separate reference channel was identified.'
        self.meta_data_dict['Automatic_mapping']=metadata
        self.extract_header()
        self.finish_selected_spectrum()


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
        To distinguish between sample and reference materials the content of the
        provided file is checked for facility specific key words. If only 1
        measurement column is found, the material is likely a reference. If 2 are
        detected, the reference and sample mu are extracted. The energy calibration
        is than applied to the reference mu.

        Returns
        -------
        numpy.array
            array([energy, mu_reference, mu_sample])
        """
        reference_sample_simultaneous = False  # keyword if sample and reference are measured simultaneously
        entries = [entry.lower() for entry in self.larch_data.array_labels]
        # SYNCHROTRON
        if self.beamline == "CATACT KIT":
            self.larch_data.energy = self.larch_data.energy
            self.larch_data.I0 = self.larch_data.ioni3
            self.larch_data.transmission = self.larch_data.ioni2
            self.larch_data.mu_ref = np.log(self.larch_data.ioni2/self.larch_data.ioni3)
            self.larch_data.mu = np.log(self.larch_data.ioni1/self.larch_data.ioni2)
            if np.corrcoef(self.larch_data.mu, self.larch_data.mu_ref)[0,1] < 0.8:
                self.larch_data.mu = self.larch_data.mu_ref

        elif self.beamline == "PETRA III Extension Beamline P64":
            raw_data = np.asarray(self.larch_data.data, dtype=float)
            p64_labels = list(getattr(self.larch_data, 'array_labels', []) or [])
            for line in self.header:
                match = re.match(r'^\s*#\s*#\s*(\d+)\s*-\s*(.+?)\s*$', line)
                if match:
                    index = int(match.group(1))
                    if index < raw_data.shape[0]:
                        while len(p64_labels) < raw_data.shape[0]:
                            p64_labels.append(f'col{len(p64_labels) + 1}')
                        p64_labels[index] = re.sub(
                            r'[^a-z0-9]+', '_', match.group(2).strip().lower()
                        ).strip('_')
            if len(p64_labels) == raw_data.shape[0]:
                self.larch_data.array_labels = p64_labels
            normalized_entries = [entry.lower().replace('-', '_') for entry in p64_labels]

            def p64_column(*names):
                for name in names:
                    if name in normalized_entries:
                        return raw_data[normalized_entries.index(name)]
                return None

            self.larch_data.energy = p64_column(
                'position', 'energy', 'energy_enc', 'mono_energy', 'photon_energy', 'e_enc'
            )
            if self.larch_data.energy is None:
                self.larch_data.energy = raw_data[0]

            i0 = p64_column('i0', 'incident', 'incident_intensity')
            i1 = p64_column('i1', 'it', 'itrans', 'transmission')
            i2 = p64_column('i2', 'iref', 'reference')
            processed_mu = p64_column('mu', 'xmu', 'mu_trans', 'normalized')
            with np.errstate(divide='ignore', invalid='ignore'):
                if processed_mu is not None:
                    self.larch_data.mu_ref = processed_mu
                    self.larch_data.mu = processed_mu
                elif i0 is not None and i1 is not None:
                    self.larch_data.mu = -np.log(i1 / i0)
                    self.larch_data.mu_ref = -np.log(i2 / i1) if i2 is not None else self.larch_data.mu.copy()
                elif raw_data.shape[0] >= 4:
                    self.larch_data.transmission = raw_data[1]
                    self.larch_data.I0 = raw_data[3]
                    self.larch_data.mu_ref = np.log(self.larch_data.transmission/self.larch_data.I0)
                    self.larch_data.mu = self.larch_data.mu_ref.copy()
                elif raw_data.shape[0] >= 2:
                    self.larch_data.mu_ref = raw_data[1]
                    self.larch_data.mu = raw_data[1]
                    self.meta_data_dict['Column_selection_required'] = True
                else:
                    raise ValueError('P64 text file does not contain a usable signal column')
        elif self.beamline == "PETRA III Extension Beamline P65":
            if "i0" in entries and "i1" in entries and "i2" in entries:
                reference_sample_simultaneous = True
                try:
                    self.larch_data.energy = self.larch_data.energy_enc
                except AttributeError as e:
                    self.larch_data.energy = self.larch_data.e_enc
                self.larch_data.mu_ref = self.larch_data.i1/self.larch_data.i2
                self.larch_data.mu = self.larch_data.i0/self.larch_data.i1
                # remove inf and nan
                self.larch_data.mu_ref = np.nan_to_num(self.larch_data.mu_ref, posinf=0)
                self.larch_data.mu = np.nan_to_num(self.larch_data.mu, posinf=0)
                # if only reference is measured check if the reference and sample
                # columns are switched by checking 
                # 1) vast values in mu_ref or mu
                # 2) by the std of the 1st derivative of the mu and mu_ref
                # and last resort, 3) check the pearson correlation and check if 
                # indeed sample and reference are measured simultaneously
                # 1)
                if len(self.larch_data.mu_ref[self.larch_data.mu_ref > 100]) > 5:
                    self.larch_data.mu_ref = self.larch_data.mu
                elif len(self.larch_data.mu[self.larch_data.mu > 100]) > 5:
                    self.larch_data.mu = self.larch_data.mu_ref
                # 2)
                if np.std(np.diff(self.larch_data.mu_ref[:len(self.larch_data.mu_ref)//2])) < 0.0005:
                    self.larch_data.mu_ref = self.larch_data.mu
                elif np.std(np.diff(self.larch_data.mu[:len(self.larch_data.mu)//2])) < 0.0005:
                    self.larch_data.mu = self.larch_data.mu_ref
                # 3)
                print(f"pearson of sample and reference: {np.corrcoef(self.larch_data.mu, self.larch_data.mu_ref)}")
                if 0 < np.corrcoef(self.larch_data.mu, self.larch_data.mu_ref)[0,1] < 0.8:
                    self.larch_data.mu = self.larch_data.mu_ref
                elif -0.8 < np.corrcoef(self.larch_data.mu, self.larch_data.mu_ref)[0,1] < 0:
                    self.larch_data.mu_ref = self.larch_data.mu
            if not reference_sample_simultaneous:
                if "mono_energy" in entries:
                    self.larch_data.energy = self.larch_data.mono_energy
                elif "energy_enc" in entries:
                    self.larch_data.energy = self.larch_data.energy_enc
                elif "e_enc" in entries:
                    self.larch_data.energy = self.larch_data.e_enc
                elif "energy" in entries:
                    self.larch_data.energy = self.larch_data.energy
                if "vfc03" in entries:
                    self.larch_data.I0 = self.larch_data.vfc03
                elif "i0" in entries and "i2" in entries:
                    self.larch_data.I0 = self.larch_data.i2
                if "vfc02" in entries:
                    self.larch_data.transmission = self.larch_data.vfc02
                elif "i2" in entries:
                    self.larch_data.transmission = self.larch_data.i0
                if "_ev" in entries:
                    self.larch_data.energy = self.larch_data.energy
                    self.larch_data.mu_ref = self.larch_data._ev
                    self.larch_data.mu = self.larch_data._ev
                elif "murefer" in entries:
                    self.larch_data.mu_ref = self.larch_data.i0/self.larch_data.irefer
                    self.larch_data.mu = self.larch_data.i0/self.larch_data.itrans
                    if np.corrcoef(self.larch_data.mu, self.larch_data.mu_ref)[0,1] < 0.8:
                        self.larch_data.mu = self.larch_data.mu_ref
                try:
                    self.larch_data.mu_ref = np.log(self.larch_data.transmission/self.larch_data.I0)
                    self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
                    if np.isnan(self.larch_data.mu).any() or np.isinf(self.larch_data.mu).any():
                        if self.verbose:
                            print("changing dataset, darn P65 always something special!")
                        self.larch_data.transmission = self.larch_data.i0
                        self.larch_data.I0 = self.larch_data.i1
                        self.larch_data.mu_ref = np.log(self.larch_data.transmission/self.larch_data.I0)
                        self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
                except:
                    if self.verbose:
                        print("no transmission data loaded")
        elif self.beamline == "ELETTRA XAFS":
            self.larch_data.energy = self.larch_data.data[0, :]
            self.larch_data.I0 = self.larch_data.data[3, :]
            self.larch_data.transmission = self.larch_data.data[2, :]
            self.larch_data.mu_ref = np.log(self.larch_data.data[6, :]/self.larch_data.data[7, :])
            self.larch_data.mu = np.log(self.larch_data.data[2, :]/self.larch_data.data[3, :])
        elif self.beamline == "SLRI":
            self.larch_data.energy = self.larch_data.data[0, :]
            self.larch_data.I0 = self.larch_data.data[4, :]
            self.larch_data.transmission = self.larch_data.data[3, :]
            self.larch_data.mu_ref = np.log(self.larch_data.transmission/self.larch_data.I0)
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "ESRF BM 23":
            if "zapenergy" in entries:
                self.larch_data.energy = self.larch_data.zapenergy
                self.larch_data.I0 = self.larch_data.data[2, :]
                self.larch_data.transmission = self.larch_data.data[1, :]
                self.larch_data.mu_ref = np.log(self.larch_data.transmission/self.larch_data.I0)
                self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
            elif "eneenc" in entries:
                self.larch_data.energy = self.larch_data.eneenc
                self.larch_data.mu_ref = self.larch_data.mu_ref
                self.larch_data.mu = self.larch_data.mu_trans
            
        elif self.beamline == "SOLEIL ROCK":
            # check if a reference was measured in parallel
            # this is determined via the keys mux (sample) and mus(reference)
            if "mux" in entries and "mus" in entries:
                reference_sample_simultaneous = True
                self.larch_data.mu_ref = self.larch_data.i1/self.larch_data.i2  # reference absorption
                self.larch_data.mu = self.larch_data.i0/self.larch_data.i1  # sample absorption
                self.larch_data.I0 = self.larch_data.i0
            elif "normalized" in entries:
                self.larch_data.mu_ref = self.larch_data.normalized
                self.larch_data.mu = self.larch_data.normalized
            elif "i0" in entries:
                self.larch_data.I0 = self.larch_data.i1
            if "vfc02" in entries:
                self.larch_data.transmission = self.larch_data.vfc02
            elif "i1" in entries:
                self.larch_data.transmission = self.larch_data.i0
            if "shifted" in entries:
                self.larch_data.energy = self.larch_data.shifted
                self.larch_data.mu_ref = np.abs(self.larch_data.normalized)
                self.larch_data.mu = np.abs(self.larch_data.normalized)
            if not reference_sample_simultaneous:
                try:
                    self.larch_data.mu_ref = np.log(self.larch_data.transmission/self.larch_data.I0)
                    self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
                except:
                    if self.verbose:
                        print("no transmission data loaded")
        elif self.beamline == "SOLEIL SAMBA":
            self.larch_data.energy = self.larch_data.data[0, :]
            self.larch_data.I0 = self.larch_data.data[8, :]
            self.larch_data.transmission = self.larch_data.data[6, :]
            self.larch_data.mu_ref = np.log(self.larch_data.transmission/self.larch_data.I0)
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "SLS":
            self.larch_data.energy = self.larch_data.data[0, :]
            self.larch_data.I0 = self.larch_data.data[3, :]
            self.larch_data.transmission = self.larch_data.data[2, :]
            self.larch_data.mu_ref = np.log(self.larch_data.transmission/self.larch_data.I0)
            self.larch_data.mu = np.log(self.larch_data.transmission/self.larch_data.I0)
        elif self.beamline == "DELTA":
            self.larch_data.energy = self.larch_data.data[0, :]
            self.larch_data.mu_ref = self.larch_data.data[1, :]
            self.larch_data.mu = self.larch_data.data[1, :]
        elif self.beamline == "SOLARIS":
            self.larch_data.mu_ref = self.larch_data.d2/self.larch_data.sr
            self.larch_data.mu = self.larch_data.d2/self.larch_data.sr
        
        # LABORATORY
        elif self.beamline == "TU Berlin":
            self.larch_data.energy = self.larch_data.data[0, :]
            self.larch_data.mu_ref = self.larch_data.data[1, :]
            self.larch_data.mu = self.larch_data.data[1, :]

        if self.column_selection:
            self.apply_column_selection()
            self.finish_selected_spectrum()
            return
        
        # check unit of energy, if value below 100 it is most likely keV
        # --> change it to eV by multipying it with 1000
        self.larch_data.energy = self.keV2eV(self.larch_data.energy)
        # sort the energy to be strictly increasing (for scipy spline in larch.autobk)
        energy_sorted_idx = self.larch_data.energy.argsort()
        self.larch_data.energy = self.larch_data.energy[energy_sorted_idx]
        self.larch_data.mu_ref = self.larch_data.mu_ref[energy_sorted_idx]
        self.larch_data.mu = self.larch_data.mu[energy_sorted_idx]
        diff_E = np.diff(self.larch_data.energy)
        mean_diff = diff_E.mean()
        remove_idx = np.where(diff_E>(mean_diff/10))
        # convert NaN to 0
        self.larch_data.energy = np.nan_to_num(self.larch_data.energy, posinf=0,
                                               neginf=0)
        self.larch_data.mu_ref = np.nan_to_num(self.larch_data.mu_ref, posinf=0,
                                            neginf=0)
        self.larch_data.mu = np.nan_to_num(self.larch_data.mu, posinf=0,
                                            neginf=0)
        
        if self.beamline == "PETRA III Extension Beamline P65":
            self.larch_data.energy = self.larch_data.energy[remove_idx]
            self.larch_data.mu_ref = self.larch_data.mu_ref[remove_idx]
            self.larch_data.mu = self.larch_data.mu[remove_idx]
        
        # convert data to numpy array with [energy, mu]
        self.data = np.array([self.larch_data.energy,
                              self.larch_data.mu_ref,
                              self.larch_data.mu])
        # set e-range
        self.meta_data_dict['E_range_min'] = np.round(self.data[0,0], decimals=1)
        self.meta_data_dict['E_range_max'] = np.round(self.data[0,-1], decimals=1)
        # create raw plot
        self.create_raw_plot_base64()

    def apply_column_selection(self):
        units=getattr(self.larch_data,'column_units',[])
        energy=self.column_selection.get('energy')
        try: index=int(energy)
        except (TypeError,ValueError):
            matches=[i for i,label in enumerate(self.larch_data.array_labels) if str(label).lower()==str(energy).lower()]
            index=matches[0] if len(matches)==1 else -1
        unit=units[index] if 0<=index<len(units) else None
        self.data, metadata = calculate_spectrum(
            self.larch_data.data, self.larch_data.array_labels, self.column_selection,declared_energy_unit=unit)
        metadata['scan_index']=int(self.scan_number or 0)
        metadata['scan_label']=getattr(self.larch_data,'read_info',{}).get('scan_label')
        self.larch_data.energy = self.data[0]
        self.larch_data.mu_ref = self.data[1]
        self.larch_data.mu = self.data[2]
        self.meta_data_dict['Column_selection'] = metadata

    def finish_selected_spectrum(self):
        self.meta_data_dict['E_range_min'] = float(self.data[0, 0])
        self.meta_data_dict['E_range_max'] = float(self.data[0, -1])
        self.create_raw_plot_base64()

    def load_hdf(self,):
        """
        Read ESRF HDF5 and generic NeXus/HDF5 XAS files. Numeric one-dimensional
        datasets sharing the energy-array length are exposed to the column
        preview so that unfamiliar beamline layouts can be selected safely.
        """
        self.reset_2_default()
        self.header = []
        datasets = {}
        metadata = []

        with h5py.File(self.data_path, 'r') as hdf_file:
            def collect(name, item):
                if isinstance(item, h5py.Dataset):
                    if item.dtype.kind in 'iuf' and item.size >= 10:
                        values = np.asarray(item[()]).squeeze()
                        if values.ndim == 1:
                            datasets[name] = values.astype(float)
                for key, value in item.attrs.items():
                    metadata.append(f'{name}@{key}: {value}')

            hdf_file.visititems(collect)
            for key, value in hdf_file.attrs.items():
                metadata.append(f'@{key}: {value}')

        if not datasets:
            raise ValueError('No numeric one-dimensional scan datasets were found in the HDF5/NeXus file')

        normalized = {
            path: Path(path).name.lower().replace('-', '_').replace(' ', '_')
            for path in datasets
        }
        energy_aliases = (
            'energy_cenc', 'energy_enc', 'mono_energy', 'photon_energy',
            'energy', 'e_enc', 'energies_ev', 'energy_ev'
        )

        def find_dataset(aliases, length=None):
            for alias in aliases:
                for path, name in normalized.items():
                    if name == alias and (length is None or len(datasets[path]) == length):
                        return path
            for alias in aliases:
                for path, name in normalized.items():
                    if alias in name and (length is None or len(datasets[path]) == length):
                        return path
            return None

        energy_path = find_dataset(energy_aliases)
        if energy_path is None:
            raise ValueError(
                'No energy dataset was recognized in this HDF5/NeXus file. '
                'Expected a dataset named energy, energy_enc, mono_energy, or photon_energy.'
            )

        point_count = len(datasets[energy_path])
        compatible_paths = [
            path for path, values in datasets.items() if len(values) == point_count
        ]
        if len(compatible_paths) < 2:
            raise ValueError('The HDF5/NeXus energy dataset has no matching one-dimensional signal dataset')

        labels = compatible_paths
        raw_data = np.array([datasets[path] for path in labels])
        self.larch_data = SimpleNamespace(array_labels=labels, data=raw_data)
        self.header = metadata
        self.meta_data_dict['Header'] = metadata
        self.meta_data_dict['Header_str'] = '\n'.join(metadata)
        header_text = ' '.join(metadata + list(datasets)).lower()
        if 'p64' in header_text or 'petra iii extension beamline p64' in header_text:
            self.beamline = 'PETRA III Extension Beamline P64'

        if self.preview_columns:
            self.data = None
            self.meta_data_dict['Column_selection_required'] = True
            return

        if self.column_selection:
            self.apply_column_selection()
            self.finish_selected_spectrum()
            return
        else:
            energy = datasets[energy_path]
            mu_ref_path = find_dataset(('mu_trans_ref', 'mu_ref', 'muref', 'reference_mu'), point_count)
            mu_path = find_dataset(('mu_trans', 'mu', 'xmu', 'normalized'), point_count)
            i0_path = find_dataset(('i0', 'incident', 'incident_intensity'), point_count)
            i1_path = find_dataset(('i1', 'itrans', 'transmission'), point_count)
            i2_path = find_dataset(('i2', 'iref', 'reference'), point_count)

            with np.errstate(divide='ignore', invalid='ignore'):
                if mu_ref_path or mu_path:
                    mu_ref = datasets[mu_ref_path or mu_path]
                    mu = datasets[mu_path or mu_ref_path]
                elif i0_path and i1_path:
                    mu = -np.log(datasets[i1_path] / datasets[i0_path])
                    mu_ref = (
                        -np.log(datasets[i2_path] / datasets[i1_path])
                        if i2_path else mu.copy()
                    )
                else:
                    signal_path = next(path for path in compatible_paths if path != energy_path)
                    mu_ref = datasets[signal_path]
                    mu = datasets[signal_path]
                    self.meta_data_dict['Column_selection_required'] = True

        energy = self.keV2eV(np.asarray(energy, dtype=float))
        mu_ref = np.asarray(mu_ref, dtype=float)
        mu = np.asarray(mu, dtype=float)
        valid = np.isfinite(energy) & np.isfinite(mu_ref) & np.isfinite(mu)
        if np.count_nonzero(valid) < 10:
            raise ValueError('The selected HDF5/NeXus datasets contain fewer than 10 finite points')
        order = np.argsort(energy[valid])
        self.data = np.array([energy[valid][order], mu_ref[valid][order], mu[valid][order]])
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
        self.read_out_file()


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
                mu_ref = self.data[1]
                mu_ref = mu_ref[self.E_range_min <= energy]
                mu = self.data[2]
                mu = mu[self.E_range_min <= energy]
                energy = energy[self.E_range_min <= energy]
                mu_ref = mu_ref[self.E_range_max >= energy]
                mu = mu[self.E_range_max >= energy]
                energy = energy[self.E_range_max >= energy]
                self.data = np.array([energy, mu_ref, mu])
            except (TypeError,AttributeError):
                if self.verbose:
                    print("Update of e-range not possible!")
        if self.data.shape[1] < 10:
            raise ValueError('The selected energy range contains fewer than 10 points')
        if not np.all(np.isfinite(self.data)):
            raise ValueError('The spectrum contains invalid values')
        #  define figures
        self.fig_raw_data = plt.figure(figsize=(10, 6.25))
        self.fig_raw_data.clf()
        self.ax_raw_data = self.fig_raw_data.subplots()
        self.ax_raw_data.grid()
        # A mistaken column/unit choice must not create millions of tick artists.
        span=float(self.data[0,-1]-self.data[0,0])
        tick_step=max(100.0,100.0*np.ceil(span/4000.0))
        major_ticks = np.arange(self.data[0,0], self.data[0,-1], tick_step)
        minor_ticks = np.arange(self.data[0,0], self.data[0,-1], tick_step/5)

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
        print("""|¯¯¯¯¯|¯¯¯¯¯|¯¯¯¯¯|¯¯¯¯¯|
        |\|/          (__)      |
        |     `\------(oo)      |
        |       ||    (__) <(mu)|
        |       ||w--||     \|/ |
        |   \|/                 |
        |¯¯¯¯¯|¯¯¯¯¯|¯¯¯¯¯|¯¯¯¯¯|
        QC succesfully performed""")


# Backward compatibility for older branches and external callers.
# v_beta/updatedQC/Hotfix/master imported the historical lowercase class name.
read_data = ReadData
