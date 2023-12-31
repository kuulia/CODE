#Author: Linus Lind Jan. 2024
#LICENSED UNDER: Creative Commons Attribution-ShareAlike 4.0 International
#Modifies MACCS fingerprint to create MACCS & SIMPOL (1) descriptor
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

def main():

    filepath = path.relpath("CODE_2/data")
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
    groups.remove('carbon number')
    multiple_simpol_groups = pd.read_csv(path.join(filepath, \
                                                   'potential_simpol_groups.csv'))

    #print(potential_simpol_groups)
    #print(groups)

    data_simpol = data_simpol_raw[groups]
    #print(data_simpol)
    
    #create simpol fingerprint
    simpol_fp = generate_simpol_fingerprint(data_simpol)
    #print(simpol_fp)
    #print(all_simpol)
    maccs_with_simpol = data
    for key, group in enumerate(groups):
        maccs_key_to_replace = unused_keys[key]
        maccs_with_simpol.iloc[:, maccs_key_to_replace] = simpol_fp[group]
    #print(maccs_with_simpol)


    fileoutname =  f'../CODE/CODE_2/data/all_smiles_MACCS_with_simpol.txt'
    np.savetxt(fileoutname, maccs_with_simpol, fmt = "%s")
if __name__ == "__main__":
    main()