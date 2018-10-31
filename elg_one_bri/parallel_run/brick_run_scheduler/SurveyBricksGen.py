#generating InsideBrick.txt EdgeBrick.txt
import astropy.io.fits as fits
import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table

outdir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_elg/sgc_brick_dat/'
topdir_surveybricks = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_elg/survey_bricks/'
dat = np.loadtxt(outdir+'brick_list.out', dtype = str).transpose()
surveybricks = Table.read(topdir_surveybricks+'survey_bricks_eBoss.fits')
dec_bound = surveybricks['DEC']
sgc_selection = (dec_bound>=-5.)&(dec_bound<=5.)
sgc_surveybricks = surveybricks[sgc_selection]

brick_list = dat[:,dat[0].argsort()]
sgc_surveybricks.sort('BRICKNAME')
num = brick_list[1].astype(float)
assert(len(brick_list[0]) == len(sgc_surveybricks))
f1 = open('InsideBrick.txt', 'w')
f2 = open('EdgeBrick.txt', 'w')
for i in range(len(brick_list[0])):
     if num[i]>800:
          #inside brick
          f1.write(str(brick_list[0][i])+'\n')
     else:
          f2.write(str(brick_list[0][i])+'\n')
f1.close()
f2.close()
