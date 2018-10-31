'''
assert: all files are either in:
1. before October, files are date-1 in that month
2.after October, files are in date-1 folder

folder at: /global/projecta/projectdirs/cosmo/staging/decam/NonDECaLS/

folder format: CP20161130
file format: c4d_130105_071202_ood_r_a1.fits.fz
'''
import os
import glob
import numpy as np
#def yesterday():
#   '''
#    string conversion: 130105 --> 130104
#   '''

#def assert_test():
topdir = '/global/projecta/projectdirs/cosmo/staging/decam/NonDECaLS/'
folders_path = np.array(glob.glob(topdir + "*"))
folders_path.sort()
date_list = np.array([ os.path.basename(br) for br in folders_path ])
for i in range(len(date_list)):
                '''
        	year = date_list[i][2:5]
                print(str(i)+'th year is: '+str(year))
                month = date_list[i][6:7]
                print('month:'+str(month))
                if len(date_list[i])==10
                    date = date_list[i][8:9]
                    print('date:'+str(date))
                    date=int(date)
                year = int(year)
                month = int(month)
                '''
                #if year<=2012 or (year==2013 and month<=9):
                       #use the month only
                        #if len(date_list[i]) == 8:
                #print(date_list[i][2:])
                fn_data = np.array(glob.glob(folders_path[i]+'/*'))
                data_basename = [os.path.basename(br) for br in fn_data]
                for fitsfiles in data_basename:
                       if fitsfiles[4:10]<date_list[i][4:] and date_list[i]!='CPHETDEX':
                            print(fitsfiles,date_list[i])


#assert_test()
        
