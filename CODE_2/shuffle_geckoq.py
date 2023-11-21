from funs import *
import pandas as pd
import numpy as np

random_seeds = [12,432,5,7543,12343,452,325432435,326,436,2435]

data = pd.read_csv('CODE_2/data/geckoq_smiles.txt', header=None)
print(data.head(10))
for seed in random_seeds:
    output = data.sample(n=3414, random_state=seed)
    output.to_csv(f'CODE_2/data/geckoq3414/geckoq_smiles_sample_{seed}.txt', index=False)
