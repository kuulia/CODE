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
   0)  SEED=121 ;;
   1)  SEED=3254324351  ;;
   2)  SEED=3261  ;;
   3)  SEED=4361  ;;
   4)  SEED=24351 ;;
esac

srun python run_main_triton_topfp.py $SEED TopFP log_p_sat