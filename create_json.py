#import argparse  # to give an argument when executing the script
import json


# Function to register la data per each module as inputs
def register_data(module):
    print("------Register data for FXT-", module.upper(),"------")
    return {
        "ctf": float(input("Conversion ratio of count rate to flux (erg*cm^{-2}/count): ")),
        "area_s": float(input("Area of the source region: ")),
        "area_b": float(input("Area of the background region: ")),
        "cts_s": int(input("Photon counts of the source region: ")),
        "cts_b": int(input("Photon counts of the background region: ")),
        "exp": float(input("Exposure time of the observation (s): "))
    }

def main():
    source_name = input("Source name: ")

    data_ab = {
        "a": register_data("a"),
        "b": register_data("b")
    }

    with open(rf'upperlimit_data_{source_name}.json', "w", encoding="utf-8") as file:
        json.dump(data_ab, file, indent=4, ensure_ascii=False)

    print("Data for upper limit calculation stored in", rf'upperlimit_data_{source_name}.json')

    with open(rf'upperlimit_data_{source_name}.json', "r", encoding="utf-8") as ffile:
        loaded_data = json.load(ffile)

    print("--- JSON FILE CONTENT ---")

    print(json.dumps(loaded_data, indent=4))


if __name__ == "__main__":
    main()