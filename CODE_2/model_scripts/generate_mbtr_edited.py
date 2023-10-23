import sys
if (sys.version_info[0] == 3 and sys.version_info[1]!=8):
	print(f'####\nPlease run this script with Python 3.8 interpreter and use dscribe 1.2.2. Your python version is {sys.version}\n####')
else:
	# Run this with python 3.8 and dscribe 1.2.2!!!!!!!!!!!!
	from dscribe.descriptors import MBTR
	from ase.io import read
	import numpy as np
	import ase
	from os import path
	import ase.data

	def main():
		element_list = ['C','O','N','H', 'Br', 'S', 'Cl']
		#k=2
		sigma1 = 0.0001
		sigma2 = 0.0075
		sigma3 = 0.1
		scale2 = 1.2
		scale3 = 0.8
		filepath = path.relpath("CODE_2/data")
		name_of_file = 'all_edited'
		filename= path.join(filepath, name_of_file + '.xyz')
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
		mbtr = MBTR(
			species=element_list,
	#		k1={
	#			"geometry": {"function": "atomic_number"},
	#			"grid": {"min": 0, "max": 1, 'sigma': sigma1, 'n': 100,},
	#		},
			k2= {
				'geometry': {"function": "inverse_distance"},
				'grid': {'min': 0, 'max': 2, 'n': 100, 'sigma': 0.1},
				"weighting": {"function": "exp", "scale": scale2, "threshold": sigma2},
			},
				k3= {
					'geometry': {"function": "cosine"},
					'grid': {'min': -1, 'max': 1, 'n': 100, 'sigma': 0.1},
					"weighting": {"function": "exp", "scale": scale3, "threshold": sigma3},
			},
			sparse=False
		)


		"""if (k == 1):
			mbtr = MBTR(
				species=element_list,
				periodic=False,
				geometry = {"function": "atomic_number"},
				grid = {"min": 0, "max": 1, 'n': 100, 'sigma': sigma_opt},
				#weighting = {"function": "unity", "scale": 1.2, "threshold": 1e-3},
				sparse=False
			)
		if (k == 2):
			mbtr = MBTR(
				species=element_list,
				periodic=False,
				geometry =  {"function": "inverse_distance"},
				grid = {'min': 0, 'max': 2, 'n': 100, 'sigma': sigma_opt},
				weighting = {"function": "exp", "scale": 1.2, "threshold": 1e-3},
				sparse=False
				)
		if (k == 3):
			mbtr = MBTR(
				species=element_list,
				periodic=False,
				geometry =  {"function": "cosine"},
				grid = {'min': -1, 'max': 1, 'n': 100, 'sigma': sigma_opt},
				weighting = {"function": 'exp', "scale": 1.2, "threshold": 1e-3},
				sparse=False
			)
		if (k not in [1,2,3]):
			print('MBTR NOT GENERATED! Pass a valid value of k = 1, 2, or 3 as a parameter for generate_mbtr_edited')
		else:
			"""
		all_m = []

		for i, element in enumerate(elements):
			mole = ase.Atoms(element,coor[i])
			mbtr_test = mbtr.create(mole)
			s = np.round(mbtr_test, decimals=3)
			all_m.append(s)

		h = np.array(all_m)



		#print(h.shape)
		#
		#
		#outname = 'all_mbtr_1_' + str(sigma1) +  '_2_' + str(sigma2) + '_3_' + str(sigma3) + '.txt'

		fileoutname =  f'../CODE/CODE_2/data/{name_of_file}_mbtr.txt'
		np.savetxt(fileoutname ,h, fmt="%s")


	if __name__ == "__main__":
		main()