#!/bin/bash
source /srv/py3_venv/bin/activate
python --version
export PYTHONPATH=$CSCRATCH_OBIWAN/obiwan_code/py:$CSCRATCH_OBIWAN/legacypipe/py:$PYTHONPATH
echo $PYTHONPATH
export RANDOMS_FROM_FITS=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_elg/sgc_brick_dat/brick_${brick}.fits
export LEGACY_SURVEY_DIR=/legacysurvey-${brick}/legacysurveydir_${dataset}
ls -l $LEGACY_SURVEY_DIR
python $obiwan_code/py/obiwan/kenobi.py --dataset ${dataset} -b ${brick} \
       --nobj ${nobj} --rowstart ${rowstart} -o ${object} \
       --randoms_db ${randoms_db} \
       --outdir $outdir --add_sim_noise \
       --threads $threads  \
       --do_skipids $do_skipids \
       --do_more $do_more --minid $minid \
       --randoms_from_fits ${RANDOMS_FROM_FITS} \
       --verbose \
       >> $log 2>&1
