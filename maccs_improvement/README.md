
This project contains a modified version of the SIMPOL project (https://github.com/stakahama/aprl-ssp/)
SIMPOL is used to estimate vapor pressures and relies on identifying a number of molecular functional groups/features
https://acp.copernicus.org/articles/8/2773/2008/

The original project was written in python2. I have changed a few instances to be python3 compatible to be able to run, but there might still be parts with py2 syntax.

I added an init file and packaged parts of substructure_search.py as functions.

data
    examples: example scripts from aprl-ssp
    validation: files to test code on 
    output: directory to write analysis output to
scripts
    aprl-ssp - the modified simpol package
    fingerprints - files to interpret MACCS keys and do some analysis on MACCS
notebooks
    contains a notebook for testing the simpol code and extracting statistics on the occurance of groups/features used by simpol.

Example run: 

example: run scripts/aprl_ssp/substructure_search.py -d -g SIMPOLgroups_sane.csv -i data/validation/apinenemech.csv  -o data/output/apinenemech_SIMPOLgroups_1.csv
