
# install.packages("BiocManager")
# BiocManager::install("rhdf5")
library(rhdf5)

mzafile = "test_data/LCMSMS_Lipids_POS.mza"

# Print HDF5 file groups:
h5ls(mzafile, recursive = FALSE)

# Read metadata table:
metadata = data.frame(h5read(mzafile, "Metadata"))
summary(metadata)

# Reading spectrum from row 2250 in metadata table:
#   corresponds to scan ID 2251 (RT 18.02 min)
#   contains base peak ion 703.57 m/z
scanRow = 2251
scanID = metadata$Scan[scanRow]
mzaPath = as.character(metadata$MzaPath[scanRow])
print(scanID)

# 2 jagged arrays with the intensity and m/z values:
intensity = h5read(mzafile, paste0("Arrays_intensity", mzaPath, "/", scanID)) # Array at "Arrays_intensity/2251" in mza file
mz = h5read(mzafile, paste0("Arrays_mz/", mzaPath, "/", scanID)) # Array at "Arrays_mz/2251" in mza file
print(mz[which.max(intensity)]) # to check base peak ion 703.57 m/z

plot(x=mz, 
     y=intensity, 
     type="h", lwd=1,xlab="m/z",
     ylab="Intensity", yaxs="i")

