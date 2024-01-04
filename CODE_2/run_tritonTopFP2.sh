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
   0)  SEED=4321 ;;
   1)  SEED=51  ;;
   2)  SEED=75431  ;;
   3)  SEED=123431  ;;
   4)  SEED=4521 ;;
esac

srun python run_main_triton_topfp.py $SEED TopFP log_p_sat