#import this file
from os import path
import numpy as np

def fun1():
    return 1

def clearvars(): #used for clearing all variables between different runs of main
    for el in sorted(globals()):
        if '__' not in el:
                print(f'deleted: {el}')
                del el

def write_benchmarks(filename, descriptor, runtimes):
    
    lines = [f'Benchmarks for {descriptor}\n',
              '#######################\n',
              f'The runtime of generating {descriptor} was: {runtimes[0]} ms \n',
              f'The runtime of the original lumiaro code for {descriptor} was: {runtimes[1]} s \n',
              f'The runtime of the improved code for {descriptor} was: {runtimes[2]} s \n',
              '#######################\n\n'
              ]
    with open(filename, 'a') as f:
        f.writelines(lines)

def summarizer(descriptor, target):
    random_state = [12,432,5,7543,12343,452,325432435,326,436,2435]
    MAEs = []
    filepath = path.relpath("CODE_2/data/KRR_output")
    fileoutname =  path.join(filepath, f'summary_{descriptor}_{target}.txt')
    outfile = open(fileoutname, 'w+')
    outfile.write(f'Test MAEs for {descriptor} -> {target} were:\n')
    outfile.close() 
    for state in random_state:
        name_of_file = f'output_KRR_{descriptor}_{target}_{state}.txt'
        filename = path.join(filepath, name_of_file)
        file = open(filename, 'r')
        lines = file.readlines()
        MAE = lines[107].removeprefix('Test MAE: ')
        outfile = open(fileoutname, 'a')
        outfile.write(MAE)
        outfile.close()
        MAEs.append(float(MAE))
    mean_val = sum(MAEs) / len(MAEs)
    outfile = open(fileoutname, 'a')
    outfile.write(f'\nmean: {mean_val}')
    outfile.close()
    


        

