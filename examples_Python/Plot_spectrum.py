import h5py
import hdf5plugin
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

mzafile = "test_data/LCMSMS_Lipids_POS.mza"

mza = h5py.File(mzafile, 'r')
print(list(mza.keys())) # h5py.File acts like a Python dictionary

# Reading Metadata table:
metadata = mza["Metadata"]
# Save metadata table as csv:
metadata = pd.DataFrame(np.array(metadata))
metadata.to_csv(mzafile.replace(".mza",".csv"), index=False)

# Reading spectrum with scan number 2431, 2 jagged arrays with the intensity and mz values:
intensities = mza["Arrays_intensity/2431"][:]
mz = mza["Arrays_mz/2431"][:]

mza.close()

# Plot spectrum:
fig = plt.figure()
ax = plt.axes()
ax.plot(mz, intensities)
plt.title("Scan number 2431 in test file LCMSMS_Lipids_POS.mza")
plt.xlabel("m/z")
plt.ylabel("Intensity")
plt.show()

