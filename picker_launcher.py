# -*- coding: UTF-8 -*-
'''
Author: Jaime Rivera
File: picker_launcher.py
Date: 2018.12.29
Revision: 2018.12.29
Copyright: Copyright Jaime Rivera 2018 | www.jaimervq.com
           The program(s) herein may be used, modified and/or distributed in accordance with the terms and conditions
           stipulated in the Creative Commons license under which the program(s) have been registered. (CC BY-SA 4.0)

Brief:

'''

__author__ = 'Jaime Rivera <jaime.rvq@gmail.com>'
__copyright__ = 'Copyright 2018, Jaime Rivera'
__credits__ = []
__license__ = 'Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)'
__maintainer__ = 'Jaime Rivera'
__email__ = 'jaime.rvq@gmail.com'
__status__ = 'Testing'


def get_picker():

    import sys
    import picker_ui
    reload(picker_ui)

    software = 'generic'
    if 'maya' in sys.executable.lower():
        software = 'maya'
    elif 'nuke' in sys.executable.lower():
        software = 'nuke'

    picker = picker_ui.UniversalPicker(software)

    return picker