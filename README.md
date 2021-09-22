# MSTopDiff: _A tool for the visualization of mass shifts in deconvoluted top-down proteomics data for the database-independent detection of protein modifications_

<p align="center">
<img src="https://img.shields.io/badge/python-3.7.3+-blue.svg" alt="Python Version"> 
<img src="https://img.shields.io/pypi/l/MSDIFF" alt="License">
</p>

**MSTopDif is a command line script with graphical user interface for the database-free detection of modifications in top-down mass spectrometric data.**

<p align="center">
<img src="https://user-images.githubusercontent.com/65888185/133243768-fd004beb-63ff-4aa6-9dfb-3099123a7bf3.png" alt="MSTopDiff Priciple">
</p>

---

## Contents
- [Abstract](#abstract)
- [Requirements](#requirements)
- [How to run MSTopDif](#how-to-run-mstopdif)
- [How to use MSTopDif](#how-to-use-mstopdif)
- [Data Sets for Testing](#data-sets-for-testing)
- [Graphical User Interface](#graphical-user-interface)
- [Results](#results)
    - [Histogram](#histogram)
    - [Intensity-based histogram](#intensity-based-histogram)
    - [Intensity×Count histogram](#IntensityxCount-histogram)
- [References](#references)
- [License](#license)

---


## Abstract 
> Top-down proteomics (TDP) analyses intact proteoforms with all their post-translational modifications, genetic and RNA splice variants. In addition, modifications introduced either deliberately or inadvertently during sample preparation, i.e., via oxidation, alkylation or labeling reagents, or through the formation of non-covalent adducts (e.g., detergents), further increase sample complexity. In order to facilitate recognition of protein modifications introduced during TD-analysis we developed MSTopDiff, a software tool with graphical user interface written in python capable to monitor and visualize protein modifications by calculating and visualizing mass differences in top-down data without the prerequisite of a database search. We demonstrate the successful application of MSTopDiff by the detection of artifacts originating from oxidation, formylation, overlabeling during isobaric labeling and adduct formation with cations or SDS. MSTopDiff offers several modes of data representation using deconvoluted MS1 or MS2 spectra. In addition to artificial modifications, the tool enables visualization of biological modifications such as phosphorylation and acetylation. MSTopDiff provides a facile overview on artificial and biological modifications in top-down proteomics samples, which makes it a valuable tool in quality control of standard workflows and for parameter evaluation during method development.



## Requirements
* Python 3.7.3 or higher

### Packages
* `pandas`
* `matplotlib`
* `math`
* `scipy`
* `numpy`
* `csv`
* `pickle`
* `PyQt5`


## How to run MSTopDif
> We recommend to install and use [Anaconda](https://www.anaconda.com/products/individual) and its build in command line prompt. In case you don't use Anaconda, make sure all required packages are [installed](https://packaging.python.org/tutorials/installing-packages/) upfront. 
```
$ cd <PATH/TO/SOURCES>
$ python GUI.py
```

##  How to use MSTopDif
1. Acquire or download mass spectrometric raw data of intact proteins.
2. Deconvolute raw data with FLASHDeconv (Jeong, 2020) or ProMEX (Park, 2017) using e.g. [Mash explorer](https://labs.wisc.edu/gelab/MASH_Explorer/MASHSoftware.php) (Wu, 2020) or stand-alone versions.
3. [Run MSTopDif](#how-to-run-mstopdif) python script.
4. Press "Open file" to select deconvoluted mass feature file (`.tsv`, `.ms1ft`, `.csv` or other file format)
5. Select the deconvolution algorithm that generated the mass feature file
6. Optional: change default filter criteria (mass range, bin size, maximal charge and retention time difference)
7. Press "Load Data": Script calculates all mass differences. This step may take a while depending on the number of mass features; please don't close the GUI during the calculation. After the calculation is completed, the number of calculated mass differences is displayed in the command line.
8. Optional: change default parameter of mass difference plot (mass range, bin-size, plots that sould be shown, annotation of the plot)
9. Press "Plot Data": Script generates interactive mass difference plots 
10. Optional: change default RT shift analysis parameter (mass, tolerance, bin size) and press "Plot RT shift". Script generates RT shift plot. 


## Data Sets for Testing
To test the Script you can download the datasets in the "Datasets" folder, which contains the deconvoluted mass feature file and a deconvoluted MS2 file of an example described in the publication. 


## Graphical User Interface
The graphical user interface has two frames for the analysis of deconvoluted MS1 and MS2 data. 

<p align="center">
<img src="https://user-images.githubusercontent.com/65888185/133244101-fa47fbbe-1e60-401f-b67f-a54646b0eb7f.PNG" alt="GUI">
</p>

### Data
| Entry | Description |
| --- | --- |
| Open file | Opens file dialog to chose a deconvoluted mass feature file.<br>_Note: It is not possible to choose raw files; they have before been deconvoluted using deconvolution algorithms._ |
| Used deconvolution algorithm | Select used deconvolution algorithm. Supported are `FLASHDeconv`, `ProMEX` or `TopFD`. |
| Plot masses | Plot monoisotopic masses over retention time (x: retention time, y: monoisotopic mass, z (color-coded): intensity). The radii of the points represent the elution duration. |
| Mass Feature Filter > From ... to ... kDa | Minimal and maximal monoisotopic mass of mass features that are considered for the calculation of mass differences |
| Delta Mass parameters > From ... to ... Da | Only mass shifts from ... to ... Da are shown in the resulting plots |
| Delta Mass parameters > RT-window | Maximal retention time shift of two mass features that is considered for the calculation of mass differences. The retention time difference is calculation by the difference of the average elution time.  |
| Delta Mass parameters > Max. charge diff. | Maximal charge difference of two mass features that is considered for the calculation of mass differences. The number defines the maximal difference of the lowest and highest detected charge states. For example, a value of 2 means that both the lowest and highest charge state for two mass features only allowed to differ by maximal two charge states to be considered for mass difference calculation.  |
| Load Data | Initialize data (needed for calculation and plotting).  |

### Plot Mass Differences
| Entry | Description |
| --- | --- |
| Bin size | Bin size of calculated histogram defining the resolution of the plots. |
| Show > Count | If checked, classical histogram plot is shown.  |
| Show > Intensity | If checked, intensity-based histogram plot is shown. |
| Show > Count x Intensity | If checked, intensity x count plot is shown. |
| Annotation and Maxima > Show Annotation | If checked, annotations of the most intense peaks are shown. |
| Annotation and Maxima > Height | Relative threshold (based on maximum value) for peak detection. |
| Annotation and Maxima > Distance | Minimal mass shift between neighbouring maximal peaks. |
| Plot Data | Plot data. |
| Export | Exporting histogram data as .csv file. |
| Peaks | Shows maximal peaks. |
| Mods | Shows possible modifications. |

### RT shift
| Entry | Description |
| --- | --- |
| Mass shift ... ± ... Da | Monoisotopic mass and tolerance (in Da) for analysis of retention time shift |
| Bin size | Bin size of calculated histogram. |
| Plot RT shift | Plots the retention time shift as histogram.  |
| Export |  Exporting retention time shift data as .csv file. |

### Menu
| Entry | Description |
| --- | --- |
| Edit > Save results | Opens a file dialog to save all result data as .mstopdif file. Allows quick access to the data at any time without the need for a mass difference calculation ("Load Data"). |
| Edit > Load results | Opens a file dialog to load all result data from a file .mstopdif-file. |
| File > Close | Closes the window. |



## Results
_MSTopDif generates three plots._

### Histogram
The calculated mass differences are presented as a classical histogram with a variable bin size defining the resolution of the plot. Here, the distinct number of mass differences found within a specific bin are displayed. 

### Intensity-based histogram
This plot is based on feature intensity instead of count. This procedure can reduce noise and amplify the influence of higher intensity mass features; a helpful feature as deconvolution algorithms often report invalid mass features with low abundance. Following the assignment of mass bins, summation of intensities for all mass feature pairs is performed, with the summed intensities of lower and higher mass feature pairs displayed above and below the x axis, respectively. This allows a rough estimation of the relative abundances of specific modifications present in the sample. 

### Intensity×Count histogram
The last plot constitutes a variation of the intensity-based plot that pushes emphasis towards mass features that are either high in intensity, frequency, or a combination of the two. By multiplying feature count by the sum intensity for each mass shift bin, commonly occurring mass shifts, or mass shifts observed with high intensity, are amplified. This enables for the rapid visual detection of auspicious mass differences that are otherwise difficult to pick out from background mass shifts. 


## References
- [Wu, Z.; Roberts, D.S.; Melby, J.A.; Wenger, K.; Wetzel, M.; Gu, Y.; Ramanathan, S.G.; Bayne, E.F.; Liu, X.; Sun, R.; Ong, I.M.; McIlwain, S.J.; **Ge, Y.** MASH Explorer: A Universal Software Environment for Top-Down Proteomics., *J. Proteome Res.*, 2020, 19 (9), 3867-3876.](https://pubmed.ncbi.nlm.nih.gov/32786689/)
- [Jeong, K., Kim, J., Gaikwad, M., Hidayah, S.N., Heikaus, L., Schlüter, H., and Kohlbacher, O. (2020). FLASHDeconv: Ultrafast, High-Quality Feature Deconvolution for Top-Down Proteomics. *Cell Syst.*, 10, 213-218.e6.](https://www.sciencedirect.com/science/article/pii/S2405471220300302)
- [Park, J., Piehowski, P.D., Wilkins, C., Zhou, M., Mendoza, J., Fujimoto, G.M., Gibbons, B.C., Shaw, J.B., Shen, Y., Shukla, A.K., Moore, R.J., Liu, T., Petyuk, V.A., Tolić, N., Paša-Tolić, L., Smith, R.D., Payne, S.H., and Kim, S. (2017). Informed-Proteomics: Open-source software package for top-down proteomics. *Nat. Methods*, 14, 909–914.](https://www.nature.com/articles/nmeth.4388)

## How to cite the script
If you are using the script, please cite:
...


## License
MSDIFF is available under the BSD license. See the LICENSE file for more info.
