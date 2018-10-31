#!/bin/bash 
source /srv/py3_venv/bin/activate  
export PYTHONPATH=$CSCRATCH_OBIWAN/obiwan_code/py:$CSCRATCH_OBIWAN/legacypipe/py:$PYTHONPATH
#export LEGACY_SURVEY_DIR=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_data/legacysurveydir_${dataset}
brickname1=0001m007
brickname2=0001m010
brickname3=0001m037
brickname4=0001m042
brickname5=0001m045
brickname6=0001p002
brickname7=0001p005
brickname8=0001p007
./slurm_job_one_bri_init.sh $brickname1 1 &
./slurm_job_one_bri_init.sh $brickname2 2 &
./slurm_job_one_bri_init.sh $brickname3 3 &
./slurm_job_one_bri_init.sh $brickname4 4 &
./slurm_job_one_bri_init.sh $brickname5 5 &
./slurm_job_one_bri_init.sh $brickname6 6 &
./slurm_job_one_bri_init.sh $brickname7 7 &
./slurm_job_one_bri_init.sh $brickname8 8 &

wait

