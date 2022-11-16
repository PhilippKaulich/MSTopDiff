# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 15:31:59 2021

@author: PTK
"""

import pandas as pd
import csv
from scipy.signal import find_peaks

from DeconvolutionAnalysis import DeconvColumns
from Settings import Settings


class DataMS1:
    """ Data structure for deconvoluted mass feature files """
    def __init__(self):
        """ Initialization """
        self.data_input: list = []
        self.mono_list: list = []
        self.elution_time_start: list = []
        self.elution_time_end: list = []
        self.elution_time: list = []
        self.elution_duration: list = []
        self.min_charge: list = []
        self.max_charge: list = []
        self.abundance: list = []
        self.number_of_elements: int = 0
        self.rt_factor: int = 1

        self.Results = self.DataResults()
        
    def _zip(self) -> list:
        """ Returns zipped list of all input data: abundance, monoisotopic list, 
            elution time start, end, average and duration, minimum and maximum charge """
        zipped_list: list = zip(self.abundance, self.mono_list, self.elution_time_start, 
                          self.elution_time_end, self.elution_time, 
                          self.elution_duration, self.min_charge, 
                          self.max_charge)
        return sorted(zipped_list)
    
    def _unzip(self, zipped_list: list):
        """ unzip zipped version of input data """
        [self.abundance, self.mono_list, self.elution_time_start, \
                          self.elution_time_end, self.elution_time, \
                          self.elution_duration, self.min_charge, \
                          self.max_charge] = list(map(list, zip(*zipped_list)))  

    
    def delete_data(self, indices: list): 
        """ delete input data with index in indices  """
        sorted_indices = sorted(list(set(indices)), reverse=True)
        for index in sorted_indices:
             del self.mono_list[index]         
             del self.elution_time_start[index] 
             del self.elution_time_end[index] 
             del self.elution_time[index] 
             del self.elution_duration[index] 
             del self.min_charge[index]  
             del self.max_charge[index] 
             del self.abundance[index] 
        self.number_of_elements = len(self.mono_list)

        
    def load_data(self, file, deconv_alg, mw_cutoff_min = 0, 
                  mw_cutoff_max = 100_000, time_cutoff_min = 0, 
                  time_cutoff_max = 1000000):
        """ load data from deconvolution algorithms """
        if not file:
            print ("Please first select a deconvoluted mass feature file")
            return None
        self.file_localisation = file
        self.mw_cutoff_min = mw_cutoff_min
        self.mw_cutoff_max = mw_cutoff_max
        self.time_cutoff_min = time_cutoff_min
        self.time_cutoff_max = time_cutoff_max
        self.deconv_alg = deconv_alg
        # Checking if loaded file is comma or tab separated
        sep = "," if file.endswith(".csv") else "\t"
        data = pd.read_csv(self.file_localisation, sep = sep) 
        print("Loaded file {}".format(self.file_localisation))
        
        # Load properties for different deconv alg
        properties = DeconvColumns(deconv_alg)
        #Exclude all mass features with mass not within mass cutoffs
        data = data[data[properties.mass]<float(mw_cutoff_max)]
        data = data[data[properties.mass]>float(mw_cutoff_min)]

        # Biopharma provides less information compared to other devonvolution
        # algorithms
        if deconv_alg == "BioPharma":        
            print ("Note: Since this file type does not provide information about "
                       "the charge state, the maximum charge difference cannot be "
                       "considered.")          
            # RT-range: xy - zy : Split into two columns
            data[[properties.rt_start, properties.rt_end]] = \
                data[properties.rt_start].str.split(' - ', expand=True).astype(float)
        # Exclude all mass features with retention time not within time cutoffs
        self.rt_factor = properties.rt_factor
        data = data[data[properties.rt_start]<float(time_cutoff_max)*self.rt_factor]
        data = data[data[properties.rt_start]>float(time_cutoff_min)*self.rt_factor]
        # Initializing of important deconvoluted features as list
        self.mono_list = data[properties.mass].to_list()
        self.elution_time_start = data[properties.rt_start].to_list()
        self.elution_time_end = data[properties.rt_end].to_list()
        self.elution_time: list[int] = [(start+end)/2 for start, end in \
                        zip(self.elution_time_start, self.elution_time_end)]
        self.elution_duration: list[int] = [end-start for start,end in \
                        zip(self.elution_time_start, self.elution_time_end)]
        self.min_charge = data[properties.charge_min].to_list()
        self.max_charge = data[properties.charge_max].to_list()
        self.abundance = data[properties.abundance].to_list()
        self.number_of_elements = len(self.mono_list)
        
        
        
        
    def remove_isotopic_errors(self):
        """ Removes isotopic artifacts """
        # sort list to highest intensity 
        data_zip = sorted(self._zip(), reverse=True)
        self._unzip(data_zip)
        # monoisotopic mass list in descending intensity order
        mono_list = [i[1] for i in data_zip]
        index_isotopic_errors_list = []
        for currentIndex, mono in enumerate(mono_list):
            isotop_errors_index = self.find_isotopic_errors(mono_list, currentIndex)
            if isotop_errors_index:
                index_isotopic_errors_list.extend(isotop_errors_index)
        self.delete_data(index_isotopic_errors_list)
        #evtl ohne aktuelle Liste zuverändern und mit Rückgabewert? 



    def find_isotopic_errors(self, l, start_index) -> list:
        """
        Find isotopic artifacts in list l of l[start_index]

        Parameters
        ----------
        l : list
            Mass list of monoisotopic masses.
        start_index : int
            Start index.

        Returns
        -------
        isotopic_errors_index_list : TYPE
            DESCRIPTION.

        """
        current_element = l[start_index]
        isotopic_errors_index_list = []
        for index, element in enumerate(l[start_index:]):
            if self._is_isotopic_error(element, current_element):
                isotopic_errors_index_list.append(index+start_index)
        return isotopic_errors_index_list


    def _is_isotopic_error(self, x, y):
        """ prüft, ob x und y ein isotopic error sind """
        # ppm = 10*10e-6 
        diff = abs(y-x)
        for i in range(1,3):
            # is_error = diff > i-i*ppm and diff < i+i*ppm
            is_error = diff > (1-0.05) and diff < (1+0.05)
            if is_error:
                return is_error
        return False      
    


        
    class DataResults:
        """ Data structure for MS1 differences """
        def __init__(self):
            """ Initialization """
            self.results = []
            self.histogram = []
            self.retention_time_shift = []
            
        def add_mass_difference(self, mass_difference, higher_mass, higher_mass_intensity, lower_mass, 
                     lower_mass_intensity, rt_difference):
            """ add mass difference (and mass features) to result """
            self.results.append([mass_difference, 
                     higher_mass, 
                     higher_mass_intensity, 
                     lower_mass, 
                     lower_mass_intensity, 
                     rt_difference])
            
        def _is_in_tolerance_ppm(self, mass1, mass2, max_da):
            """ checks if mass1 and mass2 are within the tolerance max_da (in ppm) """
            dm = abs(mass1/mass2 * 1_000_000 - 1_000_000)
            return dm < max_da 
            
        def _is_in_tolerance_da(self, mass1, mass2, max_da):
            """ checks if mass1 and mass2 are within the tolerance max_da (in Da) """
            dm = abs(mass1 - mass2)
            return dm < max_da 
            
            
        def get_retention_time_shift(self, target_mass_difference, tolerance=10): 
            """ """
            mass_difference, _, _, _,  _, rt_difference_pm \
                    = zip(*sorted(self.results.copy()))
            rt_shift_list = []
            for index, mass_diff in enumerate(mass_difference):
                if self._is_in_tolerance_da(target_mass_difference, mass_diff, tolerance):
                    rt_shift_list.append(rt_difference_pm[index])
# perfomanter schreiben,v da Liste sortiert ist!!!
            return rt_shift_list
        
        
        def _export(self, file_name, data, header):
            """ """
            with open(file_name, "w", newline='')  as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(data)
            print("Data successfully exported:", file_name)
            
            
        def export_delta_mass_data(self, file_name):
            """ """
            data = self.histogram
            if not data: 
                print ("Please calculate histogram (Plot Data) before exporting the data")
                return
            header = ["bin", "count", "intensity_lower_mass", "intensity_higher_mass", 
                      "intensity_lower_mass x count", "intensity_higher_mass x count"] 
            self._export(file_name, data, header)
            
        def export_rt_shift_data(self, file_name):
            """ """
            data = enumerate(self.retention_time_shift)
            if not data: 
                print ("Please calculate histogram (Plot RT shift) before exporting the data")
                return
            header = ["Nr.", "RT-shift"] 
            self._export(file_name, data, header)
            

        




class DataMS2:
    """ Data structure for deconvoluted ms2 mass differences """
    def __init__(self):
        """ Initialization """
        self.difference_list = []
        self.difference_intensity_list = []
        self.difference_intensity_list_low = []
        self.difference_intensity_list_high = []
        
        self.Results = self.DataResults()
        
    def add_mass_difference(self, element):
        """ add mass difference element to result lists 
            element: list [mass difference, sum intensity, intensity_lower_mass
            intensity_higher_mass] """
        self.difference_list.extend(element[0])
        self.difference_intensity_list.extend(element[1])
        self.difference_intensity_list_low.extend(element[2])
        self.difference_intensity_list_high.extend(element[3])
        

    class DataResults:
        def __init__(self):
            self.results = []
            self.histogram = []
            
        def _export(self, file_name, data, header):
            """ """
            with open(file_name, "w", newline='')  as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(data)
            print("Data successfully exported:", file_name)
                
                
        def export_delta_mass_data(self, file_name):
            """ """
            data = self.histogram
            if not data: 
                print ("Please calculate histogram (Plot Data) before exporting the data")
                return
            header = ["bin", "count", "intensity_lower_mass", "intensity_higher_mass", 
                     "intensity_lower_mass x count", "intensity_higher_mass x count"] 
            self._export(file_name, data, header)





class General:
    """ functions used for MS1 and MS2 differences """
    def __init__(self):
        pass
    
    def _find_peaks(self, values: list, distance: float, height: float) -> list:
        """  finds all local maximums (within distance) in values above the 
            threshold height and returns indices of maxima """
        max_index, _ = find_peaks(values, distance = distance, height = height)
        return max_index


    def _normalize_list(self, l: list):
        """ Normalizes list to maximum.   """
        max_value: float = max(l)
        norm_list: list = [i / max_value for i in l]
        return norm_list
    
    
    def _ratio_list(self, l1, l2):
        """ returns ratio list, l[e] = abs(l1[e] / l2[e])  """
        l_ratio = []
        for e1, e2 in zip(l1, l2):
            if e2 != 0:
                l_ratio.append(abs(e1 / e2))
            else:
                l_ratio.append(0)
        return l_ratio
    
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
    
    
    

    def find_peaks_and_possible_modifications(self, data, bin_size, height, 
                distance, number_checked, intensity_checked, 
                intensitynumber_checked, show_mods = True, file_name = ""):
        """ returns maximum peaks and possible modifications as string """

        if show_mods:
            possible_modifications_dict = Settings.load_possible_modifications(self, file_name)
            print("loaded modification file", file_name)
        bins, numbers, intensity1, intensity2, numberintensity, _ = \
            zip(*data)
        if number_checked:
            li = numbers 
        elif intensity_checked:
            li = intensity1
        elif intensitynumber_checked:
            li = numberintensity
        intensity_ratio = self._ratio_list(intensity2, intensity1)
        normalized_li = self._normalize_list(li)
        # Most intense peaks
        maximum_list = self._find_peaks(normalized_li, 
                                               distance / bin_size, height)
        all_peaks = []
        header = "Mass difference, Count, Intensity Ratio, Possible Modification, Mass, ΔM \n" \
                if show_mods else "Mass difference, Count, Intensity Ratio \n"
        all_peaks.append(header)
        for maximum in maximum_list:
            mass_difference = bins[maximum]
            count = numbers[maximum]
            ratio = intensity_ratio[maximum]
            if show_mods:
                possible_mods = self.possible_modifications(
                    mass_difference, possible_modifications_dict, 4 * bin_size)[0]
                dm, mass, modification = possible_mods
                line = "{:,.3f}, {}, {}, {}, {:,.2f}, {:,.3f} \n".format(mass_difference, 
                                        count, modification, mass, float(dm), ratio)
            else:
                line = "{:,.3f}, {}, {:,.3f} \n".format(mass_difference, count, ratio)
            all_peaks.append(line)
        return "".join(all_peaks)
