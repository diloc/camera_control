# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 16:46:41 2019

@author: dlozano
"""

import numpy as np
import subprocess
import time
import os
import sys
#import pgcam
import glob
from PIL import Image, ExifTags
import sftp
import shutil
import pgcam


formats = ['jpg', 'png', 'nef']


def capture(local, date):
    subprocess.Popen([r"cmd"])
    subprocess.Popen([r'C:/Program Files (x86)/digiCamControl/CameraControlCmd.exe',"captureall"]) 
    
    time.sleep(40)
    #PointGray Acquisition
    # _ = pgcam.poingray(local, date)
    # time.sleep(5)
    
    cwd = os.getcwd()
    os.chdir(local)
    
    for form in formats:
        images = []
        images = glob.glob('*.' + form)

        for cnt_f in range(len(images)):
            oldname = []
            oldname=images[cnt_f]
            cam=oldname.split('_')[0]
            newname = cam + '_' + date
            oldpath = os.path.join(local, oldname)
            campath = os.path.join(local, 'cam' + cam + '_' + form)
            newpath =  campath + '/' +  newname + '.' + form
            
            if not os.path.exists(campath):
                os.mkdir(campath)
        
            if not os.path.exists(newpath):
                os.rename(oldpath, newpath)
                
            if os.path.exists(oldpath):
                os.remove(oldpath)

    os.chdir(cwd)