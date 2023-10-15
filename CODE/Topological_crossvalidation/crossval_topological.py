import numpy as np
import os
import random
import sys
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
from sklearn.kernel_ridge import KernelRidge

si = sys.argv[1]
maxp = sys.argv[2] 

#size = [1024,2048,4096]
#max_p = [5,7,9,11]
min_p = [1,2]
bits = [3,4,5,6,7,8,9,10,11,12,13,14]

alpha = [0.01,0.001]
gamma = [0.01,0.001]

kernel_used = 'laplacian'

target = 'kwiomg'

cv = 5

test_size = 414

coeff = np.genfromtxt('1500/some_kwiomg.txt') 

tuned_parameters = [{'kernel':[kernel_used],'alpha': alpha, 'gamma': gamma}]

outfilename = 'RD_results_train_1500_' + kernel_used +  '_' + si  + '_' + maxp +'.txt'

outfile = open('1500/{}'.format(outfilename), 'w+')

parameters = []
mins = []
maxs = []
nbits = []
sizes = []
scores = []


for minp in min_p:
	for bit in bits:
		name = 'RD_' + str(si) + '_' + str(maxp) + '_' + str(minp) + '_' + str(bit) + '.txt'
		X = np.genfromtxt('1500/{}/{}/{}/{}'.format(si, maxp, minp, name))
		grid_search = GridSearchCV(KernelRidge(), tuned_parameters, cv=cv, scoring='neg_mean_absolute_error', n_jobs=-1, verbose=0)		
		grid_search.fit(X, coeff)
		param = grid_search.best_params_
		score = grid_search.best_score_
		mins.append(minp)
		maxs.append(maxp)
		sizes.append(si)
		nbits.append(bit)
		scores.append(score)
		result = [si, maxp, minp, bit, score, param]
		outfile.write(str(result) + '\n')
		parameters.append(result)
	
index_min = scores.index(max(scores))

outfile.write('Best parameters: Size: ' +  str(sizes[index_min]) + '    Max:    ' + str(maxs[index_min]) + '    MIN:    ' + str(mins[index_min]) + '    BIT:    ' + str(nbits[index_min]) + '   SCORE:    ' + str(scores[index_min]) )

outfile.close()
