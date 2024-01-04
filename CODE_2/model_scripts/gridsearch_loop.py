#Author: Emma Lumiaro as part of Lumiaro et al. (2021) https://doi.org/10.5194/acp-21-13227-2021
import time
start = time.time()
from sklearn.model_selection import train_test_split
import numpy as np
import os
import sys

def main(ver):
	#Here change the training sizes or decrease the amount of differenyt training sizes per each suffle, the data is shuffled and the biggest training size is save in the samplename-file. In the gridsearch smaller training sizes (if initialized here) aer obtained from the largest trainign size without shuffling so that all teh smaller training sizes are included in the bigger ones. 
	#This loop in the looped by averages a set number of times to make multiple runs, with different random seeds, there parameters can also be changed


	##################################initializing parameters ##############################################

	run_by_loop = False

	if run_by_loop:
		version = ver
		test_size = sys.argv[2]
		target = sys.argv[3]
		kernel = sys.argv[4]
		descriptor = sys.argv[5]
	else:
		version = ver
		test_size = 414
		target = 'kwg'
		kernel = 'rbf'
		descriptor = "Morgan"
		os.system("mkdir data")
		os.system("mkdir reg_plots")
		os.system("mkdir models")

	#gridsearch_loop.py 0

	random_state = [12,432,5,7543,12343,452,325432435,326,436,2435]
	train_size = 3000



	#############################input files#############################################################
	X = np.genfromtxt(f'../CODE/CODE_2/data/all_smiles_{descriptor}.txt') #change if you want to alter descriptor i.e. mbtr, all filter some out, not take all molecules
	non_log_y = np.genfromtxt(f'all_{target}.txt')

	if target == 'pressure':
		y = []
		for pres in non_log_y:
			y.append(np.log10(pres))
	else:
		y = non_log_y


	#####################################splitting largest training set ###################################

	X_train, X_test, y_train, y_test = train_test_split(X,y, train_size= train_size, test_size=test_size, random_state=random_state[int(version)], shuffle=True)

	testname =  f'test_{str(test_size)}_cm_{target}_{kernel}_{version}.txt'
	target_testname = f'test_{str(test_size)}_{target}_{kernel}_{version}.txt'

	samplename = f'{str(train_size)}_cm_{target}_{kernel}_{version}.txt'
	target_samplename = f'{str(train_size)}_{target}_{kernel}_{version}.txt'


	np.savetxt("data/{}".format(testname), X_test, fmt = '%s')
	np.savetxt("data/{}".format(target_testname), y_test,  fmt = '%s')
	np.savetxt("data/{}".format(samplename), X_train, fmt = '%s')
	np.savetxt("data/{}".format(target_samplename), y_train, fmt = '%s')

	################################initializing loop for different trainign sizes #############################

	samples = [500,1000,1500,2000,2500,3000] # change training sizes

	MAE = []
	MAE_train = []
	r2 = []
	r2_train = []
	alpha = []
	gamma = []
	score = []

	data_titles = ['mae', 'r2','mae_train','r2_train','alpha','gamma', 'crossval score']
	no_return_values = len(data_titles)

	data = []

	for j in range(no_return_values):
		data.append([])



	##################################looping over multiple training sizes determined above####################

	for k in samples:
		os.system("python3 gridsearch.py {} {} {} {} {}".format(k, version, str(test_size), kernel, target))
		temp2 = open('tempfile2_'+ version +'.txt', 'r')
		data[0].append(round(float(temp2.readline().strip()),3))
		data[1].append(round(float(temp2.readline().strip()),3))
		data[2].append(round(float(temp2.readline().strip()),3))
		data[3].append(round(float(temp2.readline().strip()),3))
		data[4].append(float(temp2.readline().strip()))
		data[5].append(float(temp2.readline().strip()))
		data[6].append(abs(float(temp2.readline().strip())))
		temp2.close()
		os.remove('tempfile2_'+ version +'.txt')

	dataname = 'data_test_size_' + str(test_size) + '_' + target +'_' + kernel + '_' + version  + '.txt'

		
	datafile = open(dataname, 'w+')

	for j in range(no_return_values):  
		datafile.write(str(data[j]) + '\n')
	datafile.write(str(random_state[int(version)]))

	datafile.close()

if __name__ == "__main__":
    main()