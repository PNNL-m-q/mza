__author__ = "Aivett Bilbao"
__date__ = "December 4, 2020"

from source.MZA_SpectrumInfo import *
from source.MZA import *
import os
import re
import pymzml
import numpy as np

class MzML2mza():
    
    def write_mza_from_mzml(self, ms_file, intensityThreshold = 1, output_mzafile=""):
        if(output_mzafile == ""):
            output_mzafile = ms_file.replace(".mzML" , ".mza")

        output_mzafile_meta_temp = output_mzafile.replace(".mza" , "_temp.mza")
        import h5py
        h5 = h5py.File(output_mzafile, 'w')

        import tables as tb
        h5meta_table = tb.open_file(output_mzafile_meta_temp, 'w')
        # create metadata table with predefined column names and types
        my_dtype = MZA_SpectrumInfo.get_types_metadata_array()
        tbh5 = h5meta_table.create_table(h5meta_table.root, name=MZA_Structure.metadata_table, description=my_dtype, filters=tb.Filters(complevel=5, complib='blosc'))

        # Define accession numbers for metadata, (add as extras if not included by default): MS Level (MS:1000511, included), Polarity (not included), Activation Method (not included),
        # Retention Time (MS:1000016, included), Precursor Scan (use precursors function), Precursor MZ (MS:1000744, not included), 
        # Precursor Charge (MS:1000041, not included), Isolation Window Target (MS:1000827, not included), 
        # Isolation Window Lower Offset (MS:1000828, included), Isolation Window Upper Offset (MS:1000829, included), TIC (calculated from spectra), Scan Label (MS:1000512, included)
        # Ion mobility time ("MS:1002476)
        extraAccessions = [
            ('MS:1000744', ['value']),  # Precursor MZ
            ('MS:1000041', ['value']),  # Precursor Charge
            ('MS:1000827', ['value']),  # Isolation Window Target
            ('MS:1000828', ['value']),  # Isolation Window Lower Offset
            ('MS:1000829', ['value']),  # Isolation Window Upper Offset
            ('MS:1000130', ['value']),  # Polarity, positive scan
            ('MS:1000129', ['value']),  # Polarity, negative scan
            ('MS:1000133', ['value']),  # Activation, collision-induced dissociation (CID)
            ('MS:1000422', ['value']),  # Activation, beam-type collision-induced dissociation (HCD)
            ('MS:1000045', ['value']),  # Collision energy
            ('MS:1002476', ['value'])   # Ion mobility time
        ]

        # Read mzML file 
        with pymzml.run.Reader(ms_file, extraAccessions = extraAccessions) as msfile:
            previousMS1 = 0
            seen_scan_ids = set()  # Track seen scan IDs
            scan_counter = 1       # Counter for generating unique scans
            
            for spectrum in msfile:
                spectrumInfo = MZA_SpectrumInfo()
                original_scan = spectrum.get('id')
                
                # Check if scan ID already exists, if so use counter
                if original_scan in seen_scan_ids:
                    scan = scan_counter
                else:
                    scan = original_scan
                
                scan_counter += 1
                seen_scan_ids.add(scan)
                spectrumInfo.scan_number = scan
                spectrumInfo.ms_level = int(spectrum.get('MS:1000511', 0))  

                if spectrum.get('MS:1000130'):
                    spectrumInfo.polarity = Polarity.POS
                if spectrum.get('MS:1000129'):
                    spectrumInfo.polarity = Polarity.NEG
    
                # TODO: add more activation/fragmentation methods
                if spectrumInfo.ms_level == 1:
                    spectrumInfo.fragmentation = Fragmentation.NotUsed
                elif spectrum.get('MS:1000133', 0):
                    spectrumInfo.fragmentation = Fragmentation.CID
                elif spectrum.get('MS:1000422', 0):
                    spectrumInfo.fragmentation = Fragmentation.HCD

                if spectrum.get('MS:1000045'):
                    spectrumInfo.collision_energy = int(spectrum.get('MS:1000045', 0))
                
                spectrumInfo.retention_time = spectrum.get('MS:1000016', 0)
                spectrumInfo.precursor_monoisotopic_mz = spectrum.get('MS:1000744', 0)
                spectrumInfo.precursor_charge = int(spectrum.get('MS:1000041', 0))
                spectrumInfo.isolation_window_target_mz = spectrum.get('MS:1000827', 0)
                spectrumInfo.isolation_window_lower_offset = spectrum.get('MS:1000828', 0)
                spectrumInfo.isolation_window_upper_offset = spectrum.get('MS:1000829', 0)
                spectrumInfo.tic = sum(spectrum.i)
            
                if spectrum.get('MS:1000512', 0):
                    spectrumInfo.scan_label = spectrum.get('MS:1000512', 0)

                if spectrum.get('MS:1002476', 0):
                    spectrumInfo.ion_mobility_time = spectrum.get('MS:1002476', 0)

                if spectrumInfo.ms_level == 1:
                    previousMS1 = scan
                else:
                    spectrumInfo.precursor_scan = previousMS1
                
                # Apply intensity threshold:
                indexes = np.argwhere(spectrum.i > intensityThreshold)
                intensities = spectrum.i[indexes].flatten()
                mzs = spectrum.mz[indexes].flatten()
                spectrumInfo.tic = sum(spectrum.i)

                if len(intensities) > 0:
                    tbh5.append(spectrumInfo.get_metadata_array()) # write spectrum metadata array
                    # write spectrum arrays:
                    h5.create_dataset(MZA_Structure.spectra_mz_arrays + "/" + str(scan), data=mzs)
                    h5.create_dataset(MZA_Structure.spectra_intensities_arrays + "/" + str(scan), data=intensities)
            msfile.close()

        h5.close()
        tbh5.flush()
        # copy metadata from temp h5 to final file and delete temp file
        h5 = tb.open_file(output_mzafile, 'a')
        metadata_tb = tbh5.read()
        h5.create_table(h5.root, name="Metadata", obj=metadata_tb, filters=tb.Filters(complevel=5, complib='blosc'))
        h5.flush()
        h5meta_table.close()
        h5.close()
        os.remove(output_mzafile_meta_temp)

        # Store mza info:
        usedparams = "intensityThreshold=" + str(intensityThreshold) + ", from " + os.path.basename(ms_file)
        MZA.save_mza_info(output_mzafile, usedparams) 

        return(output_mzafile)

        