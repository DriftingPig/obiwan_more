#!/bin/bash 
source /srv/py3_venv/bin/activate 
echo TASK${tasks}
python $obiwan_code/py/obiwan/draw_radec_color_z.py \
 --survey ${survey} --obj elg --ra1 ${ra1} --ra2 ${ra2} --dec1 "-2" --dec2 ${dec2} \
 --ndraws ${nrandoms} --outdir ${outdir} --nproc ${tasks} \
 --startid ${startid} --max_prev_seed ${max_prev_seed}
