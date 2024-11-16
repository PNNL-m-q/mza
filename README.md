# MZA: mass-to-charge (m/z) generic data storage and access tool

<div align="center">
<mark><strong>-> Download the latest mza.exe version from the <a href="https://github.com/PNNL-m-q/mza/releases">releases</a>.</strong></mark>
</div>

MZA is a stand-alone and self-contained command-line executable which converts multidimensional mass spectrometry (MS) data from files in proprietary vendor formats to the MZA simple data structure based on the HDF5 format.
Once converted, MZA files can be easily accessed from any programming language and operating system using generic HDF5 libraries available (e.g., h5py and rhdf5).

Untargeted MS-based workflows incorporating orthogonal separations, such as liquid chromatography (LC) and ion mobility spectrometry (IM), and collecting extensive fragmentation data with data-independent acquisition (DIA) methods or alternative activation techniques, are providing heterogeneous and multidimensional information which allows deeper understanding in omics studies. However, the large volume of these rich multidimensional spectra challenges current MS-data storage and access technologies. The cross-platform and cross-programming language tool, MZA (pronounced m-za), was created to facilitate software development and artificial intelligence research in these kind of multidimensional MS data.

### Input formats supported:
* Agilent '.d' (with or without ion mobility)
* Bruker ion mobility 'd' (with ion mobility)
* Thermo '.raw'
* mzML

### Parameters:

#### Required
* -file arg: The raw MS file to be converted.

#### Optional:
* -extension arg: Input file extension. To convert multiple files in a path provide the extension: .mzML, .raw or .d.
* -intensityThreshold arg: The minimum intensity that must be exceeded for signals to be included in the output mza file.

## USAGE: data conversion 
Download the latest version (Releases section, right panel) and decompress it.

### Windows
Tested on Windows 10. The MZA executable has no requirements, it can be run directly on Windows. Examples:

Convert a single '.d' file:<br />
```bash
mza -file test_data\LowHigh_PC_160_180_frames1-10.d -intensityThreshold 20
```

Convert all '.d' files in a directory:<br />
```bash
mza -file test_data -extension .d -intensityThreshold 20
```

### Unix-like operating systems - Using Docker container

Build the container:
```bash
docker build -t mzacontainer:latest -f docker/Dockerfile .
```

Run the container:
```bash
docker run -it --rm -e WINEDEBUG=-all -v test_data:/data mzacontainer wine mza.exe -file /data/LCMSMS_Lipids_POS.raw
```

### Unix-like operating systems - Using Wine
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

## USAGE: data access in .mza files

The MZA file structure is simple: a metadata table and two groups with 1D arrays stored individually as HDF5 datasets per spectrum.
* Metadata (HDF5 dataset): each row in the metadata table (see csv files in test_data) represents a spectrum and the columns represent the properties of the spectrum such as scan number (unique to each spectrum), MS level, activation (i.e., ion fragmentation type), retention time, ion mobility arrival time, etc. 

Spectra are stored omitting zero-intensity values and as two jagged arrays, one in each corresponding group and named as the "Scan" value in the metadata table:
* Arrays_intensity (HDF5 group): contains 1D arrays with intensity values.
* Arrays_mz (HDF5 group): contains 1D arrays with mass-to-charge (m/z) values.
>Example for spectrum with Scan value 630: Arrays_intensity/630, Arrays_mz/630.

For IM spectra the m/z dimension is stored as indexes (mzbins):
* Arrays_mzbin (HDF5 group): contains 1D arrays with indexes to Full_mz_array.
* Full_mz_array (HDF5 dataset): 1D array of full m/z values common for all spectra in the file.
Note: IonMobilityBin = 0, represents the total frame spectrum or summed spectra in the frame (i.e., ignores IM dimension).
>Example for spectrum with Scan value 630: Arrays_intensity/630, Arrays_mzbin/630.


### Examples Python and R
Example scripts are provided in the respective folders. R requires the rhdf5 package and Python requires the h5py, hdf5plugin, numpy and matplotlib packages (see requirements.txt).

Example scripts for visualization of mobility distributions from total (or mass extracted) ion intensities in the raw data in mza files can be found is this [repository](https://github.com/EMSL-Computing/CCSz-demo) described in this [paper](https://doi.org/10.1002/pmic.202200436).

### CCS calibration coefficients:
These are included as an HDF5 dataset if detected during conversion to MZA
* CCScalDT = [Tfix, Beta] for Agilent DT
* CCScalSLIM = [C0, C1, C2, C3] for SLIM
* CCScalTIMS = [C0, C1, C2, C3, C4, C5, C6, C7, C8, C9] for Bruker TimsTOF

### Metadata table columns

| Column name |    Data type  | Values/units  |
| ------      | -----------   | ------  |
| Scan        | numeric     |  |
| MzaPath    | character   | Empty string or partition index of the HDF5 group to access arrays of the scan (*) |
| MSLevel     | numeric     | 1:MS1, 2:MS2  |
| Polarity    | character   | POS, NEG |
| Activation  | character   | CID, HCD, ETD, UVPD, EThcD |
| CollisionEnergy | numeric     |  |
| RetentionTime | numeric    | minutes |
| PrecursorScan | numeric    |  |
| PrecursorMonoisotopicMz | numeric    |  |
| PrecursorCharge | numeric    |  |
| IsolationWindowTargetMz | numeric    |  |
| IsolationWindowLowerOffset | numeric    |  |
| IsolationWindowUpperOffset | numeric    |  |
| TIC | numeric    |  |
| SpectrumTitle  | character   |  |
| IonMobilityFrame | numeric    | Index for RT |
| IonMobilityBin | numeric    |  |
| IonMobilityTime | numeric    | Arrival time in milliseconds for DT and SLIM; 1/k0 in Vs/cm2 for TimsTOF |

(*) Partitions may be created for files with too many spectra. Having too many datasets within a single group can slow down data reading performance. HDF5 is more efficient when using multiple groups instead of storing many datasets within one group.
Example to access arrays for Scan=630 and MzaPath=1: Arrays_intensity1/630, Arrays_mzbin1/630

### Contact

aivett.bilbao@pnnl.gov

### Reference

If you use MZA or any portions of this code please cite: Bilbao et al. "MZA: a data conversion tool to facilitate software development and artificial intelligence research in multidimensional mass spectrometry". Journal of Proteome Research 2023 https://doi.org/10.1021/acs.jproteome.2c00313.

### License addendum
This software binary is provided free of charge (closed-source code due to restrictions from instrument vendors on their proprietary formats). 
The example scripts are freely provided under the BSD License here included. 
However, the software binary depends on other software libraries which place further restrictions on its use and redistribution. 
By using MZA, you agree to comply with the restrictions imposed on you by the license agreements of the software libraries on which it depends:
* Agilent Technologies Mass Hunter Data Access Component Library (www.agilent.com)
* Thermo Fisher Scientific MSFileReader Library (www.thermofisher.com)
* Bruker TDF-SDK data access library (www.bruker.com)
