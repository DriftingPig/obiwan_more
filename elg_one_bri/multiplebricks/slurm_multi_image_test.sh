#SBATCH -p debug
#SBATCH -N 2
#SBATCH -t 00:05:00
#SBATCH --account=cosmo
#SBATCH --image=driftingpig/obiwan_composit:v3
#SBATCH -J obiwan
#SBATCH -L SCRATCH,project
#SBATCH -C haswell
#SBATCH --volume=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_data:/legacysurvey-0068m045
#SBATCH --mail-user=kong.291@osu.edu  
#SBATCH --mail-type=ALL

srun -N 1 -n 2 -c 4 shifter slurm_multi_image_test1.sh --image=driftingpig/obiwan_composit:v3 --volume=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_data:/legacysurvey-01 &

srun -N 1 -n 2 -c 4 shifter slurm_multi_image_test2.sh --image=driftingpig/obiwan_composit:v3 --volume=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_data:/legacysurvey-02 &




