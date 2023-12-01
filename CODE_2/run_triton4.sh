#!/bin/bash
#SBATCH --time=01-00
#SBATCH --mem=100G
#SBATCH --array=0-4
#SBATCH --cpus-per-task=5

cd $WRKDIR
module load miniconda
source activate CODE_2
cd CODE/CODE_2
random_state = [432,5,7543,12343,452]
case $SLURM_ARRAY_TASK_ID in
   0)  SEED=432 ;;
   1)  SEED=5  ;;
   2)  SEED=7543  ;;
   3)  SEED=12343  ;;
   4)  SEED=452 ;;
esac

srun python run_main_triton.py $SEED MACCS