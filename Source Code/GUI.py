# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 20:41:57 2021

@author: Phili
"""

import sys
import pickle
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QFileDialog, QTextEdit, QVBoxLayout, QScrollArea

import MS1Differences as MSDIFF_MS1
from Settings import Settings
from DataStructure import General




class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('MSTopDiff_GUI.ui', self)
        self.show()
        
        ###
        
        self.MS1_diff = MSDIFF_MS1.MS1Differences()
        self.General = General()
        
        ### Default variables
        self.setWindowTitle(Settings.gui_title)
        self.text_massfeature_mass_min.setText(str(Settings.massfeature_mass_min))
        self.text_massfeature_mass_max.setText(str(int(Settings.massfeature_mass_max)))
        self.text_deltamass_mass_min.setText(str(Settings.deltamass_mass_min))
        self.text_deltamass_mass_max.setText(str(Settings.deltamass_mass_max))
        self.text_massdifference_bin_size.setText(str(Settings.deltamass_bin_size))
        self.text_massdifference_annotation_height.setText(str(Settings.annotation_height))
        self.text_massdifference_annotation_distance.setText(str(Settings.annotation_distance))
        self.text_retentiontime_shift_mass.setText(str(Settings.rt_shift_mass))
        self.text_retentiontime_shift_tolerance.setText(str(Settings.rt_shift_mass_tolerance))

        
        # Disable widgets 
        self.disable_widget(self.combobox_deconv_algorithm)
        self.disable_widget(self.group_templates_4)
        self.disable_widget(self.groupBox_5)
        self.disable_widget(self.group_templates_3)
        self.disable_widget(self.group_templates_5)
        self.disable_widget(self.button_load_data)
        self.disable_widget(self.button_plot_masses)
        


    def disable_widget(self, widget):
        widget.setEnabled(False)
        
    def enable_widget(self, widget):
        widget.setEnabled(True)
            
    
    
    def open_file(self):
        self.setWindowTitle(Settings.gui_title + " - Open file ...")
        file_filter = 'Deconvoluted mass feature file (*.tsv *.ms1ft *ms1.feature);; All Files (*)'
        initialFilter = 'Deconvoluted mass feature file (*.tsv *.ms1ft *ms1.feature)'
        self.file_name = QFileDialog.getOpenFileName(caption = 'Load results',
            directory = '', filter = file_filter, initialFilter = initialFilter)[0]
        self.text_open_file.setText(self.file_name.split("/")[-1])
        self.setWindowTitle(Settings.gui_title + " - File opened")

        self.enable_widget(self.combobox_deconv_algorithm)
        self.enable_widget(self.group_templates_3)
        self.enable_widget(self.group_templates_5)
        self.enable_widget(self.button_load_data)
        self.enable_widget(self.button_plot_masses)
        
    
    def plot_masses(self):
        self.setWindowTitle(Settings.gui_title + " - Plot masses ...")
        file = self.file_name
        deconv_alg = self.combobox_deconv_algorithm.currentText()
        mw_min = float(self.text_massfeature_mass_min.toPlainText()) * 1000
        mw_max = float(self.text_massfeature_mass_max.toPlainText()) * 1000
        self.MS1_diff.plotMono(file, deconv_alg, mw_min, mw_max)
        self.setWindowTitle(Settings.gui_title + " - Masse ploted")
    
    
    
    def load_data(self):
        self.setWindowTitle(Settings.gui_title + " - Load data ...")
        deconv_alg = self.combobox_deconv_algorithm.currentText()
        mf_mass_min = float(self.text_massfeature_mass_min.toPlainText()) * 1000
        mf_mass_max = float(self.text_massfeature_mass_max.toPlainText()) * 1000
        rt_window = float(self.text_massfeature_rt_window.value())
        max_charge_diff = int(self.text_massfeature_max_charge_diff.value())
        dm_mass_min = float(self.text_deltamass_mass_min.toPlainText())
        dm_mass_max = float(self.text_deltamass_mass_max.toPlainText())
# dm min dm max in load einbauen!         
        self.MS1_diff.load_file(self.file_name, deconv_alg, mf_mass_min, mf_mass_max)
        self.MS1_diff.calculateMS1Differences(rt_window, max_charge_diff, 
                                              dm_mass_min, dm_mass_max)
        self.setWindowTitle(Settings.gui_title + " - Data loaded")        
        self.enable_widget(self.group_templates_4)
        self.disable_widget(self.button_export_histogram_data)
        self.disable_widget(self.button_show_peaklist)
        self.disable_widget(self.button_show_possible_modifications)
        self.enable_widget(self.groupBox_5)
        self.enable_widget(self.group_templates_3)
        self.enable_widget(self.group_templates_5)
        self.disable_widget(self.button_export_rt_shift_data)

    
    
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
        
        plot_options={"number": hist_number,
                      "intensity": hist_intensity,
                      "nI": hist_intensity_number,
                      "annot":annotation, 
                      "height": annot_height,
                      "distance": annot_distance,
                      "x-axis": (dm_mass_min, dm_mass_max)}

        self.delta_mass = self.MS1_diff.plot_deltaMass(bin_size, plot_options)
        self.setWindowTitle(Settings.gui_title + " - Histogram calculated")
        self.enable_widget(self.button_export_histogram_data)
        self.enable_widget(self.button_show_peaklist)
        self.enable_widget(self.button_show_possible_modifications)
        

    def plot_rt_shift(self):
        self.setWindowTitle(Settings.gui_title + " - Calculate RT shift ...")
        mass = float(self.text_retentiontime_shift_mass.toPlainText()) 
        tolerance = float(self.text_retentiontime_shift_tolerance.toPlainText())
# 60 rausbekommen! 
        bin_size = self.text_retentiontime_shift_bin_size.value() / 60
        print(bin_size)
        self.rt_shift = self.MS1_diff.plot_RTShift(mass, tolerance, bin_size)
        self.setWindowTitle(Settings.gui_title + " - RT shift calculated")
        self.enable_widget(self.button_export_rt_shift_data)
        
    
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
    
    
    

    
    
    def export_histogram_data(self):
        if not self.MS1_diff.Data.Results.histogram:
            print ("Please plot first a retention time shift")
            return False
        file_filter = 'Comma separated values (*.csv);; All Files (*)'
        initialFilter = 'Comma separated values (*.csv)'
        file_name = QFileDialog.getSaveFileName(caption = 'Save results as',
            directory = '', filter = file_filter, initialFilter = initialFilter)[0]
        self.MS1_diff.Data.Results.export_delta_mass_data(file_name)
        
        
    def export_rt_shift_data(self):
        if not self.MS1_diff.Data.Results.retention_time_shift:
            print ("Please plot first a retention time shift")
            return False
        file_filter = 'Comma separated values (*.csv);; All Files (*)'
        initialFilter = 'Comma separated values (*.csv)'
        file_name = QFileDialog.getSaveFileName(caption = 'Save results as',
            directory = '', filter = file_filter, initialFilter = initialFilter)[0]
        self.MS1_diff.Data.Results.export_rt_shift_data(file_name)
        
        
    
    
    def _possible_modifications(self, show_mods = True):
        """ Creates new window, which shows the most intense mass shifts 
            in the n*I plot as a csv file """
            
        if not self.MS1_diff.Data.Results.histogram:
            return "Data must be plotted (Plot Histograms) before a peak list " \
                   "can be displayed."
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
            self.MS1_diff.Data.Results.histogram, bin_size, height, distance, 
            number_checked, intensity_checked, intensitynumber_checked, 
            show_mods, file_name)
        return result_list
    



    def save_results(self):
        file_filter = 'MSTopDiff Result File (*.ms1topdif);; All Files (*)'
        initialFilter = 'MSTopDiff Result File (*.ms1topdif)'
        file_name = QFileDialog.getSaveFileName(caption = 'Save results as',
            directory = '', filter = file_filter, initialFilter = initialFilter)[0]
        data = self.MS1_diff.Data
        pickle.dump(data, open( file_name, "wb"))
        print ("Saved results", file_name)


    def load_results(self):
        file_filter = 'MSTopDiff Result File (*.ms1topdif);; All Files (*)'
        initialFilter = 'MSTopDiff Result File (*.ms1topdif)'
        file_name = QFileDialog.getOpenFileName(caption = 'Load results',
            directory = '', filter = file_filter, initialFilter = initialFilter)[0]
        self.MS1_diff.Data = pickle.load(open(file_name, "rb" ))
        self.text_open_file.setText(self.MS1_diff.Data.file_localisation)
        self.text_massfeature_mass_min.setText(str(self.MS1_diff.Data.mw_cutoff_min))
        self.text_massfeature_mass_max.setText(str(self.MS1_diff.Data.mw_cutoff_max))
        self.text_massfeature_rt_window.setValue(self.MS1_diff.Data.rt_diff_max)
        self.text_massfeature_max_charge_diff.setValue(self.MS1_diff.Data.charge_diff_max)
        print ("Loaded results", file_name)


    def show_about(self):
        text = """
            MSTopDiff
            v.1.0.0 (September, 2021)
            by Philipp T. Kaulich 
            
            Manual: https://github.com/PhilippKaulich/
            Contact: p.kaulich@iem.uni-kiel.de        
        """
        self.w = ResultWindow()
        self.w.textedit.setText(text)
        self.w.show()


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