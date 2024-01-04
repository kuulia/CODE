#Author: Emma Lumiaro as part of Lumiaro et al. (2021) https://doi.org/10.5194/acp-21-13227-2021
#Edited by Linus Lind Jan. 2024 as part of a Bachelor's thesis. Changes include
#but not limited to:
#filepath organization & code refactoring
#LICENSED UNDER: Creative Commons Attribution-ShareAlike 4.0 International
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