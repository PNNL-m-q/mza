# MZA: mass-to-charge (m/z) generic data storage and access tool

Untargeted mass spectrometry (MS)-based workflows incorporating orthogonal separations, such as liquid chromatography (LC) and ion mobility spectrometry (IM), and collecting extensive fragmentation data with data-independent acquisition (DIA) methods or alternative activation techniques, are providing heterogeneous and multidimensional information which allows deeper understanding in omics studies. However, the large volume of these rich multidimensional spectra challenges current MS-data storage and access technologies. The cross-platform and cross-programming language tool, MZA™ (pronounced m-za), was created to facilitate software development and artificial intelligence research in these kind of multidimensional MS data.

MZA is a stand-alone and self-contained command-line executable which converts multidimensional MS data from files in proprietary vendor formats to the MZA simple data structure based on the HDF5 format.
Once converted, MZA files can be easily accessed from any programming language and operating system using standard HDF5 libraries available (e.g., h5py and rhdf5).

### Input formats supported:
* Agilent MassHunter ion mobility '.d'
* Thermo '.raw'
* mzML

### Parameters:

#### Required
* -file arg: The raw MS file to be converted.

#### Optional:
* -extension arg: Input file extension. To convert multiple files in a path provide the extension: .mzML, .raw or .d.
* -intensityThreshold arg: The minimum intensity that must be exceeded for signals to be included in the output mza file.

### USAGE: data conversion

#### Windows
Tested on Windows 10. The MZA executable has no requirememts, it can be run directly on Windows. Examples:

Convert a single '.d' file:<br />
```bash
mza -file test_data\LowHigh_PC_160_180_frames1-10.d -intensityThreshold 20
```

Convert all '.d' files in a directory:<br />
```bash
mza -file test_data -extension .d -intensityThreshold 20
```

#### Unix-like operating systems
Tested on Ubuntu version 22.04.1. For Unix-like operating systems, the MZA executable requires pre-installation of the Wine compatibility layer (www.winehq.org).

1. Install Wine (tested version 6.0.3):
```bash
sudo apt-get install wine
```

2. Download and install wine-mono.msi from the official WineHQ site: https://dl.winehq.org/wine/wine-mono/ (tested version 7.3.0):
```bash
wine64 uninstaller
```

3. Press install from the uninstaller GUI and select the downloaded .msi package. Click ok.

Examples:

Convert a single '.d' file:<br />
```bash
wine mza -file test_data\LowHigh_PC_160_180_frames1-10.d -intensityThreshold 20
```

Convert all '.d' files in a directory:<br />
```bash
wine mza -file test_data -extension .d -intensityThreshold 20
```

### USAGE: data access in .mza files

Example scripts are provided in the respective folders. R requires the rhdf5 package and Python requires the h5py, hdf5plugin, numpy and matplotlib packages (see requirements.txt).

### Metadata table columns

| Column name |    Data type  | Values/units  |
| ------      | -----------   | ------  |
| Scan        | numeric     |  |
| MSLevel     | numeric     | 1:MS1, 2:MS2  |
| Polarity    | character   | POS, NEG |
| Activation  | character   | CID, HCD, ETD, UVPD, EThcD |
| RetentionTime | numeric    | minutes |
| PrecursorScan | numeric    |  |
| PrecursorMonoisotopicMz | numeric    |  |
| PrecursorCharge | numeric    |  |
| IsolationWindowTargetMz | numeric    |  |
| IsolationWindowLowerOffset | numeric    |  |
| IsolationWindowUpperOffset | numeric    |  |
| TIC | numeric    |  |
| SpectrumTitle  | character   |  |
| IonMobilityFrame | numeric    |  |
| IonMobilityBin | numeric    |  |
| IonMobilityTime | numeric    | milliseconds |

### Contact

aivett.bilbao@pnnl.gov

### Reference

If you use MZA please cite: Bilbao et al. "MZA: a data conversion tool to facilitate software development and artificial intelligence research in multidimensional mass spectrometry". Submitted.

### License addendum
This software binary and example scripts are freely provided under the BSD License here included. 
However, the binary software depends on other software libraries which place further restrictions on its use and redistribution. 
By using MZA, you agree to comply with the restrictions imposed on you by the license agreements of the software libraries on which it depends:
* Agilent Mass Hunter Data Access Component Library (www.agilent.com)
* Thermo-Scientific MSFileReader Library (www.thermofisher.com)
