#can be used to tabulate individual learning curves into one file 

import sys
import os


versions = [1,2,3,4,5]
test_size = 414
target = 'kwg'
kernel = 'rbf'

dataname = 'data_test_size_' + str(test_size) + '_' + target +'_' + kernel + '.csv'

all_data = open(dataname, 'w+')

data = []

random_state = -1


for version in versions:
	filename = 'data_test_size_' + str(test_size) + '_' + target + '_'+ kernel+'_' + str(version)  + '.txt'
	file = open(filename, 'r')	
	some_data = []
	for line in file:
		line = line.strip()
		al = line.replace('[','').replace(']','')
		s = al.split(',')
		if len(s) == 1:
			random_state = int(s[0])
		else:
			k = []
			for n in s:		
				k.append(float(n))
			some_data.append(k)
	data.append(some_data)
	#os.remove(filename)

for b in range(len(some_data)):
	for c in range(len(k)):
		for a in range(len(data)):
			all_data.write(str(data[a][b][c]))
			all_data.write(',')
		all_data.write('\n')
	all_data.write('\n')	
	all_data.write('\n')
	all_data.write('\n')


all_data.write("random_state:, {}\n".format(random_state))
all_data.close()

						

 
