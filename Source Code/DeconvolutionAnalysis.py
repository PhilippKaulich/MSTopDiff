# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 09:39:33 2021

@author: Philipp
Deconvolution algorithms 
"""


class DeconvColumns:
    def __init__(self, deconv_alg: str): 
        """
        Provides the column names of mass feature files for different 
        deconvolution algorithms: Monoisotopic mass, retention time start and
        end, minimal and maximal charge, abundance, rt-factor (seconds or minutes)
        Supported: FlashDeconv, ProMEX, TopFD, BioPharma

        Parameters
        ----------
        deconv_alg : str
            Used deconvolution algorithm. Possible: FlashDeconv, ProMEX, TopFD.
            If not supported algorithm is used False is returned

        Returns
        -------
        None.

        """
        if deconv_alg == "FLASHDeconv": self.flashdeconv()
        elif deconv_alg == "ProMEX": self.promex()
        elif deconv_alg == "TopFD": self.topfd()
        elif deconv_alg == "BioPharma": self.biopharma()
        else: print ("Not supported deconvolution algorithm"); return False
        
    def flashdeconv(self):
        """ Column names after deconvolution with FlashDeconv """
        self.mass = "MonoisotopicMass"
        self.rt_start = "StartRetentionTime"
        self.rt_end = "EndRetentionTime"
        self.charge_min = "MinCharge"
        self.charge_max = "MaxCharge"
        self.abundance = "SumIntensity"
        self.rt_factor = 60
        
    def promex(self):
        """ Column names after deconvolution with ProMEX """
        self.mass = "MonoMass"
        self.rt_start = "MinElutionTime"
        self.rt_end = "MaxElutionTime"
        self.charge_min = "MinCharge"
        self.charge_max = "MaxCharge"
        self.abundance = "Abundance"
        self.rt_factor = 1
        
    def topfd(self):
        """ Column names after deconvolution with TopFD """
        self.mass = "Mass"
        self.rt_start = "Time_begin"
        self.rt_end = "Time_end"
        self.charge_min = "Minimum_charge_state"
        self.charge_max = "Maximum_charge_state"
        self.abundance = "Intensity"
        self.rt_factor = 60
        
        
    def biopharma(self):
        """ Column names after deconvolution with BioPharma """
        self.mass = "Monoisotopic_Mass"
        self.rt_start = "RT_Range"
        self.rt_end = "RT_End"
        self.charge_min = "Number_of_Charge_States"
        self.charge_max = "Number_of_Charge_States"
        self.abundance = "Sum_Intensity"
        self.rt_factor = 1
