#!/bin/bash -l
brick_total=32
Nproc=8
function PushQue {    
Que="$Que $1"
Nrun=$(($Nrun+1))
}
function GenQue {     
OldQue=$Que
Que=""; Nrun=0
for PID in $OldQue; do
if [[ -d /proc/$PID ]]; then
PushQue $PID
fi
done
}
function ChkQue {     
OldQue=$Que
for PID in $OldQue; do
if [[ ! -d /proc/$PID ]] ; then
GenQue; break
fi
done
}

brick_index=0
next_brick=None

function GetNextBrick {
next_brick=${ARRAY[$brick_index]}
brick_index=$brick_index+1
}

#get an array of bricks need to be processed
ARRAY=()
count=0
while IFS='' read -r line || [[ -n "$line" ]]; do
    ARRAY[$count]=$line
    count=$count+1
done < InsideBrick.txt
#done

i=0
for((i=1; i<$brick_total; i++)); do 
        echo 'processing brick: $next_brick'
        ./slurm_job_one_bri_init.sh $next_brick &
	PID=$!
	PushQue $PID
	while [[ $Nrun -ge $Nproc ]]; do
		ChkQue
		sleep 1
	done
done

wait
