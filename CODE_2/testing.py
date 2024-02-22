#Author: Linus Lind Jan. 2024
#GNU General Public License v3.0
#scratch work file for testing various functions, sanity checking etc.
#ignore! may contain broken code!
from funs import *
import pandas as pd
import numpy as np

data = pd.read_csv('SIMPOLgroups.csv')
#print(data)

out = pd.DataFrame()
out.insert(0, 'Pattern name', data['substructure'])
out.insert(1,'SMARTS pattern', data['pattern'])

out.to_latex('SMARTSpatts.tex', index=False)