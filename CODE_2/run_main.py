import subprocess as sp
import time
import os, sys
from model_scripts import *
import numpy as np
from funs import * # see module funs.py

# the main for executing the whole code
def main():
    ###############
    t_0 = time.time_ns() # store starting time of the whole script
    scaling = 1_000_000 # used for conversions of powers of 10
    # run precomputations before benchmarking
    # loading the models etc
    generate_cm_edited.main()
    generate_mbtr_edited.main()
    #generate_MACCS_edited.main()
    #generate_Morgan_edited.main()
    #generate_topological_edited.main()

    ###############
    t_0_lumiaro = time.time_ns() # store the starting time of executing main

    # run lumiaro code
    n=100_000
    arr = np.zeros((n,1))
    for i in range(0,n):
        arr[i] = i * (i+1)
    
    t_end_lumiaro = time.time_ns() # store the end time of lumiaro code
    runtime_lumiaro = (t_end_lumiaro - t_0_lumiaro) // scaling # compute runtime (in milliseconds)

    ###############
    t_0_improved = time.time_ns()

    #run improved codetime.time_ns()
    n=10_000
    arr2 = np.zeros((n,1))
    for i in range(0,n):
        arr[i] = i * (i+1)

    t_end_improved = time.time_ns()
    runtime_improved = (t_end_improved - t_0_improved) // scaling
    ###############

    runtime_total = (t_end_improved - t_0) // scaling #calculate the total runtime of the code


    #print runtime results
    print('\nThe runtime of the original lumiaro code is: ', runtime_lumiaro, ' ms \n')
    print('The runtime of the improved code is: ', runtime_improved, ' ms\n')
    print('The total runtime of the script is: ', runtime_total, ' ms\n')

if __name__ == "__main__":
    clearvars()
    main()