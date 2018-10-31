#!/bin/bash
export PYTHONPATH=$CSCRATCH_OBIWAN/obiwan_code/py:$CSCRATCH_OBIWAN/legacypipe/py:$PYTHONPATH
export RANDOMS_FROM_FITS=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_elg/sgc_brick_dat/brick_$1.fits
export LEGACY_SURVEY_DIR=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_data/legacysurveydir_${dataset}
export DUST_DIR=/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_data/dust
python $obiwan_code/py/obiwan/kenobi.py --dataset ${dataset} -b $1 \
       --nobj ${nobj} --rowstart ${rowstart} -o ${object} \
       --randoms_db ${randoms_db} \
       --outdir $outdir --add_sim_noise \
       --threads $threads  \
       --do_skipids $do_skipids \
       --do_more $do_more --minid $minid \
       --randoms_from_fits ${RANDOMS_FROM_FITS} \
       --verbose \
       >> $log 2>&1
