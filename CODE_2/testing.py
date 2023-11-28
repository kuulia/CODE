from funs import *
import pandas as pd
import numpy as np
#summarizer('MACCS', 'log_p_sat')

data1 = pd.read_csv('CODE_2/data/simpol/32k_Mol4SIMPOL.csv')
data1 = data1.drop(columns=['compound'])
data2 = pd.read_csv('CODE_2/data/geckoq_smiles.txt', header=None)
data2.columns=['SMILES']

#comparison = data1.compare(data2)
print('\n############################\n32k_Mol4SIMPOL is')
print(data1)
print('\n############################\n GeckoQ dataframe is:')
print(data2)
print(comparison)