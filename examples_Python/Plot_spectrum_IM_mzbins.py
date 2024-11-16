import h5py
import hdf5plugin
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# This data was converted from an Agilent .d ion mobility data file:
#   For IM spectra, the m/z dimension is stored as indexes (mzbins) of a single full m/z array common for all spectra in the file.
#   Note: IonMobilityBin = 0, represents the total frame spectrum or summed spectra in the frame (i.e., ignores IM dimension).
mzafile = "test_data/LowHigh_PC_160_180_frames1-10.mza"

mza = h5py.File(mzafile, 'r')
print(list(mza.keys())) # h5py.File acts like a Python dictionary

# Reading Metadata table:
metadata = mza["Metadata"]
# Save metadata table as csv:
metadata = pd.DataFrame(np.array(metadata))
metadata.to_csv(mzafile.replace(".mza",".csv"), index=False)

# Reading spectrum from row 585 in metadata table:
#   conrresponds to scan ID 630 (RT 0.25 min, IM 15.6 ms)
#   contains base peak ion 121.05 m/z
scanRow = 585
scanID = metadata["Scan"][scanRow]
mzaPath = str(metadata["MzaPath"][scanRow], 'utf-8')
print(scanID)

# 2 jagged arrays with the intensity and mzbin values:
intensities = mza["Arrays_intensity" + mzaPath + "/" + str(scanID)][:] # Array at "Arrays_intensity/630" in mza file
mzbins = mza["Arrays_mzbin" + mzaPath + "/" + str(scanID)][:] # Array at "Arrays_mzbin/630" in mza file

# Get array of m/z values (common for all spectra in the file) and map mzbins to m/z:
full_mz = mza["Full_mz_array"][:]
mz = [full_mz[i] for i in mzbins]

mza.close()

# Plot spectrum:
fig = plt.figure()
ax = plt.axes()
ax.plot(mz, intensities)
plt.title("Scan ID 630 in test file LowHigh_PC_160_180_frames1-10.mza")
plt.xlabel("m/z")
plt.ylabel("Intensity")
plt.show()

