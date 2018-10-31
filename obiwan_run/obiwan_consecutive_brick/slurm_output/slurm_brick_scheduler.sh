#!/bin/bash -l
source /srv/py3_venv/bin/activate
export PYTHONPATH=$CSCRATCH_OBIWAN/obiwan_code/py:$CSCRATCH_OBIWAN/legacypipe_origin/legacypipe/py:$PYTHONPATH

ARRAY=()
count=0
while IFS='' read -r line || [[ -n "$line" ]]; do  
   ARRAY[$count]=$line
   count=`expr $count + 1` 
done < BlobBricks.txt

function ExcecutBrick {
./slurm_job_one_bri_init.sh $1
}

if [ $1 -lt 2915  ]; then
    ExcecutBrick ${ARRAY[$1]}
fi


