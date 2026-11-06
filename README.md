## file_prep.py
Input: 
- folder containing the level 1 FXT's data
  
  IMPORTANT: there must be src and bkg region files stored in the fxt/products folder with the naming convention: src_reg/bkg_reg_{product_file_name}
- ra and dec (in degrees) for given source
- optional: groupping for the spectrum files (int number)

Output:
- FXT's level 2 data files
- grp.pha file with the src.pha, bkg.pha, src.rmf, src.arf files to be used in XSPEC.
  By default, the output files will be stored at the same directory one is executing the script at.

## cts_to_flux.py
Input: 
- FXT-a and FXT-b grp.pha (no groupping in general)
- lowest and higher energy values for which to calculate the flux (keV)
- nH  (column density in units of 1e22)
- gamma (photon index value)

  
Output:
- Convertion ratio = Flux/Counts , per each module (a/b)

## create_json.py
Input:
- name of the source

  For each module a/b:
- photon counts to flux ratio convertion
- area of the src/bkg region
- counts of the src/bkg region
- exposure time

Output:
- upperlimit_data_{source}.json file containing all the information for both modules

## upperlimit.py
Input:
- upperlimit_data_{source}.json

Output:
- X-ray upperlimit for the source 
