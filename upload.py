# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:52:51 2019

@author: Diloz
"""

import sftp

root = 'F:/'
EXP = 'Exp12'
expName = EXP + '_RAO_dns'
local = root + 'pheno/'
remote = '/data/phenomics-archive/whelanlab/' + expName + '/'

sftp.upload(local, remote, EXP)