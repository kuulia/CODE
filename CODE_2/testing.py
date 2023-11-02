from funs import *
import pandas as pd
import numpy as np

#summarizer('MACCS_with_simpol', 'log_p_sat')

data = pd.read_clipboard()
print(data)
print(np.mean(data))

#0.345