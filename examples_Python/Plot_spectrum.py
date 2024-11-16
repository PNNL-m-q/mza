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

# Reading spectrum from row 2250 in metadata table:
#   corresponds to scan ID 2251 (RT 18.02 min)
#   contains base peak ion 703.57 m/z
scanRow = 2250
scanID = metadata["Scan"][scanRow]
mzaPath = str(metadata["MzaPath"][scanRow], 'utf-8')
print(scanID)

# 2 jagged arrays with the intensity and m/z values:
intensities = mza["Arrays_intensity" + mzaPath + "/" + str(scanID)][:] # Array at "Arrays_intensity/2251" in mza file
mz = mza["Arrays_mz" + mzaPath + "/" + str(scanID)][:] # Array at "Arrays_mz/2251" in mza file

mza.close()

# Plot spectrum:
fig = plt.figure()
ax = plt.axes()
ax.plot(mz, intensities)
plt.title("Scan number 2251 in test file LCMSMS_Lipids_POS.mza")
plt.xlabel("m/z")
plt.ylabel("Intensity")
plt.show()

