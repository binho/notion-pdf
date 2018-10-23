#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from distutils.dir_util import copy_tree

app_deploy_name = 'NotionPDF.app'

print('🚮  Cleaning...')
os.system('rm -f *.pyc')
os.system('rm -fr build')
os.system('rm -fr dist')
os.system('rm -fr __pycache__')
os.system('echo > /tmp/chromedriver.log')

print('⚙️  Running pyinstaller...')
os.system('pyinstaller --onefile --windowed main.spec')

print('🚢  Copying files from bin folder...')
copy_tree('bin/', 'dist/{}/Contents/MacOS/bin'.format(app_deploy_name))