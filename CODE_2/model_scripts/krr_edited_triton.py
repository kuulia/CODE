#Author: Emma Lumiaro as part of Lumiaro et al. (2021) https://doi.org/10.5194/acp-21-13227-2021
#Edited by Linus Lind Jan. 2024 as part of a Bachelor's thesis. Changes include
#but not limited to:
#filepath organization, code refactoring
#LICENSED UNDER: Creative Commons Attribution-ShareAlike 4.0 International
#used for running topfp on wang et al 2017 data set
import numpy as np
import sklearn
import matplotlib.pyplot as plt
import math
from os import path
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error


# input files for training (change these to appropriate)
def main(descriptor, target, seed):
    krr_regr(descriptor, target, seed)

def krr_regr(descriptor, target, seed):
    name_of_file = f'all_smiles_{descriptor}.txt'
    filepath = path.relpath("data")
    descriptor_filename = path.join(filepath, name_of_file)  # file of descriptors of the molecules (MBTR, CM, MACCS, Morgan, Topological etc.)
    target_property_filename = path.join(filepath, f'{target}.txt') # target property (log_p_sat, kwiomg, kwg etc.)

    # training sizes for producing learning curve (in increasing order)
    train_sizes = [500, 1000, 1500, 2000, 2500, 3000]

    # parameters 
    kernel_used = 'rbf' # kernel used in KRR ('rbf'- Gaussian, 'laplacian'- Laplacian)
    test_size = 414 # size of test set 
    #test_size = 383 # size of test set 
    random_seed = seed 
    cv = 5 # number of folds for KRR crossvalidation

    # search space for KRR hyperparameters
    alpha = np.logspace(-10,-1,10)
    gamma = np.logspace(-10,-1,10)


    ##################################################################################################################################



    X_data = np.genfromtxt(descriptor_filename)
    y_data = np.genfromtxt(target_property_filename)

    # obtaining test set
    X, X_test, y, y_test = train_test_split(X_data, y_data, train_size=len(X_data)- test_size, test_size=test_size, shuffle=True, random_state=random_seed)

    learning_curve_mae = []
    training_sets = []


    # obtaining training set so that smaller set is a subset of a larger one
    for train_size in reversed(train_sizes):
        if train_size < len(X):
            X_train, _, y_train, _ = train_test_split(X, y, train_size= train_size, test_size=1, shuffle=True, random_state=random_seed)
            X = X_train
            y = y_train
        else:
            X_train = X
            y_train = y
        training_sets.append([X_train,y_train])
    training_sets.reverse()



    # initializing outputfile and writing parameters in it
    outputfile = open(f'data/KRR_output/output_KRR_{descriptor}_{target}_{seed}.txt', 'w+')
    outputfile.write("Begin KRR training.... \n\n")

    outputfile.write("Training_sizes: " + str(train_sizes) + "\n\n")

    outputfile.write("Other parameters: \n")
    outputfile.write("Kernel used: " + kernel_used + '\n')
    outputfile.write("Test size: " + str(test_size) + '\n')
    outputfile.write("Random seed: " + str(random_seed) + '\n')

    outputfile.close()


    # starting loop for all training sizes
    for train_id in range(len(train_sizes)):

        train_size = train_sizes[train_id]
        X_train, y_train = training_sets[train_id]


        ################################ training the model #########################################################################


        tuned_parameters = [{'kernel':[kernel_used],'alpha': alpha, 'gamma': gamma}]

        # inializing grid search for crossvalidating optimal combination of hyperparameters
        grid_search = GridSearchCV(KernelRidge(), tuned_parameters, cv=cv, scoring='neg_mean_absolute_error', n_jobs=-1, verbose=1)

        # fitting the model
        grid_search.fit(X_train, y_train)

        ################################################################################################################################

        ############################### train predictions and errors ###################################################################

        # Prediction for training set
        y_pred_train = grid_search.predict(X_train)

        #MSE
        MSE_train = np.mean((y_pred_train - y_train)**2)

        #MAE
        MAE_train = mean_absolute_error(y_train, y_pred_train)

        #R2
        r2_train = r2_score(y_train, y_pred_train)

        ################################################################################################################################

        ################################## test predictions and errors #################################################################

        # Prediction for test set
        y_pred = grid_search.predict(X_test)

        #MSE
        MSE = np.mean((y_pred-y_test)**2)

        #MAE
        MAE = mean_absolute_error(y_test, y_pred)
        learning_curve_mae.append(MAE)

        #R2
        r2 = r2_score(y_test, y_pred)

        ################################################################################################################################


        # Recording optimal parameters and errors in outputfile
        gamma_opt = grid_search.best_params_.get("gamma")
        alpha_opt = grid_search.best_params_.get("alpha")

        outputfile = open(f'data/KRR_output/output_KRR_{descriptor}_{target}_{seed}.txt', 'a+')

        outputfile.write("\nTraining_size: " + str(train_size) + "\n\n")

        outputfile.write("Training Errors: \n")
        outputfile.write("Training MAE: " + str(MAE_train) + '\n')
        outputfile.write("Training r2: " + str(r2_train) + '\n')
        outputfile.write("Training MSE: " + str(MSE_train) + '\n\n')

        outputfile.write("Test Errors: \n")
        outputfile.write("Test MAE: " + str(MAE) + '\n')
        outputfile.write("Test r2: " + str(r2) + '\n')
        outputfile.write("Test MSE: " + str(MSE) + '\n\n')

        outputfile.write("Optimal parameters: \n")
        outputfile.write("Optimal alpha: " + str(alpha_opt) + '\n')
        outputfile.write("Optimal gamma: " +  str(gamma_opt) + '\n')
        outputfile.write("Best gridsearch score with optimal parameters: " + str(grid_search.best_score_) + '\n\n')

        outputfile.close()


    # scatterplot for largest training size
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=1)
    fig.text(0, 0, '$R^2$= %.4f' % r2)
    plt.title('Predicted vs. True', fontsize=18)
    ax.set_xlabel('Reference', fontsize=18)
    ax.set_ylabel('Predicted', fontsize=18)
    fig.savefig(f'data/plots/{descriptor}/plot_regr_{descriptor}_{target}_{seed}.png')



    # Plot learning curve 
    fig, ax = plt.subplots()
    ax.plot(train_sizes, learning_curve_mae, marker='o')
    plt.title('Learning Curve', fontsize=18)
    ax.set_xlabel('Train Size', fontsize=18)
    ax.set_ylabel('MAE', fontsize=18)
    fig.savefig(f'data/plots/{descriptor}/plot_learn_curve_{descriptor}_{target}_{seed}.png')

if __name__ == "__main__":
    main()