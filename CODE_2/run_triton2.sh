#!/bin/bash
#SBATCH --time=00-01
#SBATCH --cpus-per-task=16
#SBATCH --mem=1G

cd $WRKDIR
module load miniconda
source activate CODE_2
cd CODE/CODE_2
python run_main.py