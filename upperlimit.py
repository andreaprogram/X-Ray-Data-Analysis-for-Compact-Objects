# 对于FXT，计算流量上限时需要联合FXT-A/B的结果
# For FXT, we need to combine the results from FXT-A/B

from scipy.special import gammainc, gammaincc, gammaincinv

import re
import argparse
import json

parser = argparse.ArgumentParser(description='Script to obtain the upperlimit for the source')

parser.add_argument('-d', '--data', dest='data_file', required=True,
                    type=str, help='Path to the .json file containing data for modules a & b (e.g.: "upperlimit_data_ASKAP.json")')
 
args = parser.parse_args()

source_name = re.search(rf'upperlimit_data_(.*)\.json', args.data_file).group(1)

with open(args.data_file, "r", encoding="utf-8") as file:
    upperlimit_data = json.load(file)

# FXT-A data
nevts_src_A = upperlimit_data["a"]["cts_s"]  # FXT-A source region counts
alpha_A = upperlimit_data["a"]["area_s"] / upperlimit_data["a"]["area_b"]  # ratio of source area to background area for FXT-A
nevts_back_A = upperlimit_data["a"]["cts_b"]  # FXT-A background region counts
expo_time_A = upperlimit_data["a"]["exp"]  # FXT-A exposure
ctrt_to_absflux_A = upperlimit_data["a"]["ctf"]  # FXT-A conversion ratio from cts to flux, derived from `cts_to_flux.py`

# FXT-B data
nevts_src_B = upperlimit_data["b"]["cts_s"]  # FXT-B source region counts   
alpha_B = upperlimit_data["b"]["area_s"] / upperlimit_data["b"]["area_b"]
nevts_back_B = upperlimit_data["b"]["cts_b"]  # FXT-B background region counts
expo_time_B = upperlimit_data["b"]["exp"]  # FXT-B exposure
ctrt_to_absflux_B = upperlimit_data["b"]["ctf"]  # FXT-B conversion ratio from cts to flux, derived from `cts_to_flux.py`

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

print(f'X-ray flux upper limit for {source_name}: {absflux_UL_combined} erg*cm^-2*s^-1 (90% confidence level)')
