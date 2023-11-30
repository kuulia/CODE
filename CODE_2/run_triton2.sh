#!/bin/bash
#SBATCH --time=01-00
#SBATCH --cpus-per-task=8
#SBATCH --mem=100G

cd $WRKDIR
module load miniconda
source activate CODE_2
cd CODE/CODE_2
python run_main_triton.py 452 'MACCS_with_simpol'