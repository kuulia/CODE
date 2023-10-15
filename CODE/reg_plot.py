import matplotlib.pyplot as plt
import numpy as np


version = str(4)
kernel_used = 'laplacian'
test_size = 414
target = 'kwiomg'
train_size = 3000



regcoorname = 'regression_plot_coordinates_' + str(train_size) + '_test_' + str(test_size) + '_' + target + '_' + kernel_used + '_' + version +  '.txt'

y_true = []
y_pred = []

file = open(regcoorname,'r')
for line in file:
	line = line.split()
	y_true.append(float(line[0]))
	y_pred.append(float(line[1]))
	
#y_true1 = np.array(y_true)

plt.rc('text', usetex='True')
plt.rc('font', family='serif')

#print(y_true)

regname = 'regression_plot_train_' + str(train_size) + '_test_' + str(test_size) + '_' + target + '_' + kernel_used + '_' + version +  '.png'
fig = plt.figure()
plt.scatter(y_true, y_pred, c='#0504aa')
plt.plot([0, 14], [0,14], 'k--', lw=1)
#fig.text(0, 0, '$R^2$= %.4f' % r2)
plt.title('Predicted vs. true log(KWIOMG)')
plt.xlabel('Reference log(KWIOMG)')
plt.ylabel('Predicted log(KWIOMG)')
fig.savefig(regname)



