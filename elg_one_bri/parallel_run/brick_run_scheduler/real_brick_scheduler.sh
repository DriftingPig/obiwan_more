#!/bin/bash -l
source /srv/py3_venv/bin/activate
export PYTHONPATH=$CSCRATCH_OBIWAN/obiwan_code/py:$CSCRATCH_OBIWAN/legacypipe/py:$PYTHONPATH

ARRAY=()  
count=0 
while IFS='' read -r line || [[ -n "$line" ]]; do
    ARRAY[$count]=$line 
    count=$(expr $count + 1) 
done < UnprocessedBricks.txt   


function ExcecutBrick {
#echo $1 $2 $3
./slurm_job_one_bri_init.sh $1 $2 $3
}

function ExcecutBrickThread {
sub_DR3_CopyNum=$1
DR3_CopyNum=$2
num=()
queue_length=0
for i in `seq 0 $queue_length`
do
   num[$i]=$(expr ${sub_DR3_CopyNum} - 1 + $(($i * 16)) + $((${DR3_CopyNum} * 16)))
done

for i in `seq 0 $queue_length`
do
  if [ ${num[$i]} -lt 1680 ]; then  
      ExcecutBrick ${ARRAY[${num[$i]}]} ${sub_DR3_CopyNum} ${DR3_CopyNum}
  fi
done
}

for i in `seq 1 16`
do
    ExcecutBrickThread $i $1 &
done

wait
