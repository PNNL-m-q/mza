
# install.packages("BiocManager")
# BiocManager::install("rhdf5")
library(rhdf5)

# This data was converted from an Agilent .d ion mobility data file:
#   For IM spectra, the m/z dimension is stored as indexes (mzbins) of a single full m/z array common for all spectra in the file.
#   Note: IonMobilityBin = 0, represents the total frame spectrum or summed spectra in the frame (i.e., ignores IM dimension).
mzafile = "test_data/LowHigh_PC_160_180_frames1-10.mza"

# Print HDF5 file groups:
h5ls(mzafile, recursive = FALSE)

# Read metadata table:
metadata = data.frame(h5read(mzafile, "Metadata"))
summary(metadata)

# Reading spectrum from row 585 in metadata table:
#   conrresponds to scan ID 630 (RT 0.25 min, IM 15.6 ms)
#   contains base peak ion 121.05 m/z
scanRow = 586
scanID = metadata$Scan[scanRow]
mzaPath = as.character(metadata$MzaPath[scanRow])
print(scanID)

# 2 jagged arrays with the intensity and mzbin values:
intensity = h5read(mzafile, paste0("Arrays_intensity", mzaPath, "/", scanID)) # Array at "Arrays_intensity/630" in mza file
mzbins = h5read(mzafile, paste0("Arrays_mzbin", mzaPath, "/", scanID)) # Array at "Arrays_mzbin/630" in mza file

# Get array of m/z values (common for all spectra in the file) and map mzbins to m/z:
full_mz = h5read(mzafile, "Full_mz_array")
mz = full_mz[mzbins + 1] # +1 for R's 1-indexing
print(mz[which.max(intensity)]) # to check base peak ion 121.05 m/z


plot(x=mz, 
     y=intensity, 
     type="h", lwd=1,xlab="m/z",
     ylab="Intensity", yaxs="i")

