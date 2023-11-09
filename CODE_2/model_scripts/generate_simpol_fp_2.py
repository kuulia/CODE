# Used to generate simpol -fingerprint to compare performance to MACCS + simpol
# This fingerprint will be run by main. Generates simpol fp based on whether
# simpol group exist (1) or not (0) and also if there is 2-4 instances of 
# a particular simpol group
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

def main():

    filepath = path.relpath("CODE_2/data")
    
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
    simpol_fp_multi = multiple_groups(data_simpol)
    #print(simpol_fp_multi)
    for new_group in simpol_fp_multi.columns:
        groups.append(new_group)
    #replace unused MACCS keys with simpol fingerprints
    #print(groups)

    all_simpol = simpol_fp.join(simpol_fp_multi)
    #print(all_simpol)


    fileoutname =  f'../CODE/CODE_2/data/all_smiles_simpol.txt'
    np.savetxt(fileoutname, all_simpol, fmt = "%s")
if __name__ == "__main__":
    main()