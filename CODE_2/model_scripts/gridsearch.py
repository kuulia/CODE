#Author: Emma Lumiaro as part of Lumiaro et al. (2021) https://doi.org/10.5194/acp-21-13227-2021
import matplotlib
import numpy as np
import sys
import sklearn
import matplotlib.pyplot as plt
import math
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from sklearn.metrics import make_scorer
import sys
import time
from joblib import dump


################################### Load datasets ######################################################

#If only one run with one training size done set false and specify parameters here
run_in_loop = True

if run_in_loop:
	kernel_used = sys.argv[4]
	target = sys.argv[5]
	version = sys.argv[2]
	train_size = int(sys.argv[1])
	test_size = sys.argv[3]
else:
	kernel_used = 'rbf'
	target = 'kwiomg'
	version = str(0)
	train_size = 3000
	test_size = str(414)	
	os.system("mkdir reg_plots")
	os.system("mkdir models")	

sample_size = 3000


samplename = str(sample_size) +'_cm_' + target + '_' + kernel_used + '_' + version +  '.txt'
target_samplename = str(sample_size) + '_' + target + '_' + kernel_used + '_' + version + '.txt'

testname = 'test_' + test_size + '_cm_' + target + '_' + kernel_used +'_' + version + '.txt'
target_testname = 'test_' +  test_size + '_' + target + '_' + kernel_used + '_' + version + '.txt'


#loading data from files
X = np.genfromtxt("data/{}".format(samplename))
y = np.genfromtxt("data/{}".format(target_samplename))

cv = 5


################################ Split data in training and test set of defined size ###################

#shuffle=false, no shuffling done
if train_size < sample_size:
	X_train, noneed1, y_train, noneed2 = train_test_split(X, y, train_size= train_size, test_size= 100, shuffle=False)
else:
	X_train = X
	y_train = y

X_test = np.genfromtxt("data/{}".format(testname))
y_test = np.genfromtxt("data/{}".format(target_testname))

alpha = np.logspace(-10,-1,10)
gamma = np.logspace(-10,-1,10)

tuned_parameters = [{'kernel':[kernel_used],'alpha': alpha, 'gamma': gamma}]


scores = ['neg_mean_absolute_error']

grid_search = GridSearchCV(KernelRidge(), tuned_parameters, cv=cv, scoring='neg_mean_absolute_error', n_jobs=-1, verbose=0)

grid_search.fit(X_train, y_train)

gamma_opt = grid_search.best_params_.get("gamma") # saving best hyperparameters

alpha_opt = grid_search.best_params_.get("alpha")

if(train_size == sample_size):
	dump(grid_search,'models/savedmodel_'+version+'.joblib')

############## compute training error with best hyperparameters ###########################################################

y_true_train, y_pred_train = y_train, grid_search.predict(X_train)


#MSE
#MSE_train = np.mean((y_pred_train - y_true_train)**2)


#RMSE
#RMSE_train = math.sqrt(MSE_train)


#MAE
MAE_train = mean_absolute_error(y_true_train, y_pred_train)

#RMol_coeff.txt2
r2_train = r2_score(y_true_train, y_pred_train)

#################### compute test error with best hyperparameters ###################################

y_true, y_pred = y_test, grid_search.predict(X_test)



#MSE
#MSE = np.mean((y_pred-y_true)**2)


#RMSE
#RMSE = math.sqrt(MSE)


#MAE
MAE = mean_absolute_error(y_true, y_pred)

#R2
r2 = r2_score(y_true, y_pred)

############################### MAE_file ############################

tempfile = open("tempfile2_"+version+".txt", 'w+')
tempfile.write(str(MAE) + '\n')
tempfile.write(str(r2) + '\n')
tempfile.write(str(MAE_train) + '\n')
tempfile.write(str(r2_train) + '\n')
tempfile.write(str(alpha_opt) + '\n')
tempfile.write(str(gamma_opt) + '\n')
tempfile.write(str(grid_search.best_score_) + '\n')


tempfile.close()

if train_size == sample_size:
	regname = 'regression_plot_train_' + str(train_size) + '_test_' + str(test_size) + '_' + target + '_' + kernel_used + '_' + version +  '.png'
	fig, ax = plt.subplots()
	ax.scatter(y_true, y_pred)
	ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=1)
	plt.title('Predicted vs. true log(KW/G)', fontsize=18)
	ax.set_xlabel('Reference log(KW/G)', fontsize=18)
	ax.set_ylabel('Predicted log(KW/G)', fontsize=18)
	fig.savefig("reg_plots/{}".format(regname))

	regcoorname = 'regression_plot_coordinates_' + str(train_size) + '_test_' + str(test_size) + '_' + target + '_' + kernel_used + '_' + version +  '.txt'

### save x-y coordinates of predicted output to text file
	z = zip(y_true, y_pred)
	lis = list(z)
	with open("reg_plots/{}".format(regcoorname), 'w') as f:
		f.write('\n'.join('%.5f %.5f' % x for x in lis))







