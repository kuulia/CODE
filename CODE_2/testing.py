#Author: Linus Lind Jan. 2024
#GNU General Public License v3.0
#scratch work file for testing various functions, sanity checking etc.
#ignore! may contain broken code!
from funs import *
import pandas as pd
import numpy as np

data = pd.read_csv('data/mins_and_maxes.csv', index_col='Compound')
data = data[['Counts', 'Min', 'Max', 'Mean', 'Weighted_mean']]
print(data)
data.to_latex('data/mins_and_maxes.tex', float_format="%.3f")