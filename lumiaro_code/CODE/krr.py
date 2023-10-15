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


################################### Set variables ######################################################


kernel_used = 'rbf'
target = 'kwiomg'
version = str(0)
train_size = 3000
test_size = str(414)	
sample_size = 3000


#############################Load data #############################################################

X = np.genfromtxt('all_'+ descriptor + '.txt') #change if you want to alter descriptor i.e. mbtr, all filter some out, not take all molecules
non_log_y = np.genfromtxt('all_' + target + '.txt')

if target == 'pressure':
	y = []
	for pres in non_log_y:
		y.append(np.log10(pres))
else:
	y = non_log_y


cv = 5


################################ Split data in training and test set of defined size ###################


X_train, noneed1, y_train, noneed2 = train_test_split(X, y, train_size= train_size, test_size= test_size, shuffle=True)


alpha = np.logspace(-10,-1,10)
gamma = np.logspace(-10,-1,10)

tuned_parameters = [{'kernel':[kernel_used],'alpha': alpha, 'gamma': gamma}]

scores = ['neg_mean_absolute_error']

grid_search = GridSearchCV(KernelRidge(), tuned_parameters, cv=cv, scoring='neg_mean_absolute_error', n_jobs=-1, verbose=0)

grid_search.fit(X_train, y_train)

gamma_opt = grid_search.best_params_.get("gamma") # saving best hyperparameters

alpha_opt = grid_search.best_params_.get("alpha")

#saves the trained model
dump(grid_search,'savedmodel_'+version+'.joblib')

############## compute training error with best hyperparameters ###########################################################

#make predictrions on the test set
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

rfile = open("results_"+ str(train_size) + '_test_' + str(test_size) + '_' + target + '_' + kernel_used + '_' + version + ".txt", 'w+')
rfile.write(str(MAE) + '\n')
rfile.write(str(r2) + '\n')
rfile.write(str(MAE_train) + '\n')
rfile.write(str(r2_train) + '\n')
rfile.write(str(alpha_opt) + '\n')
rfile.write(str(gamma_opt) + '\n')
rfile.write(str(grid_search.best_score_) + '\n')


rfile.close()


regname = 'regression_plot_train_' + str(train_size) + '_test_' + str(test_size) + '_' + target + '_' + kernel_used + '_' + version +  '.png'
fig, ax = plt.subplots()
ax.scatter(y_true, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=1)
plt.title('Predicted vs. true log(KW/G)', fontsize=18)
ax.set_xlabel('Reference log(KW/G)', fontsize=18)
ax.set_ylabel('Predicted log(KW/G)', fontsize=18)
fig.savefig("{}".format(regname))

regcoorname = 'regression_plot_coordinates_' + str(train_size) + '_test_' + str(test_size) + '_' + target + '_' + kernel_used + '_' + version +  '.txt'

### save x-y coordinates of predicted output to text file
z = zip(y_true, y_pred)
lis = list(z)
with open("{}".format(regcoorname), 'w') as f:
	f.write('\n'.join('%.5f %.5f' % x for x in lis))







