def main():

####################### exctracting data from csv #####################################
	import numpy as np
	import matplotlib.pyplot as plt
	import pandas as pd
	import statistics as statistics

	file = open("Supporting information CSV.csv","r")
	coeff = []
	no_atoms =  []
	no_H = []
	no_N = []
	no_O = []
	no_Cl = []
	no_S = []
	no_Br = []
	no_C = []
	func = []
	press = []
	kwg = []


	i = 0
	for line in file:
		if i > 1:
			line = line.strip()
			one_mol = line.split(',')
			no_atoms.append(int(one_mol[15]))
			coeff.append(float(one_mol[41]))
			kwg.append(float(one_mol[42]))
			no_Br.append(int(one_mol[14]))
			no_S.append(int(one_mol[13]))
			no_Cl.append(int(one_mol[12]))
			no_O.append(int(one_mol[11]))
			no_N.append(int(one_mol[10]))
			no_H.append(int(one_mol[9]))
			no_C.append(int(one_mol[8]))
			func.append(int(one_mol[30]))
			press.append(np.log10(float(one_mol[43])))
		i += 1

############################# no_atoms historgram ##################################################

	plt.rc('text', usetex='True')
	plt.rc('font', family='serif', size=18)
	plt.tight_layout()

	fig = plt.figure()
	n, bins, pathches = plt.hist(x=no_atoms, bins='auto', color='#0504aa', edgecolor='k')
	
	plt.xlabel("No Atoms", fontsize=18)
	plt.ylabel('Frequency', fontsize=18)
	plt.title('Number of Atoms in a Molecule', fontsize=18)
	fig.savefig('no_atoms.png',bbox_inches = "tight")


######################### no_atoms excluding hydrogen #########################################

	
	j = 0
	no_atoms_noH = []
	for atoms in no_atoms:
		atom_noH = atoms - no_H[j]
		no_atoms_noH.append(atom_noH)
		j += 1

	
	fig = plt.figure()
	plt.hist(x=no_atoms_noH, bins = bins, color = '#0504aa', alpha=0.75, edgecolor='k')
	
	plt.xlabel('Number of atoms in a molecule, excluding hydrogen')
	plt.ylabel('Frequency')
	plt.title('Number of Atoms Excluding Hydrogen')
	plt.grid(True)
	fig.savefig('no_atoms_noH.png',bbox_inches = "tight")
	


#################################### COSMOcoeffs WIOM  histogram #####################################



	hist_coeff, bin_edges_coeff = np.histogram(coeff)
	fig_coeff = plt.figure()

	plt.hist(x = coeff, bins = 'auto', facecolor = '#0504aa', edgecolor = 'k')

	plt.xlabel('log units')
	plt.ylabel('Frequency')
	plt.title('log($K_{WIOM/G}$)')
	fig_coeff.savefig('coeff.png',bbox_inches = "tight")

####################################### COSMOTherm KWG histogram #############################

	fig_kwg = plt.figure()

	n, bins_coeff, p = plt.hist(x = kwg, bins = 'auto', facecolor = 'blue', edgecolor = 'k')

	plt.xlabel('log(KWG)')
	plt.ylabel('Frequency')
	plt.title('COSMOtherm log(KW/G)')
	fig_kwg.savefig('kwg.png')





######tests ####

	#print(min(no_atoms), max(no_atoms))
	#print(min(coeff), max(coeff))

####### find the elements in the whole database ###
	
	oc_C = 0
	oc_H = 0
	oc_O = 0
	oc_N = 0
	oc_Cl = 0
	oc_S = 0
	oc_Br = 0

	for i in range(len(no_C)):
		if not  no_C[i] == 0:
			oc_C += 1
		if not  no_H[i] == 0:
			oc_H += 1
		if not no_S[i] == 0:
			oc_S += 1
		if not no_O[i]== 0:
			oc_O +=1 
		if not no_Cl[i] == 0:
			oc_Cl += 1
		if not no_N[i] == 0:
			oc_N += 1
		if not no_Br[i] == 0:
			oc_Br += 1

################## find no occurences and no of molecules #########################################

	amounts = [sum(no_C),sum( no_H),sum( no_N),sum( no_O),sum( no_Cl),sum( no_S),sum( no_Br)]
	no_mol = [oc_C, oc_H ,oc_N,oc_O,oc_Cl, oc_S, oc_Br]
	elements = ['C','H','N','O','Cl','S','Br']
	Z_exists = [6,1,7,8,17,16,35]
	no_mol1 = []
	Z = []
	j = 0
	for i in range(40):
		if i in Z_exists:
			no_mol1.append(no_mol[j])
			j += 1
		else:
			no_mol1.append(0)
		Z.append(i)

	bar = plt.figure()
	y_pos =  np.arange(len(elements))
	plt.bar(y_pos, amounts)
	plt.xticks(y_pos, elements)
	plt.ylabel('Number of atoms')
	plt.xlabel('Elements')
	plt.title('The Sum of Atoms of each Element in the Database')
	bar.savefig('element_division.png')


	bar1 = plt.figure()
	y_pos = np.arange(len(elements))
	plt.bar(elements, no_mol , align='center', color = '#0504aa', edgecolor = 'k')
	plt.title('Number of Occurences of the Elements')	
	plt.ylabel('No of Occurences')
	plt.xlabel('Elements')
	
	bar1.savefig('number_of_occurences.png',bbox_inches = "tight")

############################## find number of functional groups #########################################

	
	fig_func = plt.figure()
	fig_func.autolayout : True
	
	plt.hist(func, bins='auto', color = '#0504aa', edgecolor = 'k')	
	plt.xlabel('No Func')
	plt.ylabel('Frequency')
	plt.title('Number of functional Groups')
	fig_func.savefig('func.png', bbox_inches = "tight")

	
				
################################Pressure histogram#################################################
	
	x = press




#	print(press[0])
	fig_press = plt.figure()
	n, bins_pres, p = plt.hist(x, bins = 'auto', facecolor='#0504aa', edgecolor='k')

#	n, bins, patches = plt.hist(x=press, bins=100, color='#0504aa')	
#	plt.xlabel('Pressure kPa')
	plt.xlabel('log(kPa)')
	plt.ylabel('Frequency')
	plt.title('Log(Vapor Pressure)')
	
	fig_press.savefig('Pressure division.png',bbox_inches = "tight")	






main()
