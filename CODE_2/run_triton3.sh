#!/bin/bash
#SBATCH --time=01-00
#SBATCH --mem=100G
#SBATCH --array=0-9

cd $WRKDIR
module load miniconda
source activate CODE_2
cd CODE/CODE_2
random_state = [12,432,5,7543,12343,452,325432435,326,436,2435]
case $SLURM_ARRAY_TASK_ID in
   0)  SEED=12 ;;
   1)  SEED=432  ;;
   2)  SEED=5  ;;
   3)  SEED=7543  ;;
   4)  SEED=12343 ;;
   5)  SEED=452 ;;
   6)  SEED=325432435 ;;
   7)  SEED=326 ;;
   8)  SEED=436 ;;
   9)  SEED=2435 ;;
esac

srun python slurm/run_main_triton.py $SEED