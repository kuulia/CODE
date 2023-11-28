from rdkit import DataStructs
from rdkit import Chem
from os import path
import numpy as np
from rdkit.Chem import MACCSkeys

def main():

	filepath = path.relpath("CODE_2/data/geckoq_all")
	name_of_file = 'geckoq_smiles'
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
	fileoutname =  f'../CODE/CODE_2/data/geckoq_all/{name_of_file}_MACCS.txt'
	np.savetxt(fileoutname, matrix, fmt = "%s")

if __name__ == "__main__":
    main()