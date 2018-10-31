#a noram file
try:
   f = open('/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_data/legacysurveydir_dr3/calib/decam/psfex/00247/00247916/test.txt')
except Exception as e:
   print(e)

import fitsio
try:
    f=fitsio.FITS('/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_data/legacysurveydir_dr3/calib/decam/psfex/00247/00247916/decam-00247916-S24.fits')
    f.close()
except Exception as e:
   print(e)

from astrometry.util import fits
try:
    T = fits.fits_table('/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_data/legacysurveydir_dr3/calib/decam/psfex/00247/00247916/decam-00247916-S24.fits')
except Exception as e:
    print(e)



