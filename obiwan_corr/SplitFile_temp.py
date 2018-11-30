'''
split the files into multiple piece to run parelle angular correlation function
'''
import numpy as np
import healpy as hp
from astropy.table import Table
from astropy.io import fits
from math import *
def radec2thphi(ra,dec):
        return (-dec+90.)*pi/180.,ra*pi/180.
    
def ranHelpsort(filename,res=256,rad=''):
    origin_dat = fits.open(filename)[1].data
    npix = 12*res**2
    angm = 1.
    if rad == 'rad':
        angm = 180./pi
    pixls=np.zeros(len(origin_dat))
    print len(origin_dat)
    for i in range(0,len(origin_dat)):
        ra,dec = float(origin_dat['ra'][i])*angm,float(origin_dat['dec'][i])*angm
        th,phi = radec2thphi(ra,dec)
        pixls[i]=hp.pixelfunc.ang2pix(res,th,phi,nest=True)
    print 'done'
    orig_cols = origin_dat.columns
    pixls = np.array(pixls)
    new_cols = fits.ColDefs([
            fits.Column(name='pixl',format='I',
                        array=pixls)
                        ])
    tb_hdu = fits.BinTableHDU.from_columns(orig_cols+new_cols)
    tb_dat = Table.read(tb_hdu)
    tb_dat.sort('pixl')
    print str(len(tb_dat))+'#L34'
    return tb_dat

#generate txt files which inculde sin, cos of ra,dec
def SprtFile_nest(filename, total_subs,res=256,rad=''):
    dat = ranHelpsort(filename,res,rad)
    print str(len(dat))+'#L40'
    import os
    base_filename = os.path.basename(filename)
    files = []
    for i in range(0,total_subs):
        sub_filename = base_filename[:-5]+'_subset'+str(i)+'.dat'
        f = open(os.path.join('./output',sub_filename),'w')
        files.append(f)
    
    sub_num = len(dat)/total_subs
    count = 0
    j=0
    pixflag=[]
    for i in range(0,len(dat)):
        ra = dat['ra'][i]
        dec = dat['dec'][i]
        thi = dec*pi/180.
        phi = ra*pi/180.
        files[j].write(str(sin(thi))+' '+str(cos(thi))+' '+str(sin(phi))+' '+str(cos(phi))+'\n')
        if j != total_subs-1:
            count+=1
            if count == sub_num:
                pixflag.append(dat['pixl'][i])
                j+=1
                count=0
    for i in range(0,total_subs):
        files[i].close()
    return pixflag

def SprtFile_nest_dat(filename, total_subs, pixflag, res=256,rad=''):
    dat = ranHelpsort(filename,res,rad)
    import os
    base_filename = os.path.basename(filename)
    files = []
    for i in range(0,total_subs):
        sub_filename = base_filename[:-5]+'_subset'+str(i)+'.dat'
        f = open(os.path.join('./output',sub_filename),'w')
        files.append(f)
    
    sub_num = len(dat)/total_subs
    count = 0
    j=0
    for i in range(0,len(dat)):
        ra = dat['ra'][i]
        dec = dat['dec'][i]
        thi = dec*pi/180.
        phi = ra*pi/180.
        files[j].write(str(sin(thi))+' '+str(cos(thi))+' '+str(sin(phi))+' '+str(cos(phi))+'\n')
        #files[j].write(str(thi)+' '+str(phi)+'\n')
        if j != total_subs-1:
            count+=1
            if dat['pixl'][i] > pixflag[j] :
                j+=1
                print count
                count=0
    for i in range(0,total_subs):
        files[i].close()

Top_dir = '/global/homes/h/huikong/obiwan_test/obiwan_eboss/data/rawdata/'
Top_dir_ran='/global/homes/h/huikong/obiwan_test/obiwan_eboss/data/rawdata/'
datfilename = 'ELGNGCtestfull_V2.dat.fits'
ranfilename = 'ELGNGCtestfull_V2.ran.fits'
pix_flag = SprtFile_nest(Top_dir_ran+ranfilename,20)
SprtFile_nest_dat(Top_dir+datfilename,20,pix_flag)
