from rdkit import DataStructs
from rdkit import Chem
import numpy as np





all_smi = open("all_smiles.txt",'r')

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

np.savetxt('all_fin.txt', matrix, fmt = "%s")

