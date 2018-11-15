'''
merge all sim randoms per brick to one fits file
'''
import astropy.io.fits as fits
import numpy as np
import os
from glob import glob
topdir_randoms = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_elg/sgc_brick_dat/'
def BrickMerge():
    fns = glob(os.path.join(topdir_randoms,'*.fits'))
    hdu = fits.open(fns[0])
    dat = hdu[1].data
    hdu.close()
    for i in range(1,len(fns)):
        print(os.path.basename(fns[i]))
        hdu = fits.open(fns[i])
        dat_i = hdu[1].data 
        hdu.close()
        dat = np.hstack((dat,dat_i))
    cols = fits.ColDefs(dat) 
    HDU = fits.BinTableHDU.from_columns(cols)
    HDU.writeto('./ipynb/sim_randoms.fits', overwrite=True)

if __name__ == '__main__':
    BrickMerge() 
