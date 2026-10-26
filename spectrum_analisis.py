import subprocess # to execute shell commands
import glob # to search files using paths
import argparse  # to give an argument when executing the script
import re


# 1. CONVERT LEVEL 0 DATA TO LEVEL 1 DATA USING THE fxtchain COMMAND----------------------------------
# FIRST, WE WOULD LIKE THE SCRIPT TO EXECUTE THE fxtchain COMMAND GIVEN THE ARGUMENTS:
# - path of the folder containing the data for the given observation
# - RA and DEC of the source
# - bkg and src region files

def main():
    parser = argparse.ArgumentParser(description="Script to analyse X_ray spectrum")
    parser.add_argument('-fol', '--data_folder', dest='input_folder', required=True,
                        type=str, help='Path to the folder containing the files to be processed (ej: "ep_fxt_*")')

    parser.add_argument('-ra', '--ra', dest='ra', required=True,
                        type=float, help='Right Ascension of the source (ej: 339.4962)')

    parser.add_argument('-dec', '--dec', dest='dec', required=True,
                        type=float, help='Declination of the source (ej: 53.2405)')

    args = parser.parse_args()

    folders = glob.glob(args.input_folder)

    if not folders:
        print(f"No files found for path: {args.input_folder}")

    for folder in folders:
        print(f"\n--- Data folder: {folder} ---")

        obs_id = (re.search(r'ep_fxt_(\d+)', folder)).group(1)

        products_files = glob.glob(f"{folder}/fxt/products/*.fits") # e.g. fxt_a_06800000900_ff_01_po_cl_3dc.fits
        
        for pfile in products_files:
            module = re.search(r'fxt_([a-b])_', pfile).group(1) 
            obs_mod = re.search(f'fxt_{module}_{obs_id}_([a-z]+)_', pfile).group(1) 
            
            print(f"Encontrado módulo {module} y modo {obs_mod} para el archivo {pfile}")

            src_file = glob.glob(f"{folder}/fxt/products/src_reg_fxt_{module}_{obs_id}_{obs_mod}*.reg") # e.g. src_reg_fxt_a_06800000900_ff_01_po_cl_3dc.reg
            bkg_file = glob.glob(f"{folder}/fxt/products/bkg_reg_fxt_{module}_{obs_id}_{obs_mod}*.reg")

            if not src_file or not bkg_file:
                print(f"Skipping {pfile}: Missing source or background .reg files.")
                continue
            
            fxt = [
                "fxtchain",
                f"indir={folder}",
                "outdir=.",
                "exitstage=2",
                "expr=ELV>5&&COR>6&&SAA==0&&DYE_ELV>30", 
                f"ra={args.ra}",
                f"dec={args.dec}",
                f"src{obs_mod}region={src_file[0]}",
                f"bkg{obs_mod}region={bkg_file[0]}"
            ]
            
            print(f"Command: {fxt}")

            try:
                subprocess.run(fxt, check=True)
            except subprocess.CalledProcessError as error:
                print(f"fxtchain error on {pfile}. Return code: {error.returncode}")
            except FileNotFoundError:
                print("Error: 'fxtchain' command not found in PATH.")
                return
        
if __name__ == "__main__":
    main()