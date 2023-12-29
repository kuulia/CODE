import pandas as pd
import numpy as np
from os import path 

def results(descriptor, target, seed, folder):
    filepath = path.relpath(f'data/KRR_output/{folder}')
    input_file = path.join(filepath,\
                            f'output_KRR_{descriptor}_{target}_{seed}.txt')
    read_file = open(input_file, 'r')
    lines = read_file.readlines()
    #input file row indexes:
    train_mae_lines = np.array([12, 30, 48, 66, 84, 102])
    train_r2_lines = train_mae_lines + 1
    train_mse_lines = train_mae_lines + 2

    test_mae_lines = train_mae_lines + 5
    test_r2_lines = test_mae_lines + 1 
    test_mse_lines = test_mae_lines + 2

    training_size_lines = train_mae_lines - 3 

    def lines_to_list(idx, lines, attr: str):
        out = []
        for line in idx:
            out.append(float(lines[line]\
                            .removeprefix(f'{attr}: ')\
                            .removesuffix('\n')))
        return out
    data = pd.DataFrame()
    data['Train_sizes'] = lines_to_list(training_size_lines, lines, \
                                        'Training_size')
    data['Train_sizes'] = data['Train_sizes'].astype(int)
    data['Train_MAE'] = lines_to_list(train_mae_lines, lines, 'Training MAE')
    data['Train_R2'] = lines_to_list(train_r2_lines, lines, 'Training r2')
    data['Train_MSE'] = lines_to_list(train_mse_lines, lines, 'Training MSE')
    data['Test_MAE'] = lines_to_list(test_mae_lines, lines, 'Test MAE')
    data['Test_R2'] = lines_to_list(test_r2_lines, lines, 'Test r2')
    data['Test_MSE'] = lines_to_list(test_mse_lines, lines, 'Test MSE')
    data.to_csv(path.join(filepath + '/results/', \
                          f'result_{descriptor}_{target}_{seed}.csv'),\
                            index=None)

def calc_mean(descriptor, target, folder):
    random_state = [12,432,5,7543,12343,452,325432435,326,436,2435]
    filepath = path.relpath(f'data/KRR_output/{folder}/results')
    output = pd.DataFrame(np.zeros([6,7]))
    output.columns = ['Train_sizes', 'Train_MAE', 'Train_R2', 'Train_MSE', \
                      'Test_MAE', 'Test_R2', 'Test_MSE']
    for state in random_state:
        input_file = path.join(filepath,\
                                f'result_{descriptor}_{target}_{state}.csv')
        data = pd.read_csv(input_file)
        output = output + data
    output = output / len(random_state)
    output.to_csv(path.join(filepath, f'mean_{descriptor}_{target}.csv'), \
                  index=None)
    return output

calc_mean('MACCS_with_simpol', 'log_p_sat', 'maccs and simple simpol')
random_state = [12,432,5,7543,12343,452,325432435,326,436,2435]
targets = ['log_p_sat', 'kwg', 'kwiomg']
folders = ['maccs and simple simpol', 'maccs and simpol with multiple groups', \
        'maccs and simpol with multiple groups and carbon numbers', \
        'maccs and norings simpol with binary encodings', \
        'maccs and norings simpol with binary encodings and four plus groups', \
        'maccs and simpol final model', 'simpol with encodings']
for folder in folders:
    for target in targets:
        for state in random_state:
            results('MACCS_with_simpol', target, state, folder)
        calc_mean('MACCS_with_simpol', target, folder)

for target in targets:
    for state in random_state:
        results('MACCS', target, state, 'maccs only')
    calc_mean('MACCS', target, 'maccs only')

for target in targets:
    for state in random_state:
        results('simpol', target, state, 'simpol only')
    calc_mean('simpol', target, 'simpol only')
    