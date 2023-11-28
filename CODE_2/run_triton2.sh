#!/bin/bash
#SBATCH --time=00-05
#SBATCH --mem=100G

cd $WRKDIR/CODE/CODE_2
python run_main.py