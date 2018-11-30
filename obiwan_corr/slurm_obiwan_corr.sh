#!/bin/bash -l

#SBATCH -p regular
#SBATCH -N 1
#SBATCH -t 06:00:00
#SBATCH --account=desi
#SBATCH -J obiwan
#SBATCH -L SCRATCH,project
#SBATCH -C haswell
#SBATCH --mail-user=kong.291@osu.edu  
#SBATCH --mail-type=ALL

module load python/2.7-anaconda-5.2
source activate myenv
./ObiwanCorr.sh
