#!/bin/bash -l
source /srv/py3_venv/bin/activate
export PYTHONPATH=$CSCRATCH_OBIWAN/obiwan_code/py:$CSCRATCH_OBIWAN/legacypipe/py:$PYTHONPATH

ARRAY=()  
count=0 
while IFS='' read -r line || [[ -n "$line" ]]; do
    ARRAY[$count]=$line 
    count=$count+1 
done < /global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/more/obiwan_run/brickstat/UnprocessedBricks.txt   


function ExcecutBrick {
#echo $1 $2 $3
./slurm_job_one_bri_init.sh $1 $2 $3
}

function ExcecutBrickThread {
sub_DR3_CopyNum=$1
DR3_CopyNum=$2
num=()
queue_length=25
for i in `seq 0 $queue_length`
do
   num[$i]=$(expr ${sub_DR3_CopyNum} - 1 + $(($i * 16)) + $((${DR3_CopyNum} * 400)))
done

for i in `seq 0 $queue_length`
do
  if [ ${num[$i]} -lt 2915  ]; then  
      ExcecutBrick ${ARRAY[${num[$i]}]} ${sub_DR3_CopyNum} ${DR3_CopyNum}
  fi
done
}

ExcecutBrickThread 1 $1 &
ExcecutBrickThread 2 $1 &
ExcecutBrickThread 3 $1 &
ExcecutBrickThread 4 $1 &
ExcecutBrickThread 5 $1 &
ExcecutBrickThread 6 $1 &
ExcecutBrickThread 7 $1 &
ExcecutBrickThread 8 $1 &
ExcecutBrickThread 9 $1 &
ExcecutBrickThread 10 $1 &
ExcecutBrickThread 11 $1 &
ExcecutBrickThread 12 $1 &
ExcecutBrickThread 13 $1 &
ExcecutBrickThread 14 $1 &
ExcecutBrickThread 15 $1 &
ExcecutBrickThread 16 $1 & 

wait
