import sys
import os

#loops the runs for learning curve multiple times and tabulates results automatically, however no parallelization

versions = [0,1,2,3,4,5,6,7,8,9]
descriptor = "mbtr"
kernel = 'rbf'
target = 'kwg'
test_size = 414

os.system("mkdir data")
os.system("mkdir reg_plots")
os.system("mkdir models")


for i in versions:
	start_loop = time.time()
	os.system("python3 MBTR_gridsearch_loop.py {} {} {} {} {}".format(i, test_size, target, kernel, descriptor))

data = []

for version in versions:
	filename = 'data_test_size_' + str(test_size) + '_' + target +'_' + kernel + '_' + str(version)  + '.txt'
	file = open(filename, 'r')	
	some_data = []
	for line in file:
		line = line.strip()
		al = line.replace('[','').replace(']','')
		s = al.split(',')
		k = []
		for n in s:		
			k.append(float(n))
		some_data.append(k)
	data.append(some_data)

dataname = 'data_test_size_' + str(test_size) + '_' + target +'_' + kernel + '.csv'
all_data = open(dataname, 'w+')

for b in range(len(some_data)):
	for c in range(len(k)):
		for a in range(len(data)):
			all_data.write(str(data[a][b][c]))
			all_data.write(',')
		all_data.write('\n')
	all_data.write('\n')	
	all_data.write('\n')
	all_data.write('\n')

all_data.close()



		
