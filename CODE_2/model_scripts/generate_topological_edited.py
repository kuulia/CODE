from rdkit import DataStructs
from rdkit import Chem
import numpy as np
import os



def main():

	filepath = os.path.relpath("CODE_2/data")
	name_of_file = 'all_smiles'
	filename= os.path.join(filepath, name_of_file + '.txt')
	all_smi = open(filename,'r')

	mol_train = [Chem.MolFromSmiles(x.strip()) for x in all_smi]

	fin_train = [Chem.rdmolops.RDKFingerprint(x, fpSize=8192, minPath=1, maxPath=8, nBitsPerHash=16) for x in mol_train]

	matrix = []

	i = 0
	for on in fin_train:
		s = [on[i] for i in range(len(on))]
		if(i == 1):
			print(np.array(s).shape)
		i += 1
		matrix.append(s)

	fileoutname = '../CODE/CODE_2/data/' + name_of_file + '_TopFP.txt'
	np.savetxt(fileoutname, matrix, fmt = "%s")
if __name__ == "__main__":
    main()