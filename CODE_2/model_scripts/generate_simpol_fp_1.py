# Used to generate simpol -fingerprint to compare performance to MACCS + simpol
# This fingerprint will be run by main. Generates simpol fp based on whether
# simpol group exist (1) or not (0)
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

    fileoutname =  f'../CODE/CODE_2/data/all_smiles_simpol.txt'
    np.savetxt(fileoutname, simpol_fp, fmt = "%s")

if __name__ == "__main__":
    main()