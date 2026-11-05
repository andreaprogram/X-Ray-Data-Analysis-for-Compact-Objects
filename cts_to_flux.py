# 输出计数率到流量的转化因子，用于计算流量上限。
# generate the conversion ratio of count rate to flux, for calculating upper limit

import glob # to search files using paths
import argparse  # to give an argument when executing the script
import re

import xspec as xs

def main():

# ADD THE ARGUMENTS NEEDED FOR THE SCRIPT TO EXECUTE THE get_ctrt_to_flux FUNCTION:
    parser = argparse.ArgumentParser(description='Script to obtain the conversion ratio of count rate to flux')

    parser.add_argument('-src_grp', '--source_groupped', dest='source_groupped', required=True,
                    nargs='+', type=str, help='Path to the grp.pha files for modules a & b (e.g.: "fxt_a_06800000900_ff_01_po_3dc_grp.pha")')
 
    parser.add_argument('-energy_l', '--energy_low', dest='energy_low', required=True,
                        type=float, help='Lowest energy value for which to caluculate the flux (in keV, e.g.: 0.5)')

    parser.add_argument('-energy_h', '--energy_high', dest='energy_high', required=True,
                        type=float, help='Highest energy value for which to caluculate the flux (in keV, e.g.: 10.0)')

    parser.add_argument('-nH', '--nH', dest='nH', required=True,
                        type=float, help='Assumed hydrogen column density (in units of 1e22)')

    parser.add_argument('-g', '--gamma', dest='PhoIndex', required=True,
                        type=float, help='Assumed photon index of the powerlaw')

    args = parser.parse_args()

    def get_ctrt_to_flux(source_spec, energy_l, energy_h, nH, PhoIndex, get_unabs):
        xs.Xset.abund = 'wilm'
        xs.Fit.statMethod = 'cstat'
        spec = xs.Spectrum(source_spec)
        spec.ignore('**-%.1f %.1f-**'%(energy_l, energy_h))    # ignore the energies outside energy_l - energy_h
        spec.background = None
        model = xs.Model('tbabs*cflux*powerlaw')
        if not get_unabs:
            model = xs.Model('cflux*tbabs*powerlaw')
        model.TBabs.nH.values = nH
        model.cflux.Emin = energy_l
        model.cflux.Emax = energy_h
        model.cflux.lg10Flux = -6.0
        model.powerlaw.PhoIndex = PhoIndex
        model.powerlaw.norm = 1.0
        model.powerlaw.norm.frozen = True       # fix the normalization of the powerlaw to 1.0
        fakeit_kwargs = {}
        fakeit_kwargs['exposure'] = 10000
        fakeit_kwargs['correction'] = 1.0
        fakeit_kwargs['backExposure'] = 1.0
        fakeit_kwargs['fileName'] = 'temp_fake.pha'
        xs.AllData.fakeit(1, xs.FakeitSettings(**fakeit_kwargs))
        spec = xs.AllData(1)
        spec.ignore('**-%.1f %.1f-**'%(energy_l, energy_h))
        spec.show()
        model.show()
        ctrt = spec.rate[-1]
        flux = 10**(model.cflux.lg10Flux.values[0])
        xs.AllModels.clear()
        xs.AllData.clear()
        return flux/ctrt   # return: units of flux (erg/cm^2/s) per count rate (cts/s)

    results = []
    for file in args.source_groupped:
        convert_ratio = get_ctrt_to_flux(source_spec=file, # source specrtum (after grppha)
                                    energy_l=args.energy_low,  # lower limit of energy in keV
                                    energy_h=args.energy_high, # upper limit
                                    nH=args.nH,       # assmued NH value（in unit of 1e22）
                                    PhoIndex=args.PhoIndex,  # assumed photon index of the powerlaw
                                    get_unabs=True) # True: measures the upper limit before absorption
    
        results.append(f"Conversion ratio for {file}: {convert_ratio} erg*cm^{{-2}}/count")  # store the conversion ratio of count rate to flux

    print("\n--- CONVERSION RATIOS ---")
    for res in results:
        print(res)
        
if __name__ == "__main__":
    main()

