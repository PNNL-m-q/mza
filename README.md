# MZA: mass-to-charge (m/z) generic data storage and access tool

Untargeted mass spectrometry (MS)-based workflows incorporating orthogonal separations, such as liquid chromatography (LC) and ion mobility spectrometry (IM), and collecting extensive fragmentation data with data-independent acquisition (DIA) methods or alternative activation techniques, are providing heterogeneous and multidimensional information which allows deeper understanding in omics studies. However, the large volume of these rich multidimensional spectra challenges current MS-data storage and access technologies. MZA™ (pronounced m-za) was created to facilitate software development and artificial intelligence research in these kind of multidimensional MS data.

MZA is a stand-alone and self-contained command-line executable which converts multidimensional MS data from files in proprietary vendor formats to the MZA simple data structure based on the HDF5 format.
Once converted, MZA files can be easily accessed from any programming language and operating system using standard HDF5 libraries available (e.g., h5py and rhdf5).

### Input formats supported:
* Agilent MassHunter '.d'
* Thermo '.raw'
* mzML

### USAGE
mza.exe has been tested on Windows 10. Examples:

* Convert a single '.d' file:<br />
mza -file test_data\LowHigh_PC_160_180_frames1-10.d -intensityThreshold 20

* Convert all '.d' files in a directory:<br />
mza -file test_data -extension .d -intensityThreshold 20


### Contact

aivett.bilbao@pnnl.gov

### Reference

If you use MZA please cite: Bilbao et al. "MZA: a data conversion tool to facilitate software development and artificial intelligence research in multidimensional mass spectrometry". Submitted.
