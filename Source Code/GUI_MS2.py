# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 08:02:26 2021

@author: Phili
"""

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, \
                QFileDialog, QCompleter, QMainWindow, QVBoxLayout, QTextEdit
import sys
import pickle 


import MS1Differences as MSDIFF_MS1
import MS2Differences as MSDIFF_MS2
from Settings import Settings
from DataStructure import General



class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('MS2TopDiff_GUI.ui', self)
        self.show()
        
        #### 

        self.MS2_diff = MSDIFF_MS2.MS2Differences()
        self.General = General()
        
        ####
        
        self.setWindowTitle(Settings.gui_title)
        self.text_deltamass_mass_min.setText(str(Settings.deltamass_mass_min_ms2))
        self.text_deltamass_mass_max.setText(str(Settings.deltamass_mass_max_ms2))
        self.text_massdifference_bin_size.setText(str(Settings.deltamass_bin_size_ms2))
        self.text_massdifference_annotation_height.setText(str(Settings.annotation_height_ms2))
        self.text_massdifference_annotation_distance.setText(str(Settings.annotation_distance_ms2))

        # Disable widgets 
        self.disable_widget(self.combobox_deconv_algorithm)
        self.disable_widget(self.group_templates_5)
        self.disable_widget(self.button_load_data)
        self.disable_widget(self.group_templates_4)

        


    def disable_widget(self, widget):
        widget.setEnabled(False)
        
    def enable_widget(self, widget):
        widget.setEnabled(True)
        
        
        
        
    def open_file(self):
        self.setWindowTitle(Settings.gui_title + " - Open file ...")
        file_filter = 'Deconvoluted MS2 spectra (*.msalign);; All Files (*)'
        initialFilter = 'Deconvoluted MS2 spectra file (*.msalign)'
        self.file_name = QFileDialog.getOpenFileName(caption = 'Load results',
            directory = '', filter = file_filter, initialFilter = initialFilter)[0]
        self.text_open_file.setText(self.file_name.split("/")[-1])
        self.enable_widget(self.combobox_deconv_algorithm)
        self.enable_widget(self.button_load_data)
        self.enable_widget(self.group_templates_5)
        self.setWindowTitle(Settings.gui_title + " - File opened")
    
    
    
    def load_data(self):
        self.setWindowTitle(Settings.gui_title + " - Load Data ...")
        deconv_alg = self.combobox_deconv_algorithm.currentText()
        dm_mass_min = float(self.text_deltamass_mass_min.toPlainText())
        dm_mass_max = float(self.text_deltamass_mass_max.toPlainText())
# dm min dm max in load einbauen!       
      
        self.MS2_diff.load_file(self.file_name)
        self.results = self.MS2_diff.calculateDifferences()
        print ("Number of considered mass differences: ", 
               len(self.results.difference_list))
        self.enable_widget(self.group_templates_4)
        self.disable_widget(self.button_export_histogram_data)
        self.disable_widget(self.button_show_peaklist)
        self.disable_widget(self.button_show_possible_modifications)
        self.setWindowTitle(Settings.gui_title + " - Data loaded")      

        

    def plot_histogram(self):
        self.setWindowTitle(Settings.gui_title + " - Calculate histogram ...")
        bin_size = float(self.text_massdifference_bin_size.text())
        dm_mass_min = float(self.text_deltamass_mass_min.toPlainText())
        dm_mass_max = float(self.text_deltamass_mass_max.toPlainText())
        
        hist_number = self.checkbox_deltamass_count.isChecked()
        hist_intensity = self.checkbox_deltamass_intensity.isChecked()
        hist_intensity_number = self.checkbox_deltamass_countintensity.isChecked()
        annotation = self.checkbox_annotation_show.isChecked()
        annot_height = float(self.text_massdifference_annotation_height.toPlainText())
        annot_distance = float(self.text_massdifference_annotation_distance.toPlainText())
        self.setWindowTitle(Settings.gui_title + " - Histogram calculated")
                

        plot_options = {"number": hist_number,
                        "intensity": hist_intensity,
                        "nI": hist_intensity_number,
                        "annot":annotation, 
                        "height": annot_height,
                        "distance": annot_distance,
                        "x-axis": (dm_mass_min, dm_mass_max)}
        
        self.MS2_diff.createHistogram(self.results.difference_list, 
                                self.results.difference_intensity_list_low, 
                                self.results.difference_intensity_list_high, 
                                bin_size, plot_options = plot_options)
        self.enable_widget(self.button_export_histogram_data)
        self.enable_widget(self.button_show_peaklist)
        self.enable_widget(self.button_show_possible_modifications)
        
        
    def export_histogram_data(self):
        file_name = QFileDialog.getSaveFileName()[0]
        self.MS2_diff.Data.Results.export_delta_mass_data(file_name)



    def show_peaklist(self):
        h1 = self._possible_modifications(False)
        self.w = ResultWindow()
        self.w.textedit.setText(h1)
        self.w.show()
        pass
    
    def show_possible_modifications(self):
        h1 = self._possible_modifications(True)
        self.w = ResultWindow()
        self.w.textedit.setText(h1)
        self.w.show()
        
        
    
    def _possible_modifications(self, show_mods = True):
        """ Creates new window, which shows the most intense mass shifts 
            in the n*I plot as a csv file """
            
        if not self.MS2_diff.Data.Results.histogram:
            print ("Please Plot the data before ")
            return False
        
        bin_size = float(self.text_massdifference_bin_size.text())
        height = float(self.text_massdifference_annotation_height.toPlainText())
        distance = float(self.text_massdifference_annotation_distance.toPlainText())
        
        number_checked = self.checkbox_deltamass_count.isChecked()
        intensity_checked = self.checkbox_deltamass_intensity.isChecked()
        intensitynumber_checked = self.checkbox_deltamass_countintensity.isChecked()
        
        if show_mods:
            file_filter = 'Comma Separated file (*.csv);; All Files (*)'
            initialFilter = 'Comma Separated file (*.csv)'
            file_name = QFileDialog.getOpenFileName(caption = 'Save results as',
                directory = '', filter = file_filter, initialFilter = initialFilter)[0]
        else:
            file_name = ""
        result_list = self.General.find_peaks_and_possible_modifications(
            self.MS2_diff.Data.Results.histogram, bin_size, height, distance, 
            number_checked, intensity_checked, intensitynumber_checked, 
            show_mods, file_name)
        return result_list
            
    
    

    
    
    def save_results(self):
        """ """
        file_filter = 'MSTopDiff Result File (*.ms2topdif);; All Files (*)'
        initialFilter = 'MSTopDiff Result File (*.ms2topdif)'
        file_name = QFileDialog.getSaveFileName(caption = 'Save results as',
            directory = '', filter = file_filter, initialFilter = initialFilter)[0]
        data = self.results
        pickle.dump(data, open( file_name, "wb"))
        print ("Saved results", file_name)
        
    
    
    def open_results(self):
        """ """
        file_filter = 'MSTopDiff Result File (*.ms2topdif);; All Files (*)'
        initialFilter = 'MSTopDiff Result File (*.ms2topdif)'
        file_name = QFileDialog.getOpenFileName(caption = 'Load results',
            directory = '', filter = file_filter, initialFilter = initialFilter)[0]
        self.results = pickle.load(open(file_name, "rb" ))
        #"deconv_alg"
        print ("Loaded results", file_name)
    
    
    
class ResultWindow(QWidget):
    """ New window used for peak detection results """
    def __init__(self):
        super().__init__()
        self.setFixedSize(640, 480)
        self.setWindowTitle("Peaklist - Results")
        layout = QVBoxLayout()
        self.textedit = QTextEdit()
        layout.addWidget(self.textedit)
        self.setLayout(layout)
        
        

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()