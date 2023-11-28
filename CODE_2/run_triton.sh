#!/bin/bash
#SBATCH --time=00-05
#SBATCH --mem=100G

cd $WRKDIR
module load miniconda
conda activate CODE_2
python run_main.py