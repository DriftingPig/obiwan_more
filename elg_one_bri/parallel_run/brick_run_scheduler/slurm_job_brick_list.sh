#!/bin/bash 
source /srv/py3_venv/bin/activate  
export PYTHONPATH=$CSCRATCH_OBIWAN/obiwan_code/py:$CSCRATCH_OBIWAN/legacypipe/py:$PYTHONPATH
export LEGACY_SURVEY_DIR=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_data/legacysurveydir_${dataset}
brickname1=0001m002
brickname2=0001m005
brickname3=0001m007
brickname4=0001m010
brickname5=0001m012
brickname6=0001m015
brickname7=0001m017
brickname8=0001m020
./slurm_job_one_bri_init.sh $brickname1 &
./slurm_job_one_bri_init.sh $brickname2 &
./slurm_job_one_bri_init.sh $brickname3 &
./slurm_job_one_bri_init.sh $brickname4 &
./slurm_job_one_bri_init.sh $brickname5 &
./slurm_job_one_bri_init.sh $brickname6 &
./slurm_job_one_bri_init.sh $brickname7 &
./slurm_job_one_bri_init.sh $brickname8 &

wait

