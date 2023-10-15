import numpy as np
import sys
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
from sklearn.kernel_ridge import KernelRidge


sigma1 = [0.3, 0.1, 0.01, 0.001, 0.0001]
sigma2 = [0.3, 0.1, 0.01, 0.001, 0.0001]
w2 = [0,0.2,0.4,0.6,0.8,1.0,1.2,1.4]

alpha = np.logspace(-10,-1,10)
gamma = np.logspace(-10,-1,10)

coeff = np.genfromtxt('/l/lumiare1/MBTR_crossvalidation/500/500_kwiomg.txt')

target = 'kwiomg'

kernel_used = 'rbf'

w1 = sys.argv[1]

test_size = 414

cv = 5

tuned_parameters = [{'kernel':[kernel_used],'alpha': alpha, 'gamma': gamma}]

outfilename = 'mbtr_results_train_500_' + kernel_used +  '_' + w1 +'.txt'

outfile = open('500/{}/{}'.format(w1, outfilename), 'w+')

parameters = []
ones = []
twos = []
w1s = []
w2s = []
scores = []

for we2 in w2:
	for one in sigma1:
		for two in sigma1:
			inputfile = "mbtr_" + str(one)+ "_" + str(two)+ "_" + str(w1) + "_" + str(we2) + "_.txt"
			X = np.genfromtxt('500/{}/{}/{}/{}'.format(w1, we2, one, inputfile))	
			grid_search = GridSearchCV(KernelRidge(), tuned_parameters, cv=cv, scoring='neg_mean_absolute_error', n_jobs=-1, verbose=0)
			grid_search.fit(X, coeff)
			param = grid_search.best_params_
			score = grid_search.best_score_
			ones.append(one)
			twos.append(two)
			w1s.append(w1)
			w2s.append(we2)
			scores.append(score)
			result = [one, two, w1, we2, score, param]
			outfile.write(str(result) + '\n')
			parameters.append(result)


index_min = scores.index(max(scores))

outfile.write('Best parameters: SIGMA1: ' +  str(ones[index_min]) + '    SIGMA2:    ' + str(twos[index_min]) + '    w1:    ' + str(w1s[index_min]) + '    w2:    ' + str(w2s[index_min]) + '   SCORE:    ' + str(scores[index_min]) )

outfile.close()

