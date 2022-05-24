

# BiocManager::install("rhdf5")
library(rhdf5)

mzafile = "test_data/LCMSMS_Lipids_POS.mza"


# Print HDF5 file groups:
h5ls(mzafile, recursive = FALSE)

# Read metadata table:
metadata = data.frame(h5read(mzafile, "Metadata"))
summary(metadata)


# Read and plot a spectrum:
scanNumber = 1000

mz = as.numeric(h5read(mzafile, paste("Arrays_mz/", scanNumber, sep = ''), compoundAsDataFrame = FALSE))

intensity = as.numeric(h5read(mzafile, paste("Arrays_intensity/", scanNumber, sep = ''), compoundAsDataFrame = FALSE))

plot(x=mz, 
     y=intensity, 
     type="h", lwd=1,xlab="m/z",
     ylab="Intensity", yaxs="i")

