# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 09:27:52 2019

@author: dlozano
"""
import paramiko
import os


def upload(username, pw, local, remote, expNumb):  
    
    hostname = 'lims-hpc-m.latrobe.edu.au'
    port = 6022
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=port, username=username, password=pw)
    
    client.invoke_shell()
    ftpClient = client.open_sftp()
       
    try:
        ftpClient.chdir(remote)  # Test if filePath exists
    except IOError:
        ftpClient.mkdir(remote)  # Create filePath
        ftpClient.chdir(remote)
    
    dest =  remote + '/'+ 'Exp' + expNumb +  '_0001' + '/'
    try:
        ftpClient.chdir(dest)  # Test if filePath exists
    except IOError:
        ftpClient.mkdir(dest)  # Create filePath
        ftpClient.chdir(dest)
    
    folders = os.walk(local)
    cnt = 0
    
    for folder in folders:
        if not folder[2]: 
            continue
        cnt= 0
        for file in folder[2]:
            localPath = folder[0] + '/' + file
            remoteDir = remote + folder[0].split('/')[2] + '/'
            remotePath = remoteDir + file

            try:
                ftpClient.chdir(remoteDir)  # Test if filePath exists
            except IOError:
                ftpClient.mkdir(remoteDir)  # Create filePath
                ftpClient.chdir(remoteDir)
            ftpClient.put(localPath, remotePath)    # At this point, you are in filePath in either case
            os.remove(localPath)
            cnt+=1
            
        print(cnt, 'uploaded from:', folder[0] )
    
    ftpClient.close()
    client.close()
    return cnt

def loginHPC(username, pw):
    hostname = 'lims-hpc-m.latrobe.edu.au'
    port = 6022
    
    cmd='dmidecode > a' 
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname,port,username,pw)
        stdin,stdout,stderr=ssh.exec_command(cmd)
        outlines=stdout.readlines()
        resp=''.join(outlines)
        print(resp)
        ssh.close()
        flag = True
    except paramiko.AuthenticationException as error:
        flag = False
    
    return flag