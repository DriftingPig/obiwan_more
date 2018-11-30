Top_dir = '/global/cscratch1/sd/huikong/obiwan_code/obiwan_publish/output/'
datfilename = 'elg_N175.fits'
ranfilename = 'elg_rdN_flagged175.fits'
bins = 51
MaxAng = 1.#degree
MinAng = 0.01 #degree
from math import *
import numpy as np
from matplotlib import pyplot as plt
def AngDis(dat1,i,dat2,j):
    ra1 = dat1['ra'][i]*pi/180.
    dec1 = dat1['dec'][i]*pi/180.
    ra2 = dat2['ra'][j]*pi/180.
    dec2 = dat2['dec'][j]*pi/180.
    return cos(dec1)*cos(dec2)*cos(ra1-ra2)+sin(dec1)*sin(dec2)

def binning():
    UpAng = MaxAng*pi/180.
    DownAng = MinAng*pi/180.
    UpAngLog = log10(UpAng)
    DownAngLog = log10(DownAng)
    interval = (UpAngLog-DownAngLog)/(float)(bins-1)
    LogList = np.zeros(bins)
    for i in range(0,bins):
        LogList[i] = DownAngLog+interval*i
    CosList = np.zeros(bins)
    for i in range(0,bins):
        CosList[i] = cos(pow(10,LogList[i]))
    return CosList

def BinAllocator(data,List):
    if data>List[0]:
        return -2
    if data<List[len(List)-1]:
        return -1
    for i in range(1,len(List)):
        if data>List[i]:
            return i-1
    raise ValueError('wrong in BinAllocator')

import astropy.io.fits as fits
def corr():
    elgs = fits.open(Top_dir+datfilename)[1].data
    rans = fits.open(Top_dir+ranfilename)[1].data
    elgs = elgs[:len(elgs)/10.]
    rans = rans[:len(rans)/10.]
    print len(elgs)
    print len(rans)
    CosLists = binning()
    DD_Hist = np.zeros(bins-1)
    DD_tot=0
    DR_Hist = np.zeros(bins-1)
    DR_tot = 0
    RR_Hist = np.zeros(bins-1)
    RR_tot = 0
    #DD
    print 'DD'
    for i in range(0,len(elgs)):
        for j in range(i+1,len(elgs)):
            DD_tot+=1
            agdis = AngDis(elgs,i,elgs,j)
            num = BinAllocator(agdis,CosLists)
            if num>=0:
                DD_Hist[num]+=1
                
    #DR
    print 'DR'
    for i in range(0,len(elgs)):
        for j in range(0,len(rans)):
            DR_tot+=1
            agdis = AngDis(elgs,i,rans,j)
            num = BinAllocator(agdis,CosLists)
            if num>=0:
                DR_Hist[num]+=1    
                
    #RR
    print 'RR'
    for i in range(0,len(rans)):
        for j in range(0,len(rans)):
            RR_tot+=1
            agdis = AngDis(rans,i,rans,j)
            num = BinAllocator(agdis,CosLists)
            if num>=0:
                RR_Hist[num]+=1    
                
    Corr_Hist = np.zeros(bins-1)
    for i in range(0,bins-1):
        Corr_Hist[i] = (DD_Hist[i]/DD_tot-DR_Hist[i]/DR_tot+RR_Hist[i]/RR_tot)/(RR_Hist[i]/RR_tot)
    print 'CorrHistV2'
    f = open('CorrHistV2','w')
    for i in range(0,len(Corr_Hist)):
        f.write(str(Corr_Hist[i])+'\n')
    f.close()
    print 'DD'
    f = open('D0D0','w')
    for i in range(0,len(DD_Hist)):
        f.write(str(DD_Hist[i])+'\n')
    f.close()
    print 'DR'
    f = open('D0R0','w')
    for i in range(0,len(DR_Hist)):
        f.write(str(DR_Hist[i])+'\n')
    f.close()   
    print 'RR'
    f = open('R0R0','w')
    for i in range(0,len(RR_Hist)):
        f.write(str(RR_Hist[i])+'\n')
    f.close()     
    xaxis = np.arange(0,bins)
    plt.plot(xaxis, Corr_Hist)
    
corr()
