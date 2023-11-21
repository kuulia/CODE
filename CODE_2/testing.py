from funs import *
import pandas as pd
import numpy as np
#summarizer('MACCS', 'log_p_sat')

data = pd.read_csv('CODE_2/data/geckoq_smiles.txt', header=None)

output = data.sample(n=3414, random_state=99)
output.to_csv('CODE_2/data/geckoq_smiles_sample3414.txt', index=False)