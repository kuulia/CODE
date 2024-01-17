# Author: Linus Lind Jan. 2024
# LICENSED UNDER: Creative Commons Attribution-ShareAlike 4.0 International
import pandas as pd
import numpy as np 
import scipy
from os import path

# Function applying ideal gas law to convert between saturation vapour pressure
# p_sat to saturation mass concentration C*. 
# Units: p_sat -> log10(kPa), molar_mass -> g / mol, temp -> K
def log_psat_to_c(p_sat: float|int, \
                  molar_mass: float|int, \
                  temp: float|int) -> float: 
        R = scipy.constants.gas_constant # 8.3... Pa m^3 / (K mol)
        P = 10**(p_sat) * 1_000 # log10(kPa) -> Pa
        T = temp
        M = molar_mass
        C = (P * M) / (T * R)
        return C # units g / m^3 

def c_to_volatility_group(c: float|int) -> str:
    volatility_groups = ['ELVOC', 'LVOC', 'SVOC', 'IVOC', 'VOC']
    vol_donahue = np.array([3 * 10**(-4), 0.3, 300, 3 * 10**(6)]) # micro g / m^3
    vol_donahue = vol_donahue / 1_000_000 # unit conversion to g / m^3
    # construct list of tuples that corresponds to edges
    volatility_ranges = []
    for i, _ in enumerate(vol_donahue):
        if i < (len(vol_donahue) - 1):
            volatility_ranges.append((vol_donahue[i], vol_donahue[i+1]))
    if c <= vol_donahue[0]:
        return volatility_groups[0]
    if c >= vol_donahue[3]:
        return volatility_groups[4]
    i = 0
    max_range = volatility_ranges[i][1]
    while c > max_range:
        i += 1
        max_range = volatility_ranges[i][1]
    return volatility_groups[i+1]

def main():
    filepath = path.relpath(f'data')
    wang_data = pd.read_csv(f'{filepath}/all_smiles_molar_mass.csv')
    temp_wang = 298.15 # K
    wang_data['c'] = wang_data.apply(lambda x: log_psat_to_c(x['log_p_sat'], x['molar_mass'], temp_wang), axis=1)
    wang_data['volatility'] = wang_data.apply(lambda x: c_to_volatility_group(x['c']), axis=1)
    wang_data.to_csv(f'{filepath}/wang_data.csv', index=None)


if __name__ == "__main__":
    main()