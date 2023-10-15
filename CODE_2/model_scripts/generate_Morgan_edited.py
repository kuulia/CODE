from rdkit import DataStructs
from rdkit import Chem
import numpy as np
from rdkit.Chem import MACCSkeys
from rdkit.Chem import AllChem

def main():

	all_smi = open("all_smiles.txt",'r')

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

	np.savetxt('all_fin.txt', matrix, fmt = "%s")

if __name__ == "__main__":
    main()