from rdkit import DataStructs
from rdkit import Chem
import numpy as np
from os import path
from rdkit.Chem import MACCSkeys
from rdkit.Chem import AllChem

def main():

	filepath = path.relpath("CODE_2/data")
	name_of_file = 'all_smiles'
	filename= path.join(filepath, name_of_file + '.txt')
	all_smi = open(filename,'r')

	mol_train = [Chem.MolFromSmiles(x.strip()) for x in all_smi]

	fin_train = [AllChem.GetMorganFingerprintAsBitVect(x,2,nBits=2048) for x in mol_train]

	matrix= [] 

	i = 0
	for on in fin_train:
		s = [on[i] for i in range(2048)]
		if(i == 1):
			print(np.array(s).shape)
		i += 1
		matrix.append(s)
	
	fileoutname =  f'../CODE/CODE_2/data/{name_of_file}_morgan.txt'
	np.savetxt(fileoutname, matrix, fmt = "%s")

if __name__ == "__main__":
    main()