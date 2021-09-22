# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 16:43:16 2021

@author: PTK
Histogram
"""



import math
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np


class Histogram:
    """ """
    def __init__(self):
         pass
    
    def calculate_histogram(self, values: list, intensities1: list = [], \
                            intensities2: list = [], bin_size: int = 0.01) \
                            -> [list, list, list, list, list, list]:
        """
        Calculates a classical and intensity-based histogram from imput list.
        
        
        Parameters
        ----------
        values : list
            Data for histogram plotting.
        intensities1 : list, optional
            Values of data for histogram plotting 1. The default is []
            (no values).
        intensities2 : list, optional
            Values of data for histogram plotting 2. The default is []
            (no values).
        bin_size : int, optional
            Bin size of the histogram. The default is 0.01.
        path : str, optional
            File name to save. The default is "Unknows_calcHist".

        Returns
        -------
        [list, list, list, list, list, list]
            DESCRIPTION.
        hist_bins : list
            Bins of the histogram.
        hist_numbers : list
            Numbers of the bins of the histogram.
        hist_values1 : list
            Sum of the values of the bins 1.
        hist_values2 : list
            Sum of the values of the bins 2.
        hist_numbersXvalues1 : list
            Sum of the values multiplied by the number of the bins 1.
        hist_numbersXvalues2 : list
            Sum of the values multiplied by the number of the bins 1.
        """
        max_list_length: int = int(max(values) / bin_size) + 2
        # contains all bins for histogram 
        hist_bins: list = [bin_size * i for  i in range(max_list_length)]
        empty_list : list = [0 for  i in range(max_list_length)]
        hist_numbers: list = empty_list.copy() # Count of the bins
        hist_values1: list = empty_list.copy() # Sum values of bins 1
        hist_values2: list = empty_list.copy() # Sum values of bins 2
        hist_numbersXvalues1: list = empty_list.copy() # Sum values * count of the bins 1
        hist_numbersXvalues2: list = empty_list.copy() # Sum values * count of the bins 2
        # If no intensites were applied, hist_values1/2 = hist_numbers
        if not intensities1: intensities1 = [1 for i in hist_bins]
        if not intensities2: intensities2 = [1 for i in hist_bins]
        for value, intensity1, intensity2 in zip(values, intensities1, intensities2):
            # Bin-Position in Histogram
            pos = math.ceil(abs(value) / bin_size) 
            hist_values1[pos] += intensity1
            hist_values2[pos] -= intensity2
            hist_numbers[pos] += 1
        for index, (bin_, number, intensity1, intensity2) in \
                    enumerate(zip(hist_bins, hist_numbers, 
                                  hist_values1, hist_values2)):
            hist_numbersXvalues1[index] = number * intensity1
            hist_numbersXvalues2[index] = number * intensity2
        return hist_bins, hist_numbers, hist_values1, hist_values2, \
            hist_numbersXvalues1, hist_numbersXvalues2
    
    
    def _plot(self,x: list, y: list, xlabel: str = "", ylabel: str = "", 
              title: str = "",
              plot_options: dict = {"bin_size":0.001,
                                    "annot":True, 
                                    "height":0.05, 
                                    "distance":5, 
                                    "round":2,
                                    "x-axis": ()}, 
              new_plot=True) -> None:
        """
        Function for plotting line plots 

        Parameters
        ----------
        x : list
            x-values of the plot.
        y : list
            y-values of the plot.
        xlabel : str, optional
            x-label. The default is "".
        ylabel : str, optional
            y-label. The default is "".
        title : str, optional
            Plot title. The default is "".
        plot_options : dict, optional
            Plot options, see "plot_deltaMass". 
        new_plot : TYPE, optional
            If True, a new plot is generated. The default is True.

        Returns
        -------
        None
            DESCRIPTION.

        """
        if new_plot: plt.figure()
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        if plot_options["x-axis"]: plt.xlim(plot_options["x-axis"])#(0, 300))#plot_options["bin_size"])#[int(i) / plot_options["bin_size"] for i in plot_options["x-axis"]])
        plt.plot(x, y)
        if plot_options["annot"]:
            peaks, _ = find_peaks(y, 
                distance=plot_options["distance"]/plot_options["bin_size"], 
                height=plot_options["height"])
            plt.plot(np.array(x)[peaks], np.array(y)[peaks], "x")
            for peak in peaks: 
                plt.annotate(round(x[peak],plot_options["round"]),
                             (x[peak],y[peak]))
                
              
    def _normalizeList(self, list_: list, value: any = "max") -> list:
        """
        

        Parameters
        ----------
        list_ : list
            list that should me normalized.
        value : any, optional
            value to which the list should be normalized. If "max", all elements
            will be normalized to the maximal number of the list

        Returns
        -------
        list
            Normalized list.

        """
        if value=="max": value=max(list_)
        if value==0: value=min(list_)
        normalized_list = [i/value for i in list_]
        return normalized_list
    
    
                

    def plot_delta_mass(self, diff_list, diff_intensity_mass_low, 
         diff_intensity_mass_high, bin_size: int = 0.001,
         plot_options: dict = {"number": False, "intensity": False, "nI": True,
                       "annot": True, "height": 0.05, "distance": 5,
                       "round": 2, "x-axis": ()}) -> None:
        """
        Creates mass shift plots. 

        Parameters
        ----------
        diff_list
            Mass difference list.
        diff_intensity_mass_low
            Corresponding intensity of lower mass peaks for mass shift.
        diff_intensity_mass_high
            Corresponding intensity of higher mass peaks for mass shift.
        bin_size : int, optional
            Resolution (=bin size) of the plots. The default is 0.001.
        plot_options : dict, optional
            DESCRIPTION. 
                "number" : bool, optional
                    If True, histogram (count) is shown. 
                    The default is False.
                "intensity" : bool, optional
                    If True, histogram (value) is shown. 
                    The default is False.
                "nI" : bool, optional
                    If True, histogram (count*value) is shown. 
                    The default is True.
                "annot" : bool, optional
                    If True, the most intense peaks of the plots were annotated. 
                    The default is False.
                "height": float, optional
                    Minimal (relative) height of annotation. 
                    The default is 0.05.
                "distance": int, optional
                    Minimal distance between annotated local maxima. 
                    The default is 5.
                "round": int, optional
                    DESCRIPTION.
        Returns
        -------
        hist_bins, hist_numbers, hist_values1, hist_values2, hist_numbersXvalues1, \
            hist_numbersXvalues2
            DESCRIPTION.

        """

        # Calculation of histogram values
        hist_bins, hist_numbers, hist_values1, hist_values2, hist_numbersXvalues1, \
            hist_numbersXvalues2 = self.calculate_histogram(diff_list, diff_intensity_mass_low, diff_intensity_mass_high, bin_size)
        # Plotting attributes
        annot: bool = plot_options["annot"]
        height: float = plot_options["height"]
        distance: int = plot_options["distance"]
        x_axis: list = plot_options["x-axis"]
        # Plotting clasical histogram
        if plot_options["number"]:
            self._plot(hist_bins, hist_numbers, xlabel="ΔMass", ylabel="Count", 
                       plot_options={"bin_size":bin_size,"annot":annot, 
                                     "height":height, "distance":distance, 
                                     "round":2, "x-axis": x_axis})
        # Plotting abundance-based histogram (sum abundance of higher mass 
        # (plus direction) and lower mass (minus direction) for each delta mass)
        if plot_options["intensity"]:
            # Lower mass abundance (normalized to maximum abundance)
            self._plot(hist_bins, self._normalizeList(hist_values1), 
                       xlabel="ΔMass", ylabel="Rel. Intensity",
                       plot_options={"bin_size":bin_size,"annot":annot, 
                                     "height":height, "distance":distance, 
                                     "round":2, "x-axis": x_axis})
            # Higher mass abundance (normalized to maximum of lower mass abundance)
            self._plot(hist_bins, self._normalizeList(hist_values2, max(hist_values1)), 
                       xlabel="ΔMass", ylabel="Rel. Intensity",
                       plot_options={"bin_size":bin_size,"annot":False, 
                                     "height":height, "distance":distance, 
                                     "round":2, "x-axis": x_axis}, 
                       new_plot=False) 
            # # Sum Abundance (abundance of lower and higher mass)
            # sum_intensity = np.array(hist_values1)-np.array(hist_values2)
            # self._plot(hist_bins, self._normalizeList(sum_intensity,max(sum_intensity)), 
            #            xlabel="ΔMass", ylabel="Rel. Intensity", 
            #            title="Sum Intensity", 
            #            plot_options={"bin_size":bin_size,"annot":False, 
            #                          "height":height, "distance":distance, 
            #                          "round":2, "x-axis": x_axis})
        # Plotting abundance (for higher (plus direction) and lower 
        # (minus direction) mass) multiplied by number of the delta mass shift
        if plot_options["nI"]:
            # Lower mass (normalized values)
            self._plot(hist_bins, self._normalizeList(hist_numbersXvalues1), 
                       xlabel="ΔMass", ylabel="Rel. Intensit*Count",
                       plot_options={"bin_size":bin_size,"annot":annot, 
                                     "height":height, "distance":distance, 
                                     "round":2, "x-axis": x_axis})
            # Higher mass (normalized to maximum of lower mass values)
            self._plot(hist_bins, self._normalizeList(hist_numbersXvalues2,
                                                      max(hist_numbersXvalues1)), 
                       xlabel="ΔMass", ylabel="Rel. Intensity*Count",
                       plot_options={"bin_size":bin_size,"annot":False, 
                                     "height":height, "distance":distance, 
                                     "round":2, "x-axis": x_axis}, new_plot=False)
        plt.show()
        return list(zip(hist_bins, hist_numbers, hist_values1, hist_values2, \
            hist_numbersXvalues1, hist_numbersXvalues2))
            