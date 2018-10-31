#!/bin/bash -l

#SBATCH -p regular
#SBATCH -N 1
#SBATCH -t 01:30:00
#SBATCH --account=desi
#SBATCH --image=driftingpig/obiwan_composit:v4
#SBATCH -J obiwan
#SBATCH -L SCRATCH,project
#SBATCH -C haswell
#########SBATCH --volume="/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_data:/legacysurvey-0351m042;/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_data:/legacysurvey-0354m042"
#SBATCH --mail-user=kong.291@osu.edu  
#SBATCH --mail-type=ALL

export name_for_run=elg_eight_bricks 
export randoms_db=None
export dataset=dr3 
export rowstart=0 
export do_skipids=no  
export do_more=no 
export minid=1  
export object=elg   
export nobj=200

export usecores=64
export threads=8  
export CSCRATCH_OBIWAN=$CSCRATCH/obiwan_Aug/repos_for_docker  
export PYTHONPATH=$CSCRATCH_OBIWAN/obiwan_code/py:$CSCRATCH_OBIWAN/legacypipe/py:$PYTHONPATH 

export obiwan_data=$CSCRATCH_OBIWAN/obiwan_data
export obiwan_code=$CSCRATCH_OBIWAN/obiwan_code
export obiwan_out=$CSCRATCH_OBIWAN/obiwan_out  

# NERSC / Cray / Cori / Cori KNL things 
export KMP_AFFINITY=disabled  
export MPICH_GNI_FORK_MODE=FULLCOPY 
export MKL_NUM_THREADS=1 
export OMP_NUM_THREADS=1   
# Protect against astropy configs 
export XDG_CONFIG_HOME=/dev/shm   
srun -n $SLURM_JOB_NUM_NODES mkdir -p $XDG_CONFIG_HOME/astropy

srun -N 1 -n 1 -c $usecores shifter ./slurm_job_brick_list.sh

#sleep 5

#export log=${outdir}/logs/${bri}/${brick}/${rsdir}/log.${brick2}
#mkdir -p $(dirname $log)
#echo logging to...${log}

#srun -N 1 -n 1 -c $usecores shifter ./slurm_job_one_bri_init.sh ${brick2}
#wait



