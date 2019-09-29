# -*- coding: UTF-8 -*-
'''
Author: Jaime Rivera
File: external_maya_commands.py
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


def maya_lambert(input=None):

    from maya import cmds

    color = input
    alpha = None
    if len(color) == 4:
        alpha = color[3]

    lm = cmds.shadingNode('lambert', asShader=True)
    sg = cmds.sets(renderable=True, empty=True)

    cmds.connectAttr('{}.outColor'.format(lm), '{}.surfaceShader'.format(sg), force=True)
    cmds.setAttr('{}.color'.format(lm), color[0], color[1], color[2])

    if alpha:
        fn = cmds.createNode('floatConstant')
        cmds.setAttr('{}.inFloat'.format(fn), 1-alpha)
        cmds.connectAttr('{}.outFloat'.format(fn), '{}.transparencyR'.format(lm))
        cmds.connectAttr('{}.outFloat'.format(fn), '{}.transparencyG'.format(lm))
        cmds.connectAttr('{}.outFloat'.format(fn), '{}.transparencyB'.format(lm))

    return 'lime', 'lambert shader created'


def maya_aiStandard(input=None):

    from maya import cmds

    color = input
    alpha = None
    if len(color) == 4:
        alpha = color[3]

    ai = cmds.shadingNode('aiStandardSurface', asShader=True)
    sg = cmds.sets(renderable=True, empty=True)

    cmds.connectAttr('{}.outColor'.format(ai), '{}.surfaceShader'.format(sg), force=True)
    cmds.setAttr('{}.baseColor'.format(ai), color[0], color[1], color[2])

    if alpha:
        fn = cmds.createNode('floatConstant')
        cmds.setAttr('{}.inFloat'.format(fn), alpha)
        cmds.connectAttr('{}.outFloat'.format(fn), '{}.opacityR'.format(ai))
        cmds.connectAttr('{}.outFloat'.format(fn), '{}.opacityG'.format(ai))
        cmds.connectAttr('{}.outFloat'.format(fn), '{}.opacityB'.format(ai))

    return 'lime', 'aiStandardSurface shader created'


def maya_constant(input=None):

    from maya import cmds

    color = input
    const = cmds.createNode('colorConstant')
    cmds.setAttr("{}.inColor".format(const), color[0], color[1], color[2])
    if len(color) == 4:
        cmds.setAttr("{}.inAlpha".format(const), color[3])
    return 'lime', 'colorConstant node created'


def maya_IO(input=None):

    from maya import cmds

    def execute_maya(executable):
        from maya import cmds
        import os, math, random
        exec (executable)
    try:
        execute_maya(input)
        return 'lime', 'Command succesfully executed'
    except Exception as e:
        return 'red', 'ERROR: ' + str(e)


def maya_set(input, color):

    from maya import cmds

    if len(cmds.ls(selection=True)) == 0:

        object = str(input.split('.')[0])
        attribute = str(input.split('.')[1])

        try:
            cmds.setAttr("{}.{}".format(object, attribute), color[0], color[1], color[2])
            return 'lime', 'Attribute set correctly'
        except Exception as e:
            print e
            return 'red', 'Could not set attribute'

    elif len(cmds.ls(selection=True)) == 1:

        object = str(cmds.ls(selection=True)[0])
        attribute = input

        if '.' in input:
            return 'red', 'Attr "{}" cannot be set to "{}"'.format(attribute, object)

        try:
            cmds.setAttr("{}.{}".format(object, attribute), color[0], color[1], color[2])
            return 'lime', 'Attribute set correctly'
        except Exception as e:
            print e
            return 'red', 'Could not set attribute'

    elif len(cmds.ls(selection=True)) > 1:

        node_number = len(cmds.ls(selection=True))

        try:
            for node in cmds.ls(selection=True):
                object = str(node)
                attribute = input
                cmds.setAttr("{}.{}".format(object, attribute), color[0], color[1], color[2])
            return 'lime', 'Attribute set correctly to {} selected nodes'.format(node_number)
        except Exception as e:
            print e
            return 'red', 'Could not set attribute to selected nodes'


def maya_get(input):

    from maya import cmds

    if len(cmds.ls(selection=True)) == 0:

        object = str(input.split('.')[0])
        attribute = str(input.split('.')[1])

        try:
            attr = cmds.getAttr("{}.{}".format(object, attribute))
            return 'lime', str(attr)
        except Exception as e:
            print e
            return 'red', 'Could not get attribute'

    elif len(cmds.ls(selection=True)) == 1:

        object = str(cmds.ls(selection=True)[0])
        attribute = input

        if '.' in input:
            return 'red', 'Cannot get attribute "{}" from "{}"'.format(attribute, object)

        try:
            attr = cmds.getAttr("{}.{}".format(object, attribute))
            return 'lime', str(attr)
        except Exception as e:
            print e
            return 'red', 'Could not get attribute'

    elif len(cmds.ls(selection=True)) > 1:
        return 'red', 'Please, select one object or less'
