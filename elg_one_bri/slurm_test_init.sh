#!/bin/bash
source /srv/py3_venv/bin/activate  
python --version
echo $PYTHONPATH
export PYTHONPATH=$CSCRATCH_OBIWAN/obiwan_code/py:$CSCRATCH_OBIWAN/legacypipe/py:$PYTHONPATH  
echo $PYTHONPATH
python readingtest.py   
