#!/bin/bash -l
source /srv/py3_venv/bin/activate
export PYTHONPATH=$CSCRATCH_OBIWAN/obiwan_code/py:$CSCRATCH_OBIWAN/legacypipe/py:$PYTHONPATH

brick_index=0
next_brick=None

ARRAY=()  
count=0 
while IFS='' read -r line || [[ -n "$line" ]]; do
    ARRAY[$count]=$line 
    count=$count+1 
done < UnprocessedBricks.txt   

function GetNextBrick {
next_brick=${ARRAY[$brick_index]}
brick_index=$brick_index+1
}

function ExcecutBrick {
./slurm_job_one_bri_init.sh $1 $2 $3
}

function ExcecutBrickThread {
sub_DR3_CopyNum=$1
DR3_CopyNum=$2
num1=$(expr ${sub_DR3_CopyNum} - 1 + 0 + $((${DR3_CopyNum} * 128)))
num2=$(expr ${sub_DR3_CopyNum} - 1 + 16 + $((${DR3_CopyNum} * 128)))
num3=$(expr ${sub_DR3_CopyNum} - 1 + 32 + $((${DR3_CopyNum} * 128)))
num4=$(expr ${sub_DR3_CopyNum} - 1 + 48 + $((${DR3_CopyNum} * 128)))
num5=$(expr ${sub_DR3_CopyNum} - 1 + 64 + $((${DR3_CopyNum} * 128)))
num6=$(expr ${sub_DR3_CopyNum} - 1 + 80 + $((${DR3_CopyNum} * 128)))
num7=$(expr ${sub_DR3_CopyNum} - 1 + 96 + $((${DR3_CopyNum} * 128)))
num8=$(expr ${sub_DR3_CopyNum} - 1 + 112 + $((${DR3_CopyNum} * 128)))
ExcecutBrick ${ARRAY[${num1}]} ${sub_DR3_CopyNum} ${DR3_CopyNum}
ExcecutBrick ${ARRAY[${num2}]} ${sub_DR3_CopyNum} ${DR3_CopyNum}
ExcecutBrick ${ARRAY[${num3}]} ${sub_DR3_CopyNum} ${DR3_CopyNum}
ExcecutBrick ${ARRAY[${num4}]} ${sub_DR3_CopyNum} ${DR3_CopyNum}
ExcecutBrick ${ARRAY[${num5}]} ${sub_DR3_CopyNum} ${DR3_CopyNum}
ExcecutBrick ${ARRAY[${num6}]} ${sub_DR3_CopyNum} ${DR3_CopyNum}
ExcecutBrick ${ARRAY[${num7}]} ${sub_DR3_CopyNum} ${DR3_CopyNum}
ExcecutBrick ${ARRAY[${num8}]} ${sub_DR3_CopyNum} ${DR3_CopyNum}
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
