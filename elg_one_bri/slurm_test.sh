#!/bin/bash -l
#SBATCH -p debug
#SBATCH -N 1
#SBATCH -t 00:20:00
#SBATCH --account=cosmo
#SBATCH --image=driftingpig/obiwan_composit:v3
#SBATCH -J obiwan
#SBATCH -L SCRATCH,project
#SBATCH -C haswell
#SBATCH --mail-user=kong.291@osu.edu
#SBATCH --mail-type=ALL
export CSCRATCH_OBIWAN=$CSCRATCH/obiwan_Aug/repos_for_docker


srun -n 1 -c 1 shifter ./slurm_test_init.sh
