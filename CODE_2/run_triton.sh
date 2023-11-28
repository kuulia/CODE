#!/bin/bash
#SBATCH --time=00-05
#SBATCH --mem-per-cpu=4096M
#SBATCH --mem=65536M

cd $WRKDIR
module load miniconda
conda activate CODE_2
python run_main.py