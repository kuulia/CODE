from dscribe.descriptors import MBTR
from dscribe.descriptors import CoulombMatrix
from ase.build import molecule
from ase.io import read
import numpy as np
import ase
import os
from ase.visualize import view
import matplotlib.pyplot as mpl
import ase.data

def main(k):
	element_list = ['C','O','N','H', 'Br', 'S', 'Cl']
	#sigma1 = 0.0001
	sigma2 = 0.0075
	sigma3 = 0.1
	filepath = os.path.relpath("CODE_2/data")
	name_of_file = 'all_edited'
	filename= os.path.join(filepath, name_of_file + '.xyz')
	xyz = open(filename, errors='ignore')
	inter= []
	elements = []
	coor = []
	e  = []

	for line in xyz:
		line = line.strip()
		s = line.split(' ')
		b = s[0] == ''
		if len(s) ==  1 and not b:
			coor.append(inter)
			elements.append(e)
			inter = []
			e = []
		if len(s) > 1:
			atom, x, y, z = line.split()
			e.append(atom)
			inter.append((float(x),float(y),float(z))) 
	coor.append(inter)
	elements.append(e)

	del coor[0]
	del elements[0]



	if (k == 1):
		mbtr = MBTR(
			species=element_list,
			periodic=False,
			geometry = {"function": "atomic_number"},
			grid = {"min": 0, "max": 1, 'n': 100, 'sigma': 0.1},
			weighting = {"function": "exp", "scale": 1.2, "threshold": 1e-3},
			sparse=False
		)
	if (k == 2):
		mbtr = MBTR(
			species=element_list,
			periodic=False,
			geometry =  {"function": "inverse_distance"},
			grid = {'min': 0, 'max': 2, 'n': 100, 'sigma': 0.1},
			weighting = {"function": "exp", "scale": 1.2, "threshold": 1e-3},
			sparse=False
			)
	if (k == 3):
		mbtr = MBTR(
			species=element_list,
			periodic=False,
			geometry =  {"function": "cosine"},
			grid = {'min': -1, 'max': 1, 'n': 100, 'sigma': 0.1},
			weighting = {"function": 'exp', "scale": 0.8, "threshold": 1e-3},
			sparse=False
		)
	if (k not in [1,2,3]):
		print('MBTR NOT GENERATED! Pass a valid value of k = 1, 2, or 3 as a parameter for generate_mbtr_edited')
	else:

		all_m = []

		for i in range(len(elements)):
			mole = ase.Atoms(elements[i],coor[i])
			mbtr_test = mbtr.create(mole)
			s = np.round(mbtr_test, decimals=3)
			all_m.append(s[0])

		h = np.array(all_m)



		#print(h.shape)
		#
		#
		#outname = 'all_mbtr_1_' + str(sigma1) +  '_2_' + str(sigma2) + '_3_' + str(sigma3) + '.txt'

		fileoutname = '../CODE/CODE_2/data/' + name_of_file + '_mbtr.txt'
		np.savetxt(fileoutname ,h, fmt="%s")


if __name__ == "__main__":
    main()