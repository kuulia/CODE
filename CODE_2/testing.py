from funs import *
import pandas as pd
import numpy as np
#summarizer('MACCS_with_simpol', 'log_p_sat', 'geckoq')
#summarizer('MACCS', 'log_p_sat', 'geckoq')
data = pd.DataFrame()
data['carbon number'] = list(range(1,64))
for i in range(0,6):
    data[f'C_bit{i+1}'] = data['carbon number'].apply(np.binary_repr, width = 6).map(lambda v: v[i])

#data['carbon number (binary)'] = data['carbon number'].apply(np.binary_repr, width = 6)
print(data)

def to_bin(x: int):
    binary = list(bin(x))
    return binary[2:]

def binary_encoded(df, element: str):
    for i in range(0,6):
        df[f'C_NO_bit'] = df[element].apply(to_bin[0])
    return 0