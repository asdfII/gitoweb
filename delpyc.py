# -*- coding: utf-8 -*-

import os
import platform


if platform.system() == 'Windows':
    os.system('del /q /f /s *.pyc')
if platform.system() == 'Linux':
    os.system('rm -fr *.pyc')