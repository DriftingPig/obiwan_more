from __future__ import print_function
import os 
import glob
import numpy as n
import numpy as np
from astropy.io import fits
from math import *
from astropy.table import Column
example_file = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/elg_eight_bricks/tractor/000/0001m005/more_rs0/tractor-0001m005.fits'

top_dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/elg_new_ccd_list/tractor/'
output_dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/subset/'
brick_pathes = n.array(glob.glob(top_dir + "???/*"))

brick_pathes.sort()

#contains unsuccessful bricks
brick_list = n.array([ os.path.basename(br) for br in brick_pathes ])

simdat_dir = '/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_out/eboss_elg/sgc_brick_dat/'

#all bricks should be succrssful, but might not contain elgs after selection
fn_PB='/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/more/obiwan_run/brickstat/ProcessedBricks.txt'
fn_FB='/global/cscratch1/sd/huikong/obiwan_Aug/repos_for_docker/obiwan_code/py/obiwan/more/obiwan_run/brickstat/elg_new_ccd_list/FinishedBricks.txt'
brick_list_real = n.loadtxt(fn_PB,dtype=n.str).transpose()
brick_list_finished = n.loadtxt(fn_FB,dtype=n.str).transpose()
#select ELGs in one brick
def select_all(index, top_dir = top_dir, brick_pathes = brick_pathes, brick_list = brick_list, startid = 0, nobj = 1000, footprint = 'sgc'):
    brick_name = brick_list[index]
    if not brick_name in brick_list_real:
        return None
    if not brick_name in brick_list_finished:
         return None
    #sim catalogue -- need to be modifiled in the future, multiple rs
    fn_simcat = simdat_dir + 'brick_' + brick_name + '.fits'
    assert(os.path.isfile(fn_simcat))
    #tractor catalogue -- need to be modifiled in the future, multiple rs
    fn_tractorcat = brick_pathes[index]+'/more_rs0/tractor-'+brick_name+'.fits'
    assert(os.path.isfile(fn_tractorcat))
    #DR_5 data
    top_dir_dr5 = "/global/project/projectdirs/cosmo/data/legacysurvey/dr5/tractor"
    fn_DR5 = os.path.join( top_dir_dr5, brick_name[:3], "tractor-"+brick_name+".fits")
    assert(os.path.isfile(fn_DR5))
    #select ELG for obiwan-randoms
    flag_tc, tcN_i, tcS_i = select_ELG(fn_tractorcat, startid = startid, nobj = nobj)
    #select ELG for DR5 data
    flag_DR5, DR5N_i, DR5S_i = select_ELG(fn_DR5)
    #open sim data
    hdu_simcat = fits.open(fn_simcat)
    dat_simcat = hdu_simcat[1].data[startid:startid+nobj]
    hdu_simcat.close()
    if footprint == 'sgc':
        if len(tcS_i)>0 or len(DR5S_i)>0:
            return True, dat_simcat, tcS_i, DR5S_i
        else:
            print('No ELG in brick %s' %(brick_name))
            return None
    if footprint == 'ngc':
        if len(tcN_i)>0 or len(DR5N_i)>0:
             return True, dat_simcat, tcN_i, DR5N_i
        else:
            print('No ELG in brick %s' %(brick_name))
            return None
    else:
        raise ValueError('Invalid region encountered')

def array_to_table(index):
    from astropy.table import Table
    N_bricks = 0
    X = select_all(index)
    if X is None:
        return None
    (flag, simcat, tccat, DR5cat) = X
    print('index: %d, simcat: %d, tccat: %d, DR5cat: %d' \
          %(index, len(simcat), len(tccat), len(DR5cat)))
    
    simcat=n.array(simcat)
    coldefs_simcat = fits.ColDefs(simcat)
    hdu_simcat = fits.BinTableHDU.from_columns(coldefs_simcat)
    tb_simcat = Table.read(hdu_simcat)
    
    tccat=n.array(tccat)
    coldefs_tccat = fits.ColDefs(tccat)
    hdu_tccat = fits.BinTableHDU.from_columns(coldefs_tccat)
    tb_tccat = Table.read(hdu_tccat)

    DR5cat=n.array(DR5cat)
    coldefs_DR5cat = fits.ColDefs(DR5cat)
    hdu_DR5cat = fits.BinTableHDU.from_columns(coldefs_DR5cat)
    tb_DR5cat = Table.read(hdu_DR5cat)
    return True, tb_simcat, tb_tccat, tb_DR5cat 

def obiwan_random_match(index):
    X=array_to_table(index)
    if X is None:
        return None
    (flag, tb_simcat, tb_tccat, tb_DR5cat) = X
    simcat_match_angD = []
    simcat_match_index = []
    for i in range(len(tb_tccat)):
        ra = tb_tccat['ra'][i]
        dec = tb_tccat['dec'][i]
        match_simcat = AngD_Estimation(ra,dec,tb_simcat)
        if len(match_simcat)>0:
            min_angdis = 10.
            min_angdis_index = None
            for j in range(len(match_simcat)):
                angdis_exact = AngD(tb_tccat,i,match_simcat,j)
                if angdis_exact<min_angdis:
                    min_angdis = angdis_exact
                    min_angdis_index = match_simcat['id'][j]
            if min_angdis_index is None:
                simcat_match_angD.append(-1.)
                simcat_match_index.append(-1)
            else:
                simcat_match_angD.append(min_angdis)
                simcat_match_index.append(min_angdis_index)
        else:
            simcat_match_angD.append(-1.)
            simcat_match_index.append(-1)
    assert(len(simcat_match_angD) == len(tb_tccat))        
    DR5cat_match_angD = []
    DR5cat_match_index = []
    for i in range(len(tb_tccat)):
        ra = tb_tccat['ra'][i]
        dec = tb_tccat['dec'][i]
        match_DR5cat = AngD_Estimation(ra,dec,tb_DR5cat)
        if len(match_DR5cat)>0:
            min_angdis = 10.
            min_angdis_index = None
            for j in range(len(match_DR5cat)):
                angdis_exact = AngD(tb_tccat,i,match_DR5cat,j)
                if angdis_exact<min_angdis:
                    min_angdis = angdis_exact
                    min_angdis_index = match_DR5cat['objid'][j]
            if min_angdis_index is None:
                DR5cat_match_angD.append(-1.)
                DR5cat_match_index.append(-1)
            else:
                DR5cat_match_angD.append(min_angdis)
                DR5cat_match_index.append(min_angdis_index)
        else:
            DR5cat_match_angD.append(-1.)
            DR5cat_match_index.append(-1)
    assert(len(DR5cat_match_angD) == len(tb_tccat))
    col_sim_angdis = Column(n.array(simcat_match_angD), name='sim_ang_dis', dtype = 'float64')
    tb_tccat.add_column(col_sim_angdis, index=0)
    col_sim_angindex = Column(n.array(simcat_match_index), name='sim_ang_index', dtype = 'int64')
    tb_tccat.add_column(col_sim_angindex, index=0)
    
    col_DR5_angdis = Column(n.array(DR5cat_match_angD), name='dr5_ang_dis',  dtype = 'float64')
    tb_tccat.add_column(col_DR5_angdis, index=0)
    col_DR5_angindex = Column(n.array(DR5cat_match_index), name='dr5_ang_index', dtype = 'int64')
    tb_tccat.add_column(col_DR5_angindex, index=0)
    return tb_tccat, tb_simcat, tb_DR5cat
    
def AngD_Estimation(ra,dec,tb_data):#SGC only
    #|ra1-ra2|<9.8e-4, |dec1-dec2|<2.8e-4
    ra_lowlim = ra - 9.8e-4
    ra_uplim = ra + 9.8e-4
    dec_lowlim = dec - 2.8e-4
    dec_uplim = dec + 2.8e-4
    value_ra = tb_data['ra']
    value_dec = tb_data['dec']
    selection_box = (value_ra > ra_lowlim) & (value_ra < ra_uplim) & (value_dec > dec_lowlim) & (value_dec < dec_uplim)
    return n.array(tb_data[selection_box])
    
def AngD(tb1,i,tb2,j):
    phi1 = tb1['ra'][i]*pi/180.0
    phi2 = tb2['ra'][j]*pi/180.0
    thi1 = tb1['dec'][i]*pi/180.0
    thi2 = tb2['dec'][j]*pi/180.0
    if cos(thi1)*cos(thi2)*cos(phi1-phi2)+sin(thi1)*sin(thi2)>=1.:
        return 0.
    return (acos(cos(thi1)*cos(thi2)*cos(phi1-phi2)+sin(thi1)*sin(thi2)))*180./pi


def select_ELG( path_2_tractor_file , startid = None, nobj = None):
    """
    Given the path to a tractor catalog, it returns two sub catalogs with the eBOSS ELG selections applied (NGC and SGC).
    """
    # opens the tractor file
    if startid is not None:
        assert(nobj is not None)
        hdu=fits.open(path_2_tractor_file)
        dat=hdu[1].data[startid:startid+nobj]
        hdu.close()
    else:
	    hdu=fits.open(path_2_tractor_file) 
	    dat=hdu[1].data
	    hdu.close()
    # the color color selection
    g     = 22.5 - 2.5 * n.log10(dat['flux_g'] / dat['mw_transmission_g'])
    r_mag = 22.5 - 2.5 * n.log10(dat['flux_r'] / dat['mw_transmission_r'])
    z_mag = 22.5 - 2.5 * n.log10(dat['flux_z'] / dat['mw_transmission_z'])
    gr = g - r_mag
    rz = r_mag - z_mag
    color_sgc = (g>21.825)&(g<22.825)&(-0.068*rz+0.457<gr)&(gr< 0.112*rz+0.773) &(0.218*gr+0.571<rz)&(rz<-0.555*gr+1.901)
    color_ngc = (g>21.825)&(g<22.9)  &(-0.068*rz+0.457<gr)&(gr< 0.112*rz+0.773) &(0.637*gr+0.399<rz)&(rz<-0.555*gr+1.901) 
    # the junk rejection criterion
    noJunk = (dat['brick_primary']) & (dat['anymask_g']==0) & (dat['anymask_r']==0) & (dat['anymask_z']==0) #& (dat['TYCHO2INBLOB']==False)
    # the low depth region rejection
    value_g=dat['psfdepth_g']
    value_r=dat['psfdepth_r']
    value_z=dat['psfdepth_z']
    gL = 62.79716079 
    rL = 30.05661087
    zL_ngc = 11.0
    zL_sgc = 12.75  
    depth_selection_ngc = (value_g > gL) & (value_r > rL) & (value_z > zL_ngc)
    depth_selection_sgc = (value_g > gL) & (value_r > rL) & (value_z > zL_sgc)
    # final selection boolean array :
    selection_sgc =(noJunk)&(color_sgc)&(depth_selection_sgc)
    selection_ngc =(noJunk)&(color_ngc)&(depth_selection_ngc)
    # returns the catalogs of ELGs
    if len(selection_sgc.nonzero()[0])>0 or  len(selection_ngc.nonzero()[0])>0 :
        flag = True
        return flag, dat[selection_ngc], dat[selection_sgc]
    else :
        flag = False
        return flag, dat[selection_ngc], dat[selection_sgc]

def sub_stack_loop(sub_task_list):
    N_bricks=0
    count = 0
    sim_total_match = 0
    DR5_total_match = 0
    total_rands = 0
    f1 = open('NOELGBricks.txt', 'a')
    while count<len(sub_task_list):
          print('#'+str(count))
          X = obiwan_random_match(sub_task_list[count])
          count += 1
          if X is not None:
              (new_col_tccat, new_col_simcat, new_col_dr5cat) = X
              N_bricks+=1
              sim_sel = new_col_tccat['sim_ang_dis']>=-0.5
              DR5_sel = new_col_tccat['dr5_ang_dis']>=-0.5
              sim_total_match += len(new_col_tccat[sim_sel])
              DR5_total_match += len(new_col_tccat[DR5_sel])
              total_rands += len(new_col_tccat)
              assert(len(new_col_simcat) > 0)
              assert(len(new_col_dr5cat) > 0)
              print('sim_total_match: %d DR5_total_match: %d total_rands: %d' %(sim_total_match, DR5_total_match, total_rands))
              break
          else:
              f1.write(str(brick_list[count])+'\n') 
    print('count is: ' + str(count))
    if count>=len(sub_task_list):
          if X is None:
              return None
          else:
              return [np.array(new_col_tccat),len(new_col_tccat),np.array(new_col_simcat), np.array(new_col_dr5cat)]
    #import pdb
    #pdb.set_trace()
    new_col_tccat = np.array(new_col_tccat)
    for ii in range(sub_task_list[count],sub_task_list[-1]+1):
        print('#'+str(ii))
        X = obiwan_random_match(ii)
        if X is not None:
             (new_col_tccat_i, new_col_simcat_i, new_col_dr5cat_i) = X
             N_bricks+=1
             #new_col_tccat += fits.ColDefs(np.array(new_tb_tccat_i))
             new_col_tccat = n.hstack((new_col_tccat, new_col_tccat_i))
             new_col_simcat = n.hstack((new_col_simcat, new_col_simcat_i))
             if len(new_col_dr5cat_i)>0:
                  new_col_dr5cat = n.hstack((new_col_dr5cat, new_col_dr5cat_i))
             sim_sel = new_col_tccat_i['sim_ang_dis']>=-0.5
             DR5_sel = new_col_tccat_i['dr5_ang_dis']>=-0.5
             sim_total_match += len(new_col_tccat_i[sim_sel])
             DR5_total_match += len(new_col_tccat_i[DR5_sel])
             total_rands += len(new_col_tccat_i)
             print('sim_total_match: %d DR5_total_match: %d total_rands: %d' %(sim_total_match, DR5_total_match, total_rands))
        else:
            f1.write(str(brick_list[ii])+'\n')
    #import pdb
    #pdb.set_trace()
    f1.close()
    #pdb.set_trace() 
    print('total valid bricks:'+str(N_bricks))
    print('returning...')
    return [new_col_tccat, total_rands, np.array(new_col_simcat), np.array(new_col_dr5cat)]

def brick_stacks():
    from multiprocessing import Pool
    ntasks = 20
    p = Pool(ntasks)
    task_list = np.arange(0, len(brick_list))
    sub_task_list = np.array_split(task_list, ntasks)
    
    X = p.map(sub_stack_loop, sub_task_list)
    #X = sub_stack_loop(sub_task_list[0])
    #X=[X]
    count = 0
    print('INFO:: after mapping')
    f1 = open('NOELGBricks.txt', 'w') 
    f1.close()
    while count<len(X):
         if X[count] is not None:
             break
         count+=1
    #import pdb
    #pdb.set_trace()
    new_col_tccat, total_rands, new_col_simcat, new_col_dr5cat = X[count]
    assert(len(new_col_simcat)>0)
    assert(len(new_col_dr5cat)>0)
    for i in range(count+1,len(X)):
        if X[i] is not None:
            (new_col_tccat_i, total_rands_i, new_col_simcat_i, new_col_dr5cat_i) = X[i]
            new_col_tccat = np.hstack((new_col_tccat, new_col_tccat_i))
            new_col_simcat = np.hstack((new_col_simcat, new_col_simcat_i))
            new_col_dr5cat = np.hstack((new_col_dr5cat, new_col_dr5cat_i))
       
    hdu_tccat_all = fits.BinTableHDU.from_columns(new_col_tccat)
    hdu_tccat_all.writeto(output_dir + 'random_subset_sub.fits',overwrite = True)
    hdu_simcat_all = fits.BinTableHDU.from_columns(new_col_simcat)
    hdu_simcat_all.writeto(output_dir + 'sim_subset_sub.fits',overwrite = True)
    hdu_dr5cat_all = fits.BinTableHDU.from_columns(new_col_dr5cat)
    hdu_dr5cat_all.writeto(output_dir + 'dr5cat_subset_sub.fits',overwrite = True)
    tot=0
    for subs in X:
        if subs is not None:
            tot+=subs[1]
    print('tot:'+str(tot)+' length of data:'+str(len(new_col_tccat)))     
    
if __name__ == '__main__':
    brick_stacks()
