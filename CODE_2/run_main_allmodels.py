from time import perf_counter_ns
from os import path
from model_scripts import *
import numpy as np
from funs import *

# the main for executing the whole code
def main():
    ###############
    t_0 = perf_counter_ns() # store starting time of the whole script
    #create new output file (if it exists, it is erased)
    output_benchmarks = open(f'CODE_2/data/output_benchmarks.txt', 'w+')
    output_benchmarks.close()
    filepath = path.relpath("CODE_2/data")
    output_filename = path.join(filepath, 'output_benchmarks.txt')
    scaling = 1_000_000 # used for conversions of powers of 10

    # run precomputations before benchmarking, loading the models etc
    descs = ['cm', 'mbtr', 'MACCS', 'Morgan', 'TopFP']
    gens = [generate_cm_edited.main, 
            generate_mbtr_edited.main,
            generate_MACCS_edited.main,
            generate_Morgan_edited.main,
            generate_TopFP_edited.main]
    #gridsearch_loop.main(1.0)  #not working currently
    for i, desc in enumerate(descs):
        t_0_desc = perf_counter_ns() # store starting time of descriptor generator
        gens[i]()
        t_end_desc = perf_counter_ns() # store the end time of descriptor generator
        runtime_desc = (t_end_desc - t_0_desc) // scaling

        ###############
        # run lumiaro code
        t_0_lumiaro = perf_counter_ns() # store the starting time of executing main
        #krr_edited.main(desc, 'log_p_sat')

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

        runtimes = [runtime_desc, runtime_lumiaro, runtime_improved]
        write_benchmarks(output_filename, desc, runtimes)
        #print runtime results
        #print('\nThe runtime of generating descriptors is: ', runtime_desc, ' s \n')
        #print('The runtime of the original lumiaro code is: ', runtime_lumiaro, ' s \n')
        #print('The runtime of the improved code is: ', runtime_improved, ' s\n')
    
    runtime_total = (perf_counter_ns() - t_0) // scaling #calculate the total runtime of the code, in seconds
    print('The total runtime of the script is: ', runtime_total, ' ms\n')

if __name__ == "__main__":
    clearvars()
    main()