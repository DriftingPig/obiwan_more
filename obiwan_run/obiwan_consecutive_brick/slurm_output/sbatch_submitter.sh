#!/bin/bash
for i in `seq 0 2`
do
   brick_id=$i
   sbatch slurm_all_bricks.sh $brick_id
done
