import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description='Script to get DATE-OBS, RA_OBJ, DEC_OBJ and EXPOSURE from event file')
    parser.add_argument('-e', '--event-file', help='Path to the event file')
    args = parser.parse_args()

    values = ["DATE-OBS", "RA_OBJ", "DEC_OBJ", "EXPOSURE"]
    e_file = args.event_file

    for v in values:
        result = subprocess.run([f'ftkeypar {e_file} {v} ; pget ftkeypar value'], shell=True, capture_output=True, text=True)
       
        print(f"{v}: {result.stdout.strip()}")
    
if __name__ == "__main__":
    main()