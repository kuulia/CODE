#!/bin/bash
#SBATCH --time=00-01
#SBATCH --cpus-per-task=8
#SBATCH --mem=250G

cd $WRKDIR
module load miniconda
source activate CODE_2
cd CODE/CODE_2
python run_main.py