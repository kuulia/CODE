#Author: Linus Lind Jan. 2024
#LICENSED UNDER: Creative Commons Attribution-ShareAlike 4.0 International
#Modifies MACCS fingerprint to create MACCS & SIMPOL (3) descriptor
import numpy as np
import pandas as pd
from os import path

def generate_simpol_fingerprint(df):
    fingerprint = pd.DataFrame()
    simpol_groups = df.columns
    for group in simpol_groups:
        if (group != 'carbon number'):
            fingerprint[group] = np.where(df[group] >= 1, 1, 0)
    return fingerprint

def multiple_groups(df):
    simpol_groups = df.columns
    two_to_four_groups = pd.DataFrame()
    for group in simpol_groups:
        if (group != 'carbon number'):
            two_to_four_groups[f'({group})_2-4'] = np.where((df[group] >= 2)\
                                                  & (df[group] <= 4), 1, 0)
    two_to_four_groups = two_to_four_groups.\
            loc[:, (two_to_four_groups != 0).any(axis=0)] #remove zero-columns
    fp_out = two_to_four_groups
    return fp_out

def carbon_numbers(df):
    carbon = 'carbon number'
    carbons = pd.DataFrame()
    for carbon_no in range(np.min(df[carbon]), np.max(df[carbon]) + 1):
        carbons[f'C_NO={carbon_no}'] = np.where((df[carbon] == carbon_no), 1, 0)
    return carbons

def main():

    filepath = path.relpath("data")
    name_of_file = 'all_smiles_MACCS'
    filename= path.join(filepath, name_of_file + '.txt')

    data = pd.read_csv(filename, header=None, sep=' ')
    #print(data)
    
    #load unused keys
    unused_keys_raw = pd.read_csv(path.join(filepath, 'unused_keys.csv'))
    unused_keys = unused_keys_raw['key']
    #print(unused_keys)

    #load simpol groups
    data_simpol_raw = pd.read_csv(path.join(filepath, \
                                            'all_smiles_simpol_groups.csv'))
    #print(data_simpol_raw)

    potential_simpol_groups = pd.read_csv(path.join(filepath, \
                                                    'potential_simpol_groups.csv'))
    groups = list(potential_simpol_groups['Compound'])
    
    #print(potential_simpol_groups)
    #print(groups)

    data_simpol = data_simpol_raw[groups]
    #print(data_simpol)
    
    #create simpol fingerprint
    simpol_fp = generate_simpol_fingerprint(data_simpol)
    #print(simpol_fp)
    simpol_fp_multi = multiple_groups(data_simpol)
    carbons = carbon_numbers(data_simpol)
    #print(simpol_fp_multi)
    for new_group in simpol_fp_multi.columns:
        groups.append(new_group)
    for carbon in carbons.columns:
        groups.append(carbon)
    groups.remove('carbon number')
    #replace unused MACCS keys with simpol fingerprints
    #print(groups)

    all_simpol = simpol_fp.join(simpol_fp_multi)
    all_simpol = all_simpol.join(carbons)
    
    maccs_with_simpol = data
    for key, group in enumerate(groups):
        maccs_key_to_replace = unused_keys[key]
        maccs_with_simpol.iloc[:, maccs_key_to_replace] = all_simpol[group]
        
    fileoutname =  f'data/all_smiles_MACCS_with_simpol.txt'
    np.savetxt(fileoutname, maccs_with_simpol, fmt = "%s")
if __name__ == "__main__":
    main()