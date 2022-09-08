import h5py
import hdf5plugin
import numpy as np
import matplotlib.pyplot as plt

mzafile = "test_data/LCMSMS_Lipids_POS.mza"

mza = h5py.File(mzafile, 'r')
# Reading Metadata table:
metadata = mza["Metadata"]

# Reading spectrum with scan number 2431, 2 jagged arrays with the intensity and mz values:
intensities = mza["Arrays_intensity/2431"][:]
print(intensities)
mz = mza["Arrays_mz/2431"][:]
print(mz)

mza.close()

# Plot spectrum:
fig = plt.figure()
ax = plt.axes()
ax.plot(mz, intensities)
plt.title("Scan number 2431 in test file LCMSMS_Lipids_POS.mza")
plt.xlabel("m/z")
plt.ylabel("Intensity")
plt.show()

