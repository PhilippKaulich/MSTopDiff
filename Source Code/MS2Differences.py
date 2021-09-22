# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 09:27:54 2021

@author: PTK
MS2Differences
"""


from Histogram import Histogram
from Settings import Settings
import ReadMGFSpectrum
import DataStructure


class MS2Differences():
    def __init__(self):
        """ Initialization """
        self.Histogram = Histogram()
        self.Data = DataStructure.DataMS2()
                                                                               
    def load_file(self, file_name: str) -> None:
        """ Initialize self.file_name
            file_name:Filename of analyze MS2 deconvoluted data """
        self.file_name: str = file_name
        
        
    def createHistogram(self, values: list, intensities1: list = [], 
                intensities2: list = [], 
                bin_size: float = Settings.deltamass_bin_size_ms2,  
                plot_options: dict = Settings.plot_options_histogram_ms2) -> None:
        """ creates histogram plots, parameter see Histogram """
        self.Data.Results.histogram = self.Histogram.plot_delta_mass(values, 
                                     intensities1, 
                                     intensities2,
                                     bin_size, plot_options)    



    def _calculate_mass_differences(self, mass_list: list, intensity_list: list, 
        diff_min: int = 0, diff_max: int = 
        Settings.deltamass_mass_max_ms2) -> [list, list, list, list]:
        """
        Calculates all possible differences of masses in list l and returns
        mass difference list and intensity-based difference lists of higher
        and lower masses. 

        Parameters
        ----------
        l : list
            Mass list.
        i : list
            Intensity list.
        diff_min : int, optional
            Minimal mass difference that is considered. The default is 0.
        diff_max : int, optional
            Maximal mass difference that is considered. The default is 1000.

        Returns
        -------
        [list, list, list]
            difference_list : difference list
            intensity_list  : Intensity-based differece list (sum abundance
                                            of higher lower mass feature)
            intensity_list_mass_low : Intensity-based difference list of lower
                mass feature
            intensity_list_mass_high : Intensity-based difference list of 
                higher mass feature
        """
        difference_list: list = []
        hist_intensity_list: list = []
        hist_intensity_list_mass_low: list = []
        hist_intensity_list_mass_high: list = []
        list_length = len(mass_list)
        for index1 in range(list_length):
            for index2 in range(index1+1, list_length):
                mass1 = mass_list[index1]
                mass2 = mass_list[index2]
                intensity1 = intensity_list[index1]
                intensity2 = intensity_list[index2]
                mass_diff = abs(mass2 - mass1)
                # Filter: mass_difference 
                if mass_diff >= diff_min and mass_diff <= diff_max:  
                    difference_list.append(mass_diff)
                    hist_intensity_list.append(intensity1 + intensity2)
                    hist_intensity_list_mass_low.append(intensity2 if mass1 > mass2 
                                                   else intensity1)
                    hist_intensity_list_mass_high.append(intensity1 if mass1 > mass2 
                                                    else intensity2)
        return difference_list, hist_intensity_list, hist_intensity_list_mass_low, hist_intensity_list_mass_high
                



    def calculateDifferences(self):
        """ Calculates all mass differences for each spectra """
        currentData = DataStructure.DataMS2()
        MS2_scans = ReadMGFSpectrum.ReadMGFSpectrum()
        MS2_scans.load_file(self.file_name)
        print ("Number of spectra:", MS2_scans.number_of_spectra)
        for index in range(MS2_scans.number_of_spectra):
            MS2_scans.read_spectrum(index)
            if index % 1000 == 0: print (index, "Spektren eingelesen")
            mass_differences = self._calculate_mass_differences( \
               MS2_scans.fragment_mass_list, MS2_scans.fragment_intensity_list)
            currentData.add_mass_difference(mass_differences)
        return currentData
    
    
    
    def possible_modifications(self, mass: float, modification_dict: dict, 
                               tolerance_da: float) -> list:
        """
        

        Parameters
        ----------
        mass : float
            Mass to be analyzed if there are any known modifications. 
        modification_list : dict
            Known Modifications. Dictionry {Mass: Mod-Name}
        tolerance_da : float
            Maximal allowed tolerance in Da between theoretical mass and 
            observed mass.

        Returns
        -------
        List
            List of modifications within the tolerance. Sorted by minimal 
            difference to theoretical mass

        """
        possible_modifications_list: list = []
        for mod_mass in modification_dict:    
            dif: float = abs(mass - float(mod_mass)) 
            if dif < tolerance_da:
                possible_modifications_list.append([dif, mod_mass, 
                                                modification_dict[mod_mass]])
        possible_modifications_list: list = sorted(possible_modifications_list)
        return possible_modifications_list if possible_modifications_list \
            else [[0, 0, '?']]
    
    
    def export_results(self):
        """ """
        # mass_difference, higher_mass, higher_mass_intensity, lower_mass, lower_mass_intensity, rt_difference
        return self.Data.Results.histogram