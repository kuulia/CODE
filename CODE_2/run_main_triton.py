#Author: Linus Lind Jan. 2024
#LICENSED UNDER: Creative Commons Attribution-ShareAlike 4.0 International
#Used for calculations on Triton computer cluster on GeckoQ data set
from time import perf_counter_ns
from os import path
from os import getcwd
from model_scripts import *
import numpy as np
from funs import *
import sys


# the main for executing the whole code, Generates the chosen descriptors and
# runs the KRR script. Generates a summary of the results.
def main(seed, desc):
    ###############
    t_0 = perf_counter_ns() # store starting time of the whole script
    #create new output file (if it exists, it is erased)
    filepath = path.relpath('data')
    outputfile = path.join(filepath, 'output_benchmarks.txt')
    output_benchmarks = open(outputfile, 'w+')
    output_benchmarks.close()
    scaling = 1_000_000_000 # used for conversions of powers of 10

    # run precomputations before benchmarking, loading the models etc
    #descs = ['cm', 'mbtr', 'MACCS', 'Morgan', 'TopFP', 'MACCS_with_simpol']
    #targets = ['log_p_sat', 'kwiomg', 'kwg']

    #generate_cm_edited.main(), 
    #generate_mbtr_edited.main()
    #generate_MACCS_edited.main()
    #generate_Morgan_edited.main()
    #generate_TopFP_edited.main()
    #modify_MACCS_with_simpol_1.main()
    #modify_MACCS_with_simpol_2.main()
    #modify_MACCS_with_simpol_3.main()
    #gridsearch_loop.main(1.0)  #not working currently<

    t_end_precomps = perf_counter_ns() # store the end time of precomputations
    runtime_precomps = (t_end_precomps - t_0) // scaling

    ###############
    # run KRR model
    target = 'log_p_sat'

    t_0_lumiaro = perf_counter_ns() # store the start time

    krr_edited_geckoq_triton.main(desc, target, seed)

    ###############
    #compute test error values
    ###############
    t_end_lumiaro = perf_counter_ns() # store the end time of lumiaro code
    runtime_lumiaro = (t_end_lumiaro - t_0_lumiaro) // scaling # compute runtime in seconds

    ###############
    t_0_improved = perf_counter_ns()

    # run improved code
    
    ###############
    #compute test error values
    ###############
    t_end_improved = perf_counter_ns()
    runtime_improved = (t_end_improved - t_0_improved) // scaling
    ###############

    runtime_total = (t_end_improved - t_0) // scaling #calculate the total runtime of the code, in seconds
    runtimes = [runtime_precomps, runtime_lumiaro, runtime_improved, runtime_total]
    
    output_filename = path.join(filepath, 'output_benchmarks.txt')
    write_benchmarks(output_filename, desc, runtimes)
    #print runtime results
    print('\nThe runtime of generating descriptors is: ', runtime_precomps, ' ms \n')
    print('The runtime of the original lumiaro code is: ', runtime_lumiaro, ' s \n')
    print('The runtime of the improved code is: ', runtime_improved, ' s\n')
    print('The total runtime of the script is: ', runtime_total, ' s\n')

if __name__ == "__main__":
    main(int(sys.argv[1]), str(sys.argv[2]))