#!/bin/bash -l

#SBATCH -p debug
#SBATCH -N 2
#SBATCH -t 0:02:00
#SBATCH --account=desi
#SBATCH --image=driftingpig/obiwan_composit:v3
#SBATCH -J obiwan_mpi4py_test
####SBATCH -o ./mpi4py_test_%j.out
#SBATCH -L SCRATCH,project
#SBATCH -C haswell
#SBATCH --mail-user=kong.291@osu.edu  
#SBATCH --mail-type=ALL
###SBATCH --cpus-per-task=2 --ntasks=1
###SBATCH packjob
###SBATCH --cpus-per-task=62 --ntasks=1
###SBATCH packjob
###SBATCH --cpus-per-task=64 --ntasks=2

export OMP_NUM_THREADS=32
srun -n 4 -c 32 shifter python mpi4py_test.py
