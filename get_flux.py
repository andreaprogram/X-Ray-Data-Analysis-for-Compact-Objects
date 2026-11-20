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

    energy_l=args.energy_low  # lower limit of energy in keV
    energy_h=args.energy_high # upper limit
    nH=args.nH       # assmued NH value（in unit of 1e22）
    PhoIndex=args.PhoIndex  # assumed photon index of the powerlaw
    get_unabs=True # True: measures the upper limit before absorption

    xs.AllModels.clear()
    xs.AllData.clear()

    xs.Xset.abund = 'wilm'      #updated ISM abundances
    xs.Fit.statMethod = 'chi'    #statistic used for parameter estimation 

    data_comm = " ".join([f"{i+1}:{i+1} {f}" for i, f in enumerate(args.source_groupped)]) # data 1:1 src_grp_a.pha data 2:2 src_grp_b.pha
    xs.AllData(data_comm)

    xs.AllData.ignore("bad")
    xs.AllData.ignore(f"**-{energy_l:.1f} {energy_h:.1f}-**")

    xs.Model('tbabs*cflux*powerlaw')
    model = xs.AllModels(1)

    model.TBabs.nH.values = nH
    model.TBabs.nH.frozen = True
    model.cflux.Emin = energy_l
    model.cflux.Emax = energy_h
    model.cflux.lg10Flux = -10.0
    model.powerlaw.PhoIndex = PhoIndex
    model.powerlaw.norm = 1.0
    model.powerlaw.norm.frozen = True       # fix the normalization of the powerlaw to 1.0

    # by default, xspec will use the same model and parameters for both data groups 
    xs.Fit.perform()
    xs.AllModels.show()  

    idx_flux = model.cflux.lg10Flux.index
    idx_gamma = model.powerlaw.PhoIndex.index
    xs.Fit.error(f"2.706 {idx_gamma} {idx_flux}")  # 90% confidence range, corresponding to an increase in chi2 of 2.706

    gamma = model.powerlaw.PhoIndex.values[0]
    gamma_low, gamma_high, _ = model.powerlaw.PhoIndex.error

    log_flux_low, log_flux_high, _ = model.cflux.lg10Flux.error
    
    flux = 10**(model.cflux.lg10Flux.values[0])
    flux_low = 10**log_flux_low
    flux_high = 10**log_flux_high
        
    print("\n--- CONVERSION RATIOS FOR FOLLOWING PARAMETERS ---")
    print(f"Energy range: {energy_l} - {energy_h} keV")
    print(f"nH: {nH} * 1e22 cm^-2 (fixed)")
    print(f"Photon index: {gamma:.5f} (-{gamma - gamma_low:.5f}, +{gamma_high - gamma:.5f})")
    print(f"Unabsorbed flux: {flux:.5e} (-{flux - flux_low:.5e}, +{flux_high - flux:.5e}) (erg/cm^2/s)")
    print(f"Statistic ({xs.Fit.statMethod}) : {xs.Fit.statistic:.2f} with {xs.Fit.dof} d.o.f.")
    
if __name__ == "__main__":
    main()

