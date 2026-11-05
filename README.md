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
