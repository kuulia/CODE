from rdkit import DataStructs
from rdkit import Chem
from os import path
import numpy as np
from rdkit.Chem import MACCSkeys


def main(seed: int):

	filepath = path.relpath("CODE_2/data/geckoq3414")
	name_of_file = f'geckoq_smiles_sample_{seed}'
	filename= path.join(filepath, name_of_file + '.txt')
	all_smi = open(filename,'r')

	mol_train = [Chem.MolFromSmiles(x.strip()) for x in all_smi]

	fin_train = [MACCSkeys.GenMACCSKeys(x) for x in mol_train]

	matrix = []

	i = 0
	for on in fin_train:
		s = [on[i] for i in range(len(on))]
		if(i == 1):
			print(np.array(s).shape)
		i += 1
		matrix.append(s)
	fileoutname =  f'../CODE/CODE_2/data/geckoq3414/{name_of_file}_MACCS.txt'
	np.savetxt(fileoutname, matrix, fmt = "%s")

if __name__ == "__main__":
	random_seeds = [12,432,5,7543,12343,452,325432435,326,436,2435]
	for seed in random_seeds:
		main(seed)