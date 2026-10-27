import subprocess # to execute shell commands
import glob # to search files using paths
import argparse  # to give an argument when executing the script
import re


def main():

# 1. CONVERT LEVEL 0 DATA TO LEVEL 1 DATA USING THE fxtchain COMMAND----------------------------------
# FIRST, WE WOULD LIKE THE SCRIPT TO EXECUTE THE fxtchain COMMAND GIVEN THE ARGUMENTS:
# - path of the folder containing the data for the given observation
# - RA and DEC of the source
# - bkg and src region files

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
            # for a reference on the naming convention, check FXT Users Guide
            module = re.search(r'fxt_([a-b])_', pfile).group(1) # a
            obs_mod = re.search(f'fxt_{module}_{obs_id}_([a-z]+)_', pfile).group(1) #ff
            filter = re.search(f'fxt_{module}_{obs_id}_{obs_mod}_(\d+)_', pfile).group(1) # 01
            sat_mode = re.search(f'fxt_{module}_{obs_id}_{obs_mod}_{filter}_(\w+)_', pfile).group(1) # po
            lev = re.search(f'fxt_{module}_{obs_id}_{obs_mod}_{filter}_{sat_mode}_cl_(\w+)', pfile).group(1) #3dc
            
            print(f"Found module {module} and observation mode {obs_mod} for file {pfile}")

            src_file = glob.glob(f"{folder}/fxt/products/src_reg_fxt_{module}_{obs_id}_{obs_mod}_{filter}_{sat_mode}_cl_{lev}") # e.g. src_reg_fxt_a_06800000900_ff_01_po_cl_3dc
            bkg_file = glob.glob(f"{folder}/fxt/products/bkg_reg_fxt_{module}_{obs_id}_{obs_mod}_{filter}_{sat_mode}_cl_{lev}")

            if not src_file or not bkg_file:
                print(f"Skipping {pfile}: Missing corresponding source or background files.")
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
                f"bkg{obs_mod}region={bkg_file[0]}",
                f"module={module}"
                ]
            
            print(f"Command: {fxt}")

            try:
                subprocess.run(fxt, check=True)
            except subprocess.CalledProcessError as error:
                print(f"fxtchain error on {pfile}. Return code: {error.returncode}")
            except FileNotFoundError:
                print("Error: 'fxtchain' command not found in PATH.")
                return

# 2. GROUP SOURCE, BACKGROUND, RESPONSE AND EFFECTIVE AREA FILES USING THE grppha COMMAND----------------------------------
        
            grp = [
                "grppha",
                f"infile=fxt_{module}_{obs_id}_{obs_mod}_{filter}_{sat_mode}_src_{lev}.pha",     # e.g. fxt_b_06800000900_ff_01_po_src_3dc.pha
                f"outfile=fxt_{module}_{obs_id}_{obs_mod}_{filter}_{sat_mode}_{lev}_grp.pha",    # e.g. fxt_b_06800000900_ff_01_po_src_3dc_grp.pha
                (f"comm=group min 25 & "
                f"chkey BACKFILE fxt_{module}_{obs_id}_{obs_mod}_{filter}_{sat_mode}_bkg_{lev}.pha & "
                f"chkey RESPFILE fxt_{module}_{obs_id}_{obs_mod}_{filter}_{sat_mode}_src_{lev}.rmf & "
                f"chkey ANCRFILE fxt_{module}_{obs_id}_{obs_mod}_{filter}_{sat_mode}_src_{lev}.arf & exit")
            ]
                    # at least 25 counts per bin so that we can use gaussian statistics
                    # e.g. fxt_b_06800000900_ff_01_po_bkg_3dc.pha
                    # e.g. fxt_b_06800000900_ff_01_po_src_3dc.rmf
            try:
                subprocess.run(grp, check=True)
            except subprocess.CalledProcessError as error:
                print(f"grppha error on {pfile}. Return code: {error.returncode}")
            except FileNotFoundError:
                print("Error: 'grppha' command not found in PATH.")
                return

if __name__ == "__main__":
    main()