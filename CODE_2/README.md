# THIS PROJECT IS LICENSED UNDER Creative Commons Attribution-ShareAlike 4.0 International, SEE LICENSE FILE FOR DETAILS
# Last edited 05 JAN 2023
# Author: Linus Lind
# This project is a part of a Bachelor's thesis 'Feature engineering for machine learning predictions in atmospheric science' and is based on the previous work of Lumiaro et al. (2021) https://doi.org/10.5194/acp-21-13227-2021 and parts of the source code are used from the publication. 
# Data for this project is originally sourced from Wang et al. (2017) https://doi.org/10.5194/acp-17-7529-2017
# The aim of this project is to improve the performance and accuracy of the original source code that applies machine learning methods on the data set sourced from Wang et al. (2017)
# Additionally the predictions are cross validated on another data set, GeckoQ (Besel et al., 2023) https://doi.org/10.1038/s41597-023-02366-x 
# This project is guided and supervised by Prof. Patrick Rinke and Dr. Hilda Sandström from Aalto University, Department of Applied Physics, CEST group
# Usage of code: 
# run_main.py to run the given descriptor and target
# run_main.py generates all descriptors and runs the Kernel Ridge Regression (KRR) 
# All data files are stored in 'data' folder
# All model python scripts are stored in 'model_scripts' folder and are accessible as an importable package.
# generate_X.py scripts create molecular descriptors from SMILES strings
# krr_X.py scripts run a Kernel Ridge Regression machine learning model 
# geckoq_modify
# funs.py stores auxiliary functions for run_main.py
# testing.py is for various sanity checks and may be ignored
# results_preprocessing.py and results_processing are for gathering results of runs 
# run_tritonX.sh files are batch scripts for running models on Aalto Triton computer cluster