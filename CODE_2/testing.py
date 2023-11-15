from funs import *
import pandas as pd
import numpy as np
#summarizer('MACCS', 'log_p_sat')

data = pd.read_csv('CODE_2/data/all_smiles_MACCS.txt')
no_dups = data.drop_duplicates()
print(no_dups)