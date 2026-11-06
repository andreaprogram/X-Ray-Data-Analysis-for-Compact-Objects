# 对于FXT，计算流量上限时需要联合FXT-A/B的结果
# For FXR, we need to combine the results from FXT-A/B

from os import CLD_CONTINUED
from scipy.special import gammainc, gammaincc, gammaincinv

import argparse
import json

parser = argparse.ArgumentParser(description='Script to obtain the upperlimit for the source')

parser.add_argument('-d', '--data', dest='data_file', required=True,
                    nargs='+', type=str, help='Path to the .json files for modules a & b (e.g.: "fxt_a_ASKAP.json")')
 
args = parser.parse_args()

files = args.data_file

for file in files:
    with open(file, "r", encoding="utf-8") as file:
        loaded_data = json.load(file)

    
    

nevts_src_A = 3  # FXT-A source region counts
alpha_A = 1028.31 / 12152.8  # ratio of source area to background area for FXT-A
nevts_back_A = 13 # FXT-A background region counts
expo_time_A = 6857 # FXT-A exposure

nevts_src_B = 2
alpha_B = 1028.31 / 12152.8
nevts_back_B = 24
expo_time_B = 6857

ctrt_to_absflux_A = 4.2774359817707715e-11 # FXT-A counversion ratio from cts to flux, derived from `cts_to_flux.py`

ctrt_to_absflux_B = 3.9740334781367714e-11

CL = 0.9  # 置信度(confidence level)

# -------------------------------------------------------

N = nevts_src_A + nevts_src_B
B = nevts_back_A * alpha_A + nevts_back_B * alpha_B
C_1 = gammaincc(N+1, B)
sC_1 = gammainc(N+1, B)
part1 = gammaincinv(N+1, CL*C_1 + sC_1)
UL = part1 - B #count's upper limit
absflux_UL_combined = UL/(expo_time_A*1.0/ctrt_to_absflux_A + expo_time_B*1.0/ctrt_to_absflux_B)
# unabsflux_UL_combined = UL/(expo_time_A*1.0/ctrt_to_unabsflux_A + expo_time_B*1.0/ctrt_to_unabsflux_B)

print(absflux_UL_combined)
