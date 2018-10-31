import astropy.io.fits as fits
import numpy as np
import logging
import sys
import multiprocessing
'''
generate a fits file for randoms of a brick (#TODO more bricks within one fits file)
'''
topdir_randoms = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_elg/randoms_test_2/'
topdir_surveybricks = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_elg/survey_bricks/'
outdir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_elg/sgc_brick_dat_2/'

surveybricks = fits.open(topdir_surveybricks+'survey_bricks_eBoss.fits')[1].data

#ra_bound = surveybricks['ra']
dec_bound = surveybricks['DEC']
sgc_selection = (dec_bound>=-5.)&(dec_bound<=5.)

sgc_surveybricks = surveybricks[sgc_selection]

    
def startid(i):
    return 10811721

def GetBrickSrcs(index, write=True):
    from os.path import isfile
    if isfile(outdir+'brick_%s.fits' % (sgc_surveybricks['BRICKNAME'][index])):
        print('file exists for index %d' % index)
        return True
    log = logging.getLogger('grick_stats')
    log.info('sgc_surveybricks[%d] brickname:%s ra1 %f ra2 %f dec1 %f dec2 %f' %(index, sgc_surveybricks['BRICKNAME'][index], sgc_surveybricks['RA1'][index], sgc_surveybricks['RA2'][index], sgc_surveybricks['DEC1'][index], sgc_surveybricks['DEC2'][index]))
    
    ra1 = sgc_surveybricks['RA1'][index]
    ra2 = sgc_surveybricks['RA2'][index]
    dec1 = sgc_surveybricks['DEC1'][index]
    dec2 = sgc_surveybricks['DEC2'][index]
    flag = True
    TOTAL_COUNT=0
    for i in range(48,64):
        hdu = fits.open(topdir_randoms+'randoms_seed_%d_startid_%d.fits' % (i, startid(i)))
        dat_i = hdu[1].data
        hdu.close()
        TOTAL_COUNT+=len(dat_i)
        dat_ra = dat_i['ra']
        dat_dec = dat_i['dec']
        dat_sel = (dat_ra>ra1)&(dat_ra<ra2)&(dat_dec>dec1)&(dat_dec<dec2)
        dat_i_brick = dat_i[dat_sel]
        if flag:
           dat_brick = dat_i_brick
           if len(dat_brick)>0:
               flag=False
               log.debug(len(dat_brick))
        else:
           dat_brick = np.hstack((dat_brick, dat_i_brick))
           log.debug(len(dat_i_brick))
           log.debug(len(dat_brick))
    #log.info('Total points here are: %d total number of bricks: %d' % (TOTAL_COUNT, len(sgc_surveybricks)))
    if write is True:
        cols = fits.ColDefs(np.array(dat_brick))
        HDU = fits.BinTableHDU.from_columns(cols)
        HDU.writeto(outdir+'brick_%s.fits' % (sgc_surveybricks['BRICKNAME'][index]))
    return np.array(dat_brick)

def GetBrickStats():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    log = logging.getLogger('grick_stats')
    log.info('entering GetBrickStats...')
    CPU_COUNT = multiprocessing.cpu_count()
    p = multiprocessing.Pool(CPU_COUNT)
    tasks=range(len(sgc_surveybricks))
    outputs = p.map(GetBrickSrcs, tasks)
    #output_len = [len(outputs[i]) for i in range(len(outputs))]
    #bricknames = sgc_surveybricks['BRICKNAME']
    #bricks_len_list = np.array(zip(bricknames, output_len))
    #FAILED: #np.savetxt(outdir+'brick_list.out',bricks_len_list)
    GetBrickInfoFile()
    log.info('exiting GetBrickStats...')

def GetBrickInfoFile():
    f = open(outdir+'brick_list.out',"w")
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    log = logging.getLogger('grick_stats')
    for brick_i in sgc_surveybricks['BRICKNAME']:
        log.info("writing %s" % brick_i)
        hdu = fits.open(outdir+'brick_%s.fits' % brick_i)
        dat = hdu[1].data
        hdu.close()
        f.write("%s %d\n" % (brick_i, len(dat)))
    f.close()

def run_one_brick():
    print('test run')
    for i in range(1):
        final_array = GetBrickSrcs(i)
        print('brick:%s length:%d' % (sgc_surveybricks['BRICKNAME'][i], len(final_array)))
    #    brickname_array = np.array([sgc_surveybricks['BRICKNAME'][i] for k in range(len(final_array))])
    #    brickname_cols = fits.Column(name='brickname',array=brickname_array,format='20A')
        cols = fits.ColDefs(final_array)
        print(type(cols))
    #    cols.add_col(brickname_cols)
        HDU = fits.BinTableHDU.from_columns(cols)
        HDU.writeto(outdir+'brick_%s.fits' % (sgc_surveybricks['BRICKNAME'][i]), overwrite=True)

if __name__ == '__main__':
    GetBrickStats()
