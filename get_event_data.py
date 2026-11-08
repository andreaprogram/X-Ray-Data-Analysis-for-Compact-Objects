import subprocess
import argparse
import glob
import re

def main():
    parser = argparse.ArgumentParser(description='Script to get DATE-OBS, RA_OBJ, DEC_OBJ and EXPOSURE from event file')
    #parser.add_argument('-e', '--event-file', help='Path to the event file')

    parser.add_argument('-fol', '--data_folder', dest='input_folder', required=True,
                    type=str, help='Path to the folder containing the event files (e.g.: "ep_fxt_*")')

    args = parser.parse_args()

    folders = glob.glob(args.input_folder)

    if not folders:
        print(f"No files found for path: {args.input_folder}")

    for folder in folders:
        print(f"\n--- Data folder: {folder} ---")

        obs_id = (re.search(r'ep_fxt_(\d+)', folder)).group(1)

# FIRST, LOOK FOR THE EVENT FILES IN THE EVENT FOLDER
        event_files = glob.glob(f"{folder}/fxt/event/*.fits") # e.g. fxt_a_06800000900_ff_01_po_uf_evt_3dc

        for efile in event_files:
            # for a reference on the naming convention, check FXT Users Guide
            module = re.search(rf'fxt_([a-b])_', efile).group(1) # a
            obs_mod = re.search(rf'fxt_{module}_{obs_id}_([a-z]+)_', efile ).group(1) #ff
            filtr = re.search(rf'fxt_{module}_{obs_id}_{obs_mod}_(\d+)_', efile).group(1) # 01
            sat_mode = re.search(rf'fxt_{module}_{obs_id}_{obs_mod}_{filtr}_([a-z]+)_', efile).group(1) # po
            lev = re.search(rf'fxt_{module}_{obs_id}_{obs_mod}_{filtr}_{sat_mode}_uf_evt_([a-z0-9]+)', efile).group(1) #3dc
            
            # print(module, obs_mod, filtr, sat_mode, lev)  
              
            print(f"------ Event file found: fxt_{module}_{obs_id}_{obs_mod}_{filtr}_{sat_mode}_uf_evt_{lev}------")
            print(f"Telescope: FXT-{module}")
    
            values = ["DATE-OBS", "RA_OBJ", "DEC_OBJ", "EXPOSURE"]

            for v in values:
                result = subprocess.run([f'ftkeypar {efile} {v} ; pget ftkeypar value'], shell=True, capture_output=True, text=True)
                print(f"{v}: {result.stdout.strip()}")
    
if __name__ == "__main__":
    main()