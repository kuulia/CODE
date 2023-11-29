#!/bin/bash
#SBATCH --time=01-00
#SBATCH --mem=250G

cd $WRKDIR
module load miniconda
source activate CODE_2
cd CODE/CODE_2
python run_main.py