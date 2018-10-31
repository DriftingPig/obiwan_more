#!/bin/bash -l
source /srv/py3_venv/bin/activate
export PYTHONPATH=$CSCRATCH_OBIWAN/obiwan_code/py:$CSCRATCH_OBIWAN/legacypipe_origin/legacypipe/py:$PYTHONPATH
export BIRCKSTAT_DIR=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/more/obiwan_run/brickstat
ARRAY=()
count=0
while IFS='' read -r line || [[ -n "$line" ]]; do  
   ARRAY[$count]=$line
   count=`expr $count + 1` 
done < $BIRCKSTAT_DIR/BlobBricks.txt

function ExcecutBrick {
./slurm_job_one_bri_init.sh $1
}

if [ $1 -lt 2915  ]; then
    ExcecutBrick ${ARRAY[$1]}
fi


