# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 19:00:31 2021

@author: PTK
ReadMGFSpectrum
"""



class ReadMGFSpectrum:
    def __init__(self):
        """ For reading of MGF files and to extract all information: spectrum id,
            ms1 scan, retention time, precursor m/z, charge and intensity, 
            fragmentation method, fragment masses, charge and intensity """
        pass
    
    def load_file(self, file_name: str): 
        """ load mgf file """
        self.file_data = open(file_name,"r").read()
        self.spectra_list = self.file_data.split("BEGIN IONS")[1:]   
        self.number_of_spectra = len(self.spectra_list)
        return self.spectra_list
    

    def _get_value_from_mgf(self, line: int):
        """ returns value of mgf-file """
        return line.split("=")[1]
    
    def read_spectrum(self, index: int, deconv_alg: str = "MSalign"):
        """
        extract info from a single spectrum

        Parameters
        ----------
        index : Int
            Index of spectrum in mgf file.
        deconv_alg : str, optional
            Used deconvolution algorithm. The default is "".

        Returns
        -------
        None.
            initialize extracted information from single spectrum

        """
        # msalign
        spectrum = self.spectra_list[index]
        spectrum_lines = spectrum.splitlines()
        if deconv_alg == "MSalign":
            self.id_ = spectrum_lines[0]
            self.ms1_scan = self._get_value_from_mgf(spectrum_lines[1])
            self.rt = self._get_value_from_mgf(spectrum_lines[2])
            self.fragmentation = self._get_value_from_mgf(spectrum_lines[3])
            self.ms1_id = self._get_value_from_mgf(spectrum_lines[4])
            self.ms2_id = self._get_value_from_mgf(spectrum_lines[5])
            self.precursor_mz = self._get_value_from_mgf(spectrum_lines[6])
            self.precursor_charge = self._get_value_from_mgf(spectrum_lines[7])
            self.precursor_mass = self._get_value_from_mgf(spectrum_lines[8])
            self.precursor_intensity = self._get_value_from_mgf(spectrum_lines[9])
            self.fragment_mass_list = []
            self.fragment_intensity_list = []
            self.fragment_charge_list = []
            for i in spectrum_lines[11:-2]:
                mass, intensity, charge = i.split("\t")
                self.fragment_mass_list.append(float(mass))
                self.fragment_intensity_list.append(float(intensity))
                self.fragment_charge_list.append(int(charge)) 
                
        if deconv_alg == "ProMEX":
            pass

            
        
