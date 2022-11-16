# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 16:17:19 2021

@author: PTK
Default Settings
"""



class Settings:
    """ Initializsation of default variables """
    #### General ####
    # Default window title 
    gui_title = "MSTopDiff - Mass Difference Tool"
    #### MS1 #### 
    # Minimal mass of considered mass feature (in kDa)
    massfeature_mass_min: float = 0
    # Maximal mass of considered mass feature (in kDa)
    massfeature_mass_max: float = 100
    #Minimal elution time of mass features  considered for analysis (in min)
    massfeature_time_min = 0
    #Maximal elution time of mass features  considered for analysis (in min)
    massfeature_time_max = 210
    # Minimal considered mass difference (in Da)
    deltamass_mass_min: float = 0
    # Maximal considered mass difference (in Da)
    deltamass_mass_max: float = 300
    # Maximal charge difference (lowest and highest charge state) of 
    # considered mass feature paires for the calculation of mass differences
    deltamass_charge_diff_max: int = 2    
    # Maximal retention time shift (in min) of considered mass feature paires
    # for the calculation of mass differences
    # rt_diff_max: float = 500
    deltamass_rt_diff_max: float = 100
    # Bin size (in Da) of all histogram plots 
    deltamass_bin_size: float = 0.01
    # Check: Show histogram plot
    deltamass_show_histogram: bool = False
    # Check: Show intensity-based histogram plot
    deltamass_show_intensity: bool = False
    # Check: Show intensity x count histogram plot
    deltamass_show_intcount: bool = True
    # Check: Annotation of most intense peaks
    annotation_show: bool = False 
    # Threshold (relative value) for annotation 
    annotation_height: float = 0.01
    # Minmal distance of local maximum for annotation
    annotation_distance: float = 5
    # Mass (in Da) for the calculation of retention time (RT) shift 
    rt_shift_mass: float = 16.00
    # Tolerance (in Da) of Mass considered for the calculation of RT shift
    rt_shift_mass_tolerance: float = 0.01
    # Bin size (in min) of RT shift histogram
    rt_shift_bin_size: float = 0.5 
    # deconvoluted algorithms that can be selected
    deconv_algorithms_selection = ["FLASHDeconv", "ProMEX", "TopFD"]
    # Default deconvolution algorithm
    deconvolution_algorithm: str = "FLASHDeconv"
    # Default filetypes for MS1 analysis
    filetypes_ms1: list = [('TSV files','*.tsv'),
                           ('Mass feature file ProMEX', '*ms1ft'),
                           ('CSV files','*.csv'),
                           ('All files','*.*')]
    # Default plot options for histogram
    plot_options_histogram: dict = {"number": False, "intensity": False, 
                "nI": True, "annot": True, "height": 0.05, "distance": 5,
                "round": 2, "x-axis": (0, 1_500)}
    
    
    #### MS2 ####
    # Minimal considered mass difference (in Da)
    deltamass_mass_min_ms2: float = 0
    # Maximal considered mass difference (in Da)
    deltamass_mass_max_ms2: float = 550
    # Bin size (in Da) of all histogram plots 
    deltamass_bin_size_ms2: float = 0.01
    # Threshold (relative value) for annotation 
    annotation_height_ms2: float = 0.01
    # Minmal distance of local maximum for annotation
    annotation_distance_ms2: float = 5
    # deconvoluted algorithms that can be selected
    deconv_algorithms_selection_ms2 = ["MS-Align"]
    
    # Default filetypes for MS2 analysis
    filetypes_ms2: list  = [('MS align','*.msalign'), 
                            ('MGF files','*.mgf'), 
                            ('All files','*.*')]
    # Default plot options for histogram
    plot_options_histogram_ms2: dict = {"number": True, "intensity": True, 
                "nI": True, "annot": False, "height": 0.05, "distance": 5,
                "round": 2, "x-axis": (0, 550)}
    
    
    def load_possible_modifications(self, file_name):
        mod_dic = {}
        with open(file_name) as f:
            lines = f.read().splitlines()
            for line in lines:
                line.splitlines()
                mass, modification, *_ = line.split(";")
                if mass in mod_dic: mod_dic[mass] += "__" + modification
                mod_dic[mass] = modification
        return mod_dic
