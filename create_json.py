import argparse  # to give an argument when executing the script
import json

def main():
    parser = argparse.ArgumentParser(description='Script to write a json file')

    parser.add_argument('-outfile', '--output_file', dest='output_file', required=True,
                            type=str, help='Output file name')
    
    parser.add_argument('-ctf', '--cts_to_flux', dest='cts_to_flux', required=True,
                        type=float, help='Conversion ratio of count rate to flux (erg/cm^2/s)')

    parser.add_argument('-area_s', '--area_source', dest='area_source', required=True,
                        type=float, help='Area of the source region')

    parser.add_argument('-area_b', '--area_background', dest='area_background', required=True,
                            type=float, help='Area of the background region')

    parser.add_argument('-cts_s', '--counts_source', dest='cts_source', required=True,
                            type=float, help='Photon counts of the source region')

    parser.add_argument('-cts_b', '--counts_background', dest='cts_background', required=True,
                            type=float, help='Photon counts of the background region')

    parser.add_argument('-exp', '--exposure_time', dest='exposure_time', required=True,
                            type=float, help='Exposure time of the observation (s)')

    args = parser.parse_args()

    data = {
    "cts_to_flux": args.cts_to_flux,
    "area_source": args.area_source,
    "area_background": args.area_background,
    "counts_source": args.cts_source,
    "counts_background": args.cts_background,
    "exposure_time": args.exposure_time
    }


    with open(rf'{args.output_file}.json', "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print("Data for upper limit calculation stored in", args.output_file)

    with open(rf'{args.output_file}.json', "r", encoding="utf-8") as ffile:
        loaded_data = json.load(ffile)

    print("--- JSON FILE CONTENT ---")

    for name_var, value in loaded_data.items():
        print(f"{name_var}: {value}")

if __name__ == "__main__":
    main()