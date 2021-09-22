# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 09:26:58 2021

@author: PTK
MS1-Differences
"""

import matplotlib
import matplotlib.pyplot as plt

from Histogram import Histogram
from Settings import Settings
import DataStructure




class MS1Differences():
    def __init__(self) -> None:
        """ Initialization """
        self.Data = DataStructure.DataMS1()
        self.Histogram = Histogram()


    def load_file(self, file: str, 
                  deconv_type: str = Settings.deconvolution_algorithm,
                  mw_cutoff_min: int = Settings.massfeature_mass_min,
                  mw_cutoff_max: int = Settings.massfeature_mass_max) -> None:
        """
        Load mass feature file. 

        Parameters
        ----------
        file : str
            File path of mass feature file.
        deconv_type : str
            Used deconvolution algorithm.
        mw_cutoff_min : int, optional
            Maximal monoisotopic mass of mass features, which sould be considered.
            The default is Settings.massfeature_mass_min.
        mw_cutoff_max : int, optional
            Minmal monoisotopic mass of mass features, which sould be considered.
            The default is Settings.massfeature_mass_max.
        Returns
        -------
        None
            Load data from mass feature file in self.Data.

        """
        self.Data = DataStructure.DataMS1()
        try:
            self.Data.load_data(file, deconv_type, mw_cutoff_min = 0, 
                                mw_cutoff_max = mw_cutoff_max)
        except:
            print ("Please select the right deconvolution algorithm")
            print ("If the deconvolution algorithm is correct, the file "
                   "structure may be wrong")
            return False 
        # print (len(self.Data.mono_list))
        # # Remove isotopolog artifacts
        # self.Data.remove_isotopic_errors()
        print ("Number of mass features:", len(self.Data.mono_list))
        return True

            
    def plotMono(self, file: str, deconv_type: str = Settings.deconvolution_algorithm, 
                   mw_cutoff_min: int = Settings.massfeature_mass_min, 
                   mw_cutoff_max: int = Settings.massfeature_mass_max) -> None:
        """ Plot monoisotopic mass over retention time with intensity color scale;  
            the radii of data points is proportional to the elution length """
        if not self.load_file(file, deconv_type, mw_cutoff_min, mw_cutoff_max):
            return False
        plt.figure()
        plt.scatter(self.Data.elution_time, self.Data.mono_list, 
                    c = self.Data.abundance, norm = matplotlib.colors.LogNorm(), 
                    s = self.Data.elution_duration, cmap="Greens")
        plt.colorbar()
        plt.xlabel("Retention Time / min")
        plt.ylabel("Monoisotopic mass / Da")
        plt.show()

    

    def _is_over_maximal_charge_diff(self, charge1_low: int, charge2_low: int, 
             charge1_max: int, charge2_max: int, charge_diff_max: int) -> bool:
        return abs(charge1_low - charge2_low) > charge_diff_max or \
            abs(charge1_max - charge2_max) > charge_diff_max
    
    
    def _is_over_maximal_rt_shift(self, rt_time1: float, rt_time2: float, 
                                rt_shift_max: float, rt_factor: int) -> bool:
        rt_difference: float = abs( (rt_time1 / rt_factor) - (rt_time2 / rt_factor))
        return rt_difference > rt_shift_max 


    def _is_over_maximal_mass_shift(self, mass1: float, mass2: float, 
                       mass_shift_max: float, mass_shift_min: float) -> bool:
        mass_difference: float = abs(mass2 - mass1)
        return mass_difference > mass_shift_max or mass_difference < mass_shift_min

        
        
    def _elution_time_difference(self, mass1: float, mass2: float, 
                        elution_time1: float, elution_time2: float) -> float:
        """ calculates the retention time difference, using the lower mass as 
            reference:  RT(higher_mass) - RT(lower_mass) """
        # Elution time difference with lower mass as reference
        elution_time_difference: float = elution_time1 - elution_time2 if mass1 > mass2 \
            else elution_time2 - elution_time1
        return elution_time_difference

    
    def _find_higher_mass_intensity(self, mass1: float, mass2: float, 
                                abundance1: float, abundance2: float) -> list:
        """  compares masses and returns mass difference and higher and lower 
            abundance and mass """
        mass_difference: float = abs(mass2 - mass1)
        higher_mass: float = mass1 if mass1 > mass2 else mass2
        lower_mass: float = mass1 if mass1 < mass2 else mass2
        higher_mass_intensity: float = abundance1 if mass1 > mass2 else abundance2
        lower_mass_intensity: float = abundance1 if mass1 < mass2 else abundance2
        return (mass_difference, higher_mass, higher_mass_intensity, 
                lower_mass, lower_mass_intensity)

    

    def calculateMS1Differences(self, rt_diff_max: float = Settings.deltamass_rt_diff_max, 
                        charge_diff_max: int = Settings.deltamass_charge_diff_max, 
                        diff_min: float = Settings.deltamass_mass_min, 
                        diff_max: float = Settings.deltamass_mass_max) -> list:
        """
        Calculation of MS1 differences for each mass feature to all other 
        higher mass features. 

        Parameters
        ----------
        rt_diff_max : float, optional (default: Settings.deltamass_rt_diff_max)
            Maximal retention time shift / min for mass difference calculation. 
            The default is 100 (min).
        charge_diff_max : int, optinonal (default: Settings.charge_diff_max)
            Maximal charge difference of mass features considered for delta 
            mass calculation
        diff_min: float, optional (default: Settings.deltamass_mass_min)
            Minimal mass difference for delta mass calculation
        diff_max: float, optional (default: Settings.deltamass_mass_max)
            Maximal mass difference for delta mass calculation
        Returns
        -------
        self.Data.Results.results
            Generates results lists (mass differences, abundances and 
            retention time shifts) in self.Data.

        """
        # save Data settings
        self.Data.rt_diff_max = rt_diff_max
        self.Data.charge_diff_max = charge_diff_max

        # Calculation of MS1 differences for each mass feature to all other 
        # higher mass features. 
        for i in range(self.Data.number_of_elements):
            for j in range(i+1, self.Data.number_of_elements): 
                # properties of the considered mass shifts
                mass1 = self.Data.mono_list[i]
                mass2 = self.Data.mono_list[j]
                abundance1 = self.Data.abundance[i]
                abundance2 = self.Data.abundance[j]
                elution_time1 = self.Data.elution_time[i]
                elution_time2 = self.Data.elution_time[j]
                charge1_low = self.Data.min_charge[i]
                charge2_low = self.Data.min_charge[j]
                charge1_max = self.Data.max_charge[i]
                charge2_max = self.Data.max_charge[j]
                # filter criteria for mass difference calculation
                if self._is_over_maximal_rt_shift(elution_time1, 
                    elution_time2, rt_diff_max, self.Data.rt_factor): continue
                if self._is_over_maximal_mass_shift(mass1, mass2, 
                    diff_max, diff_min): continue 
                if self._is_over_maximal_charge_diff(charge1_low, charge2_low, 
                    charge1_max, charge2_max, charge_diff_max): continue   
                
                mass_difference, higher_mass, higher_mass_intensity, lower_mass, \
                  lower_mass_intensity = self._find_higher_mass_intensity(
                      mass1, mass2, abundance1, abundance2)
                  
                rt_difference = self._elution_time_difference(
                    mass1, mass2, elution_time1, elution_time2)
                
                self.Data.Results.add_mass_difference(mass_difference, 
                    higher_mass, higher_mass_intensity, lower_mass, 
                    lower_mass_intensity, rt_difference)
                
        print ("Number of calculated delta masses", len(self.Data.Results.results))
        return self.Data.Results.results
       
    

        
    def plot_deltaMass(self, bin_size: int = Settings.deltamass_bin_size,
         plot_options: dict = Settings.plot_options_histogram) -> None:
        """ Show Plots, parameters see Histogramm.plot_delta_mass """
        if not self.Data.Results.results: 
            print ("Please load data (Load Data) before plotting")
            return None
        mass_difference, higher_mass, higher_mass_intensity, lower_mass, \
            lower_mass_intensity, rt_difference_pm \
             = zip(*self.Data.Results.results.copy())

        self.Data.Results.histogram = self.Histogram.plot_delta_mass(
                                        mass_difference,  
                                        lower_mass_intensity,
                                        higher_mass_intensity,
                                        bin_size,  plot_options)
        


  

    def plot_RTShift(self, mass: float, 
                     tolerance: float = Settings.rt_shift_mass_tolerance,
                     bin_size: float = Settings.rt_shift_bin_size) -> list:
        """
        Plots the retention time shift of a specific mass shift in comparison
        to proteoform without mass shift.

        Parameters
        ----------
        mass : int
            Mass shift of whose retention time shift is to be displayed.
        tolerance : float, optional (default: Settings.rt_shift_mass_tolerance)
            Mass shift tolerance of mass in Da
        Returns
        -------
        rt_shifts : list
            List of all rt_shifts

        """
        if not self.Data.Results.results:
            print ("Please load data (Load Data) before plotting")
            return None
        rt_shifts: list = self.Data.Results.get_retention_time_shift(
                    mass, tolerance = tolerance)
        min_rt_shift: float = min(rt_shifts)
        max_rt_shift: float = max(rt_shifts)
        self.Data.Results.retention_time_shift: list = rt_shifts
        #   bin-size: 0.5 min 
        number_of_bins = int((max_rt_shift - min_rt_shift) / 
                    (self.Data.rt_factor / (1 / bin_size)))
        plt.figure()
        plt.hist(rt_shifts, number_of_bins)
        plt.show()
        return rt_shifts
    
    
    
    
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
        return self.Data.Results.results, self.Data.Results.histogram
            
        