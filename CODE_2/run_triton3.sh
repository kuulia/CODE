#!/bin/bash
#SBATCH --time=01-00
#SBATCH --mem=100G
#SBATCH --array=0-4
#SBATCH --cpus-per-task=5

cd $WRKDIR
module load miniconda
source activate CODE_2
cd CODE/CODE_2

case $SLURM_ARRAY_TASK_ID in
   0)  SEED=12 ;;
   1)  SEED=325432435  ;;
   2)  SEED=326  ;;
   3)  SEED=436  ;;
   4)  SEED=2435 ;;
esac

srun python run_main_triton.py $SEED MACCS_with_simpol