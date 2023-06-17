# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 15:05:45 2018

@author: dlozano
"""
import numpy as np
import time
import PySpin
import sys
import os
import glob
import winsound

#
#inputPath = 'F:/pheno'
#
#os.chdir(local)


NUM_IMAGES = 1  # number of images to grab
IDs = np.array([[16078622, 16078632, 16078619, 16078549, 16078623, 16078565, 16078559, 16119278, 16119280, 15641536, 16078562, 16078621, 16078550, 16078630, 16078627, 16078626, 16078612, 16078548
], [1000, 24, 32, 28, 27, 15, 11, 22, 25, 26, 31, 19, 21, 17, 29, 23, 13, 30]])

def acquire_images(cam, nodemap, nodemap_tldevice, date):
    
    try:
        result = True
        node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        
        if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
            print('')
#            print('Unable to set acquisition mode to continuous (enum retrieval). Aborting...')
            return False
        
        #node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        node_acquisition_mode_SingleFrame = node_acquisition_mode.GetEntryByName('SingleFrame')
        
        
        if not PySpin.IsAvailable(node_acquisition_mode_SingleFrame) or not PySpin.IsReadable(node_acquisition_mode_SingleFrame):
            print('')
#            print('Unable to set acquisition mode to continuous (entry retrieval). Aborting...')
            return False

        # Retrieve integer value from entry node
        #acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
        acquisition_mode_SingleFrame = node_acquisition_mode_SingleFrame.GetValue()
        


        # Set integer value from entry node as new value of enumeration node
        node_acquisition_mode.SetIntValue(acquisition_mode_SingleFrame)

        cam.BeginAcquisition()
        device_serial_number = ''
        node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))


        
        if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(node_device_serial_number):
            device_serial_number = node_device_serial_number.GetValue()
#            print('Device serial number retrieved as %s...' % device_serial_number)

        # Retrieve, convert, and save images
        #for i in range(NUM_IMAGES):
        try:
            image_result = cam.GetNextImage()
            if image_result.IsIncomplete():
                print('')
#                print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
            else:
                image_converted = image_result.Convert(PySpin.PixelFormat_RGB8, PySpin.HQ_LINEAR)
                index = np.where(IDs==np.int64(device_serial_number))[1]
                sNumb = np.str(IDs[1,index][0])
                filename = sNumb+'_'+ date +'.jpg'
                image_converted.Save(filename)
                # print('      ' + filename)
                image_result.Release()

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return False
        cam.EndAcquisition()
    
    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        return False

    return result



def run_single_camera(cam, date):

    try:
        result = True
        nodemap_tldevice = cam.GetTLDeviceNodeMap()     # Retrieve TL device nodemap
        cam.Init()                                      # Initialize camera
        nodemap = cam.GetNodeMap()                      # Retrieve GenICam nodemap
        result &= acquire_images(cam, nodemap, nodemap_tldevice, date) # Acquire images
        cam.DeInit()                                    # Deinitialize camera

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        result = False
    return result


def shottime():
    now=time.localtime()
    yy=str(format(now[0], '04d'))
    mon=str(format(now[1], '02d'))
    dd=str(format(now[2], '02d'))
    hh=str(format(now[3], '02d'))
    mm=str(format(now[4], '02d'))
    sec=str(format(now[5], '02d'))     
    tShot=np.str(yy)+'-'+np.str(mon)+'-'+np.str(dd)+'-'+np.str(hh)+'-'+np.str(mm)+'-'+np.str(sec)
    return tShot


def poingray(local, date):
    os.chdir(local)
    result = True
    system = PySpin.System.GetInstance() # Retrieve singleton reference to system object
    cam_list = system.GetCameras()
    num_cameras = cam_list.GetSize()
#    print('PointGray detected: %d' % num_cameras)
#    date = shottime()
    
    if num_cameras == 0: # Finish if there are no cameras
        cam_list.Clear()  # Clear camera list before releasing system
        system.ReleaseInstance()  # Release system instance
        print('Not enough cameras!')
        return False

    for i, cam in enumerate(cam_list):    # Run example on each camera
        print(i,cam)
        result &= run_single_camera(cam, date)
        del cam
   
#    del cam
    cam_list.Clear()  # Clear camera list before releasing system
    system.ReleaseInstance()  # Release system instance
    
        
    return result

