# -*- coding: UTF-8 -*-
'''
Author: Jaime Rivera
File: picker_ui.py
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


from PySide2 import QtWidgets, QtCore, QtGui, QtUiTools
import colorsys
import json
import os


class UniversalPicker(QtWidgets.QWidget):

    def __init__(self, software):

        self.SOFTWARE = software

        QtWidgets.QWidget.__init__(self)
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path).replace('\\', '/')
        file = QtCore.QFile(dir_path+'/universal_picker.ui')
        file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load(file,self)

        self.icons_dir_path = dir_path + '/icons/'

        # MAIN CONFIG OF THE WINDOW
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setWindowTitle('Universal color picker')
        self.setFixedWidth(442)
        self.setFixedHeight(854)

        self.setWindowIcon(QtGui.QIcon(self.icons_dir_path + 'picker.png'))

        # RGBA WIDGETS
        self.rgba_sliders = [self.ui.rgb_slider_red, self.ui.rgb_slider_green, self.ui.rgb_slider_blue, self.ui.rgb_slider_alpha]
        self.rgba_doubles = [self.ui.rgb_double_red, self.ui.rgb_double_green, self.ui.rgb_double_blue, self.ui.rgb_double_alpha]
        self.rgba_ints = [self.ui.rgb_int_red, self.ui.rgb_int_green, self.ui.rgb_int_blue]

        # HSV WIDGETS
        self.hsv_sliders = [self.ui.hsv_slider_hue, self.ui.hsv_slider_sat, self.ui.hsv_slider_val]
        self.hsv_doubles = [self.ui.hsv_double_hue, self.ui.hsv_double_sat, self.ui.hsv_double_val]

        # CONNECTIONS, VALIDATORS AND RUNNING
        self.establish_software()
        self.make_connections()
        self.set_validators()
        self.load_pantones()
        self.run()


    def establish_software(self):
        
        # ICONS FOR THE SPECIFIC BUTTONS
        icon_create = QtGui.QIcon(self.icons_dir_path + 'create.png')
        icon_paint = QtGui.QIcon(self.icons_dir_path + 'paint.png')

        if self.SOFTWARE == 'maya':
            self.ui.specifics_label.setText('MAYA')

            self.ui.specifics_button_0.setIcon(icon_create)
            self.ui.specifics_button_0.setText('Lambert')
            self.ui.specifics_button_0.setToolTip('Create a Lambert shader with the current selected color')
            self.ui.specifics_button_0.clicked.connect(self.to_external_maya_commands_0)

            self.ui.specifics_button_1.setIcon(icon_create)
            self.ui.specifics_button_1.setText('aiStandard')
            self.ui.specifics_button_1.setToolTip('Create an aiStandardSurface shader with the current selected color')
            self.ui.specifics_button_1.clicked.connect(self.to_external_maya_commands_1)

            self.ui.specifics_button_2.setIcon(icon_create)
            self.ui.specifics_button_2.setText('Constant')
            self.ui.specifics_button_2.setToolTip('Create a colorConstant node')
            self.ui.specifics_button_2.clicked.connect(self.to_external_maya_commands_2)

            self.ui.specifics_set_label.setText('Set attribute')
            self.ui.specifics_set_input.setText('inColor')
            self.ui.specifics_set_button.clicked.connect(self.to_maya_set)

            self.ui.specifics_get_label.setText('Get attribute')
            self.ui.specifics_get_input.setText('color')
            self.ui.specifics_get_button.clicked.connect(self.to_maya_get)

            self.ui.specifics_io.returnPressed.connect(self.to_external_maya_IO)


        elif self.SOFTWARE == 'nuke':
            self.ui.specifics_label.setText('NUKE')

            self.ui.specifics_button_0.setIcon(icon_paint)
            self.ui.specifics_button_0.setText('Paint sel.')
            self.ui.specifics_button_0.setToolTip('Paint selected nodes with the current selected color')
            self.ui.specifics_button_0.clicked.connect(self.to_external_nuke_commands_0)

            self.ui.specifics_button_1.setIcon(icon_create)
            self.ui.specifics_button_1.setText('Constant')
            self.ui.specifics_button_1.setToolTip('Create a Constant node')
            self.ui.specifics_button_1.clicked.connect(self.to_external_nuke_commands_1)

            self.ui.specifics_button_2.setIcon(icon_create)
            self.ui.specifics_button_2.setText('Backdrop')
            self.ui.specifics_button_2.setToolTip('Create Backdrop around selected nodes')
            self.ui.specifics_button_2.clicked.connect(self.to_external_nuke_commands_2)

            self.ui.specifics_set_label.setText('Set knob value')
            self.ui.specifics_set_input.setText('color')
            self.ui.specifics_set_button.clicked.connect(self.to_nuke_set)

            self.ui.specifics_get_label.setText('Get knob value')
            self.ui.specifics_get_input.setText('tile_color')
            self.ui.specifics_get_button.clicked.connect(self.to_nuke_get)
            
            self.ui.specifics_io.returnPressed.connect(self.to_external_nuke_IO)


        elif self.SOFTWARE == 'generic':

            self.setFixedWidth(442)
            self.setFixedHeight(660)

            self.ui.specifics_divider.setVisible(False)
            self.ui.specifics_label.setVisible(False)
            self.ui.specifics_frame.setVisible(False)

            self.ui.info_button.move(400, 630)
            self.ui.developer_info_label.move(20, 630)

    def make_connections(self):

        # COONNECTIONS FOR RGBA
        self.ui.rgb_double_red.valueChanged.connect(lambda: self.ui.rgb_slider_red.setSliderPosition(self.ui.rgb_double_red.value() * 10000))
        self.ui.rgb_double_green.valueChanged.connect(lambda: self.ui.rgb_slider_green.setSliderPosition(self.ui.rgb_double_green.value() * 10000))
        self.ui.rgb_double_blue.valueChanged.connect(lambda: self.ui.rgb_slider_blue.setSliderPosition(self.ui.rgb_double_blue.value() * 10000))
        self.ui.rgb_double_alpha.valueChanged.connect(lambda: self.ui.rgb_slider_alpha.setSliderPosition(self.ui.rgb_double_alpha.value() * 10000))
            
        for double in self.rgba_doubles:
            double.valueChanged.connect(self.update_rgba_feedback)
            double.valueChanged.connect(self.rgb_to_hsv)
            double.valueChanged.connect(self.rgb_to_hex)
            double.valueChanged.connect(self.rgb_to_cmyk)
            double.valueChanged.connect(self.update_main_feedback)

        self.ui.rgb_slider_red.valueChanged.connect(lambda: self.ui.rgb_double_red.setValue(float(self.ui.rgb_slider_red.value()) / 10000))
        self.ui.rgb_slider_green.valueChanged.connect(lambda: self.ui.rgb_double_green.setValue(float(self.ui.rgb_slider_green.value()) / 10000))
        self.ui.rgb_slider_blue.valueChanged.connect(lambda: self.ui.rgb_double_blue.setValue(float(self.ui.rgb_slider_blue.value()) / 10000))
        self.ui.rgb_slider_alpha.valueChanged.connect(lambda: self.ui.rgb_double_alpha.setValue(float(self.ui.rgb_slider_alpha.value()) / 10000))
 
 
        # ALPHA CHECKBOX
        self.ui.rgb_checkbox_alpha.clicked.connect(self.toggle_alpha)

        # COONNECTIONS FOR HSV
        self.ui.hsv_double_hue.valueChanged.connect(lambda: self.ui.hsv_slider_hue.setSliderPosition(self.ui.hsv_double_hue.value() * 10000))
        self.ui.hsv_double_val.valueChanged.connect(lambda: self.ui.hsv_slider_val.setSliderPosition(self.ui.hsv_double_val.value() * 10000))
        self.ui.hsv_double_sat.valueChanged.connect(lambda: self.ui.hsv_slider_sat.setSliderPosition(self.ui.hsv_double_sat.value() * 10000))

        for double in self.hsv_doubles:
            double.valueChanged.connect(self.update_hsv_feedback)
            double.valueChanged.connect(self.hsv_to_rgb)

        self.ui.hsv_slider_hue.valueChanged.connect(lambda: self.ui.hsv_double_hue.setValue(float(self.ui.hsv_slider_hue.value()) / 10000))
        self.ui.hsv_slider_val.valueChanged.connect(lambda: self.ui.hsv_double_val.setValue(float(self.ui.hsv_slider_val.value()) / 10000))
        self.ui.hsv_slider_sat.valueChanged.connect(lambda: self.ui.hsv_double_sat.setValue(float(self.ui.hsv_slider_sat.value()) / 10000))

        # CONNECTIONS FOR HEX
        self.ui.hex_text.returnPressed.connect(self.hex_to_rgb)

        # CONNECTIONS FOR PANTONE
        self.ui.pantones_checkbox_1.clicked.connect(lambda: self.toggle_pantones(0))
        self.ui.pantones_checkbox_2.clicked.connect(lambda: self.toggle_pantones(1))
        self.ui.pantones_checkbox_3.clicked.connect(lambda: self.toggle_pantones(2))

        self.ui.pantones_coated.currentIndexChanged.connect(lambda: self.update_pantone_feedback(0))
        self.ui.pantones_pastels_neons.currentIndexChanged.connect(lambda: self.update_pantone_feedback(1))
        self.ui.pantones_fashion.currentIndexChanged.connect(lambda: self.update_pantone_feedback(2))

        # CONNECTIONS FOR SPECIFICS
        self.ui.specifics_io.textChanged.connect(lambda: self.ui.specifics_io.setStyleSheet('color:none;'))

        # CONNECTION FOR INFO BUTTON
        self.ui.info_button.clicked.connect(self.open_web)


    def set_validators(self):

        hex_re = QtCore.QRegExp("#?[0-9a-fA-F]{6}")
        hex_validator = QtGui.QRegExpValidator(hex_re)
        self.ui.hex_text.setValidator(hex_validator)


    def update_rgba_feedback(self):

        # Setting values
        r, g, b, a = int(round(self.ui.rgb_double_red.value()*255)), int(round(self.ui.rgb_double_green.value()*255)),\
                     int(round(self.ui.rgb_double_blue.value()*255)) , int(round(self.ui.rgb_double_alpha.value()*255))

        self.ui.rgb_int_red.setValue(r)
        self.ui.rgb_int_green.setValue(g)
        self.ui.rgb_int_blue.setValue(b)


        if not self.ui.rgb_checkbox_alpha.isChecked():
            a = ''
            thereisA = ''
        else:
            a = ',' + str(a)
            thereisA = 'a'

        self.ui.rgb_text_color.setText('rgb{0}({1},{2},{3}{4})'.format(thereisA, r, g, b, a))


    def toggle_alpha(self):

        if self.ui.rgb_checkbox_alpha.isChecked():
            self.ui.rgb_slider_alpha.setEnabled(True)
            self.ui.rgb_slider_alpha.setStyleSheet("QSlider::groove:horizontal"
                                                "{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,"
                                                "stop:0 rgb(0, 0, 0),"
                                                "stop:1 rgb(255, 255,255));"
                                                "height: 5px;"
                                                "border-radius: 2px;}"
                                                "QSlider::handle:horizontal"
                                                "{background:rgb(200,200,200);"
                                                "width: 8px;margin-top: -6px;margin-bottom: -6px;"
                                                "border-radius: 2px;}")

            self.ui.rgb_double_alpha.setEnabled(True)

        else:
            self.ui.rgb_slider_alpha.setDisabled(True)
            self.ui.rgb_slider_alpha.setStyleSheet("QSlider::groove:horizontal"
                                                "{background:none;"
                                                "border:1px dotted gray;"
                                                "height:5px;"
                                                "border-radius: 2px;}"
                                                "QSlider::handle:horizontal"
                                                "background:none;"
                                                "width: 8px;margin-top: -6px;margin-bottom: -6px;"
                                                "border-radius: 2px;}")
            self.ui.rgb_double_alpha.setDisabled(True)


        self.update_rgba_feedback()
        self.update_main_feedback()


    def update_hsv_feedback(self):

        h, s, v = int(round(self.ui.hsv_double_hue.value()*359)), int(round(self.ui.hsv_double_sat.value()*100)),\
                  int(round(self.ui.hsv_double_val.value()*100))

        self.ui.hsv_int_hue.setValue(h)
        self.ui.hsv_int_sat.setValue(s)
        self.ui.hsv_int_val.setValue(v)

        stylesheet_new_hue = 'stop:1 hsv({},255,255));'.format(h)
        self.ui.hsv_slider_sat.setStyleSheet('QSlider::groove:horizontal'
                                          '{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,'
                                          'stop:0 hsv(180,0,125),'
                                          'stop:1 hsv(180,255,255));'
                                          'height: 5px;border-radius:'
                                          '2px;}'
                                          'QSlider::handle:horizontal'
                                          '{background:rgb(200,200,200);'
                                          'width: 8px;'
                                          'margin-top: -6px;'
                                          'margin-bottom: -6px;'
                                          'border-radius: 2px;}'.replace('stop:1 hsv(180,255,255));', stylesheet_new_hue))

        self.ui.hsv_text_color.setText('hsv({0},{1},{2})'.format(h, int(round(self.ui.hsv_double_sat.value()*255)), int(round(self.ui.hsv_double_val.value()*255))))

        
    def update_main_feedback(self):

        r, g, b, a = self.ui.rgb_int_red.value(), self.ui.rgb_int_green.value(),\
                     self.ui.rgb_int_blue.value(), int(round(self.ui.rgb_double_alpha.value()*255))

        if a == 1:
            a -= 1


        h, s, v = self.ui.hsv_int_hue.value(), self.ui.hsv_int_sat.value(), self.ui.hsv_int_val.value()


        if not self.ui.rgb_checkbox_alpha.isChecked():
            a = ''
            thereisA = ''
        else:
            a = ',' + str(a)
            thereisA = 'a'


        self.ui.main_color_label.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,'
                                            'stop:0.49 rgb{isA}({R},{G},{B},255),'
                                            'stop:0.5 rgb{isA}({R},{G},{B}{A}),'
                                            'stop:1 rgb{isA}({R},{G},{B}{A}));'
                                            'border-radius:10px;'.format(isA=thereisA, R=r, G=g, B=b, A=a))

        main_feedback_text = '<html><head/><body><p><span style=" text-decoration: underline;">' \
                             'COLOR PROPERTIES<br/></span>R: {R} / G: {G} / B: {B}' \
                             '<br/> </span> H: {H}º / S: {S}% / V: {V}% < br / > ' \
                             'Hex: {HEX}</p></body></html>'.format(R=r, G=g, B=b, H=h, S=s, V=v, HEX=self.ui.hex_text.text())

        self.ui.main_info_label.setText(main_feedback_text)


    def rgb_to_hsv(self):

        for double in self.hsv_doubles:
            double.valueChanged.disconnect(self.hsv_to_rgb)


        r, g, b = self.rgba_doubles[0].value(), self.rgba_doubles[1].value(), self.rgba_doubles[2].value()

        hsv_from_rgb = colorsys.rgb_to_hsv(r,g,b)
        
        for i in range(3):
            self.hsv_doubles[i].setValue(hsv_from_rgb[i])

        for double in self.hsv_doubles:
            double.valueChanged.connect(self.hsv_to_rgb)


    def hsv_to_rgb(self):

        for double in self.rgba_doubles:
            double.valueChanged.disconnect(self.rgb_to_hsv)


        h, s, v = self.hsv_doubles[0].value(), self.hsv_doubles[1].value(), self.hsv_doubles[2].value()

        rgb_from_hsv = colorsys.hsv_to_rgb(h, s, v)

        for i in range(3):
            self.rgba_doubles[i].setValue(rgb_from_hsv[i])


        for double in self.rgba_doubles:
            double.valueChanged.connect(self.rgb_to_hsv)


    def rgb_to_hex(self):

        r, g, b = self.rgba_ints[0].value(), self.rgba_ints[1].value(), self.rgba_ints[2].value()

        hex_from_rgb = '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)

        self.ui.hex_text.setText(hex_from_rgb)


    def hex_to_rgb(self):

        for double in self.rgba_doubles:
            double.valueChanged.disconnect(self.rgb_to_hex)


        hex = self.ui.hex_text.text()

        if '#' in hex:
            hex = hex[1:]
        else:
            self.ui.hex_text.setText("#" + hex)

        rgb_from_hex = [int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)]

        for i in range(3):
            self.rgba_doubles[i].setValue(float(rgb_from_hex[i])/255)


        for double in self.rgba_doubles:
            double.valueChanged.connect(self.rgb_to_hex)


    def rgb_to_cmyk(self):

        r, g, b = self.rgba_doubles[0].value(), self.rgba_doubles[1].value(), self.rgba_doubles[2].value()

        c = 1 - r
        m = 1 - g
        y = 1 - b

        temp_k = 1
        if c < temp_k:
            temp_k = c
        if m < temp_k:
            temp_k = m
        if y < temp_k:
            temp_k = y
        if temp_k == 1:
            c = 0
            m = 0
            y = 0
        else:
            c = (c - temp_k) / (1 - temp_k)
            m = (m - temp_k) / (1 - temp_k)
            y = (y - temp_k) / (1 - temp_k)

        k = temp_k

        c, m, y, k = int(c*255), int(m*255), int(y*255), int(k*255)

        self.ui.cmyk_swatch_cyan.setStyleSheet('background: hsv(180,255,255,{})'.format(c))
        self.ui.cmyk_swatch_magenta.setStyleSheet('background: hsv(299,255,255,{})'.format(m))
        self.ui.cmyk_swatch_yellow.setStyleSheet('background: hsv(60,255,255,{})'.format(y))
        self.ui.cmyk_swatch_black.setStyleSheet('background: hsv(0,0,0,{})'.format(k))

        self.ui.cmyk_label_cyan .setText(str(c))
        self.ui.cmyk_label_magenta.setText(str(m))
        self.ui.cmyk_label_yellow.setText(str(y))
        self.ui.cmyk_label_black.setText(str(k))


    def load_pantones(self):

        path = os.path.abspath(__file__)
        pantones_dir_path = os.path.dirname(path).replace('\\', '/') + '/pantones/'
        
        # COATED PANTONES
        coated_pantones_path = pantones_dir_path + 'pantone_coated.json'

        with open(coated_pantones_path, 'r') as coated_pantones_data:
            coated_pantones_dict = json.load(coated_pantones_data)

        for color in sorted(coated_pantones_dict.keys()):
            hex = coated_pantones_dict[color]
            rgb_from_hex = [int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)]
            swatch = QtGui.QColor(rgb_from_hex[0], rgb_from_hex[1], rgb_from_hex[2])
            swatch_icon = QtGui.QPixmap(16, 9)
            swatch_icon.fill(swatch)

            name = color.capitalize()

            self.ui.pantones_coated.addItem(swatch_icon, name)
            
        # PASTELS AND NEONS PANTONES
        pastels_neons_pantones_path = pantones_dir_path + 'pantone_pastels_neons.json'

        with open(pastels_neons_pantones_path, 'r') as pastels_neons_pantones_data:
            pastels_neons_pantones_dict = json.load(pastels_neons_pantones_data)

        for color in sorted(pastels_neons_pantones_dict.keys()):
            hex = pastels_neons_pantones_dict[color]
            rgb_from_hex = [int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)]
            swatch = QtGui.QColor(rgb_from_hex[0], rgb_from_hex[1], rgb_from_hex[2])
            swatch_icon = QtGui.QPixmap(16, 9)
            swatch_icon.fill(swatch)

            name = color.capitalize()

            self.ui.pantones_pastels_neons.addItem(swatch_icon, name)

        # FASHION PANTONES
        fashion_pantones_path = pantones_dir_path + 'pantone_fashion.json'

        with open(fashion_pantones_path, 'r') as fashion_pantones_data:
            fashion_pantones_dict = json.load(fashion_pantones_data)

        for color in sorted(fashion_pantones_dict):
            hex = fashion_pantones_dict[color]['hex']
            rgb_from_hex = [int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)]
            swatch = QtGui.QColor(rgb_from_hex[0], rgb_from_hex[1], rgb_from_hex[2])
            swatch_icon = QtGui.QPixmap(16, 9)
            swatch_icon.fill(swatch)

            name = fashion_pantones_dict[color]['name'].capitalize() + ' | ' + color

            self.ui.pantones_fashion.addItem(swatch_icon, name)


    def toggle_pantones(self, index):

        if index == 0:

            if (not self.ui.pantones_checkbox_2.isChecked()) and (not self.ui.pantones_checkbox_3.isChecked()):
                self.ui.pantones_checkbox_1.setCheckState(QtCore.Qt.CheckState.Checked)
            else:
                self.ui.pantones_checkbox_2.setCheckState(QtCore.Qt.CheckState.Unchecked)
                self.ui.pantones_checkbox_3.setCheckState(QtCore.Qt.CheckState.Unchecked)

                self.ui.pantones_coated.setDisabled(False)
                self.ui.pantones_pastels_neons.setDisabled(True)
                self.ui.pantones_fashion.setDisabled(True)

                self.update_pantone_feedback(0)

        elif index == 1:

            if (not self.ui.pantones_checkbox_1.isChecked()) and (not self.ui.pantones_checkbox_3.isChecked()):
                self.ui.pantones_checkbox_2.setCheckState(QtCore.Qt.CheckState.Checked)
            else:
                self.ui.pantones_checkbox_1.setCheckState(QtCore.Qt.CheckState.Unchecked)
                self.ui.pantones_checkbox_3.setCheckState(QtCore.Qt.CheckState.Unchecked)

                self.ui.pantones_coated.setDisabled(True)
                self.ui.pantones_pastels_neons.setDisabled(False)
                self.ui.pantones_fashion.setDisabled(True)

                self.update_pantone_feedback(1)

        elif index == 2:

            if (not self.ui.pantones_checkbox_1.isChecked()) and (not self.ui.pantones_checkbox_2.isChecked()):
                self.ui.pantones_checkbox_3.setCheckState(QtCore.Qt.CheckState.Checked)
            else:
                self.ui.pantones_checkbox_1.setCheckState(QtCore.Qt.CheckState.Unchecked)
                self.ui.pantones_checkbox_2.setCheckState(QtCore.Qt.CheckState.Unchecked)

                self.ui.pantones_coated.setDisabled(True)
                self.ui.pantones_pastels_neons.setDisabled(True)
                self.ui.pantones_fashion.setDisabled(False)

                self.update_pantone_feedback(2)


    def update_pantone_feedback(self, index):

        path = os.path.abspath(__file__)
        pantones_dir_path = os.path.dirname(path).replace('\\', '/') + '/pantones/'


        if index == 0:

            if self.ui.pantones_coated.currentIndex() == 0:
                self.ui.pantone_info_label.setText('')
                self.ui.pantones_swatch_label.setStyleSheet('border-radius:7px;')

                self.ui.rgb_double_red.setValue(0.5)
                self.ui.rgb_double_green.setValue(0.5)
                self.ui.rgb_double_blue.setValue(0.5)

                return

            pantone_name = self.ui.pantones_coated.currentText().lower()

            coated_pantones_path = pantones_dir_path + 'pantone_coated.json'

            with open(coated_pantones_path, 'r') as coated_pantones_data:
                coated_pantones_dict = json.load(coated_pantones_data)

            for color in sorted(coated_pantones_dict.keys()):
                if color == pantone_name:
                    hex = coated_pantones_dict[color]
                    rgb_from_hex = [int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)]
                    self.ui.pantone_info_label.setText('<html><head/><body><p><span style=" font-size:9pt; text-decoration: underline;">'
                                                    'SELECTED {COLOR}<br/></span><span style=" font-size:7pt;">'
                                                    'RGB: {R} {G} {B}<br/>#{HEX}</span></p></body></html>'
                                                    ''.format(COLOR=color, R=rgb_from_hex[0], G=rgb_from_hex[1], B=rgb_from_hex[2], HEX=hex))
                    self.ui.pantones_swatch_label.setStyleSheet('border-radius:7px;'
                                                             'background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,'
                                                             'stop:0 rgba({R}, {G}, {B}, 255),'
                                                             'stop:1 rgba({R}, {G}, {B}, 0));'
                                                             ''.format(R=rgb_from_hex[0], G=rgb_from_hex[1], B=rgb_from_hex[2]))

                    self.ui.rgb_double_red.setValue(float(rgb_from_hex[0])/255)
                    self.ui.rgb_double_green.setValue(float(rgb_from_hex[1])/255)
                    self.ui.rgb_double_blue.setValue(float(rgb_from_hex[2])/255)

                    break

                else:
                    self.ui.pantone_info_label.setText('')
                    self.ui.pantones_swatch_label.setStyleSheet('border-radius:7px;')

        if index == 1:

            if self.ui.pantones_pastels_neons.currentIndex() == 0:
                self.ui.pantone_info_label.setText('')
                self.ui.pantones_swatch_label.setStyleSheet('border-radius:7px;')

                self.ui.rgb_double_red.setValue(0.5)
                self.ui.rgb_double_green.setValue(0.5)
                self.ui.rgb_double_blue.setValue(0.5)

                return

            pantone_name = self.ui.pantones_pastels_neons.currentText().lower()

            pastels_neons_pantones_path = pantones_dir_path + 'pantone_pastels_neons.json'

            with open(pastels_neons_pantones_path, 'r') as pastels_neons_pantones_data:
                pastels_neons_pantones_dict = json.load(pastels_neons_pantones_data)

            for color in sorted(pastels_neons_pantones_dict.keys()):
                if color == pantone_name:
                    hex = pastels_neons_pantones_dict[color]
                    rgb_from_hex = [int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)]
                    self.ui.pantone_info_label.setText('<html><head/><body><p><span style=" font-size:9pt; text-decoration: underline;">'
                                                    'SELECTED {COLOR}<br/></span><span style=" font-size:7pt;">'
                                                    'RGB: {R} {G} {B}<br/>#{HEX}</span></p></body></html>'
                                                    ''.format(COLOR=color, R=rgb_from_hex[0], G=rgb_from_hex[1], B=rgb_from_hex[2], HEX=hex))
                    self.ui.pantones_swatch_label.setStyleSheet('border-radius:7px;'
                                                             'background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,'
                                                             'stop:0 rgba({R}, {G}, {B}, 255),'
                                                             'stop:1 rgba({R}, {G}, {B}, 0));'
                                                             ''.format(R=rgb_from_hex[0], G=rgb_from_hex[1], B=rgb_from_hex[2]))

                    self.ui.rgb_double_red.setValue(float(rgb_from_hex[0])/255)
                    self.ui.rgb_double_green.setValue(float(rgb_from_hex[1])/255)
                    self.ui.rgb_double_blue.setValue(float(rgb_from_hex[2])/255)

                    break

                else:
                    self.ui.pantone_info_label.setText('')
                    self.ui.pantones_swatch_label.setStyleSheet('border-radius:7px;')
                    
        elif index == 2:

            if self.ui.pantones_fashion.currentIndex() == 0:
                self.ui.pantone_info_label.setText('')
                self.ui.pantones_swatch_label.setStyleSheet('border-radius:7px;')

                self.ui.rgb_double_red.setValue(0.5)
                self.ui.rgb_double_green.setValue(0.5)
                self.ui.rgb_double_blue.setValue(0.5)

                return

            pantone_name = self.ui.pantones_fashion.currentText().lower().split('|')[0][:-1]

            fashion_pantones_path = pantones_dir_path + 'pantone_fashion.json'

            with open(fashion_pantones_path, 'r') as fashion_pantones_data:
                fashion_pantones_dict = json.load(fashion_pantones_data)

            for color in sorted(fashion_pantones_dict.keys()):
                if fashion_pantones_dict[color]['name'] == pantone_name:
                    hex = fashion_pantones_dict[color]['hex']
                    rgb_from_hex = [int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)]
                    self.ui.pantone_info_label.setText('<html><head/><body><p><span style=" font-size:9pt; text-decoration: underline;">'
                                                    'SELECTED {COLOR}<br/></span><span style=" font-size:7pt;">'
                                                    'RGB: {R} {G} {B}<br/>#{HEX}</span></p></body></html>'
                                                    ''.format(COLOR=color, R=rgb_from_hex[0], G=rgb_from_hex[1], B=rgb_from_hex[2], HEX=hex))
                    self.ui.pantones_swatch_label.setStyleSheet('border-radius:7px;'
                                                             'background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,'
                                                             'stop:0 rgba({R}, {G}, {B}, 255),'
                                                             'stop:1 rgba({R}, {G}, {B}, 0));'
                                                             ''.format(R=rgb_from_hex[0], G=rgb_from_hex[1], B=rgb_from_hex[2]))

                    self.ui.rgb_double_red.setValue(float(rgb_from_hex[0])/255)
                    self.ui.rgb_double_green.setValue(float(rgb_from_hex[1])/255)
                    self.ui.rgb_double_blue.setValue(float(rgb_from_hex[2])/255)

                    break

                else:
                    self.ui.pantone_info_label.setText('')
                    self.ui.pantones_swatch_label.setStyleSheet('border-radius:7px;')


    def to_external_maya_commands_0(self):

        import external_maya_commands
        reload(external_maya_commands)
        
        input = [self.rgba_doubles[0].value(), self.rgba_doubles[1].value(), self.rgba_doubles[2].value()]
        if self.ui.rgb_checkbox_alpha.isChecked():
            input.append(self.rgba_doubles[3].value())

        response = external_maya_commands.maya_lambert(input)
        self.ui.specifics_io.setText(response[1])
        self.ui.specifics_io.setStyleSheet('color:{};'.format(response[0]))


    def to_external_maya_commands_1(self):

        import external_maya_commands
        reload(external_maya_commands)
        
        input = [self.rgba_doubles[0].value(), self.rgba_doubles[1].value(), self.rgba_doubles[2].value()]
        if self.ui.rgb_checkbox_alpha.isChecked():
            input.append(self.rgba_doubles[3].value())

        response = external_maya_commands.maya_aiStandard(input)
        self.ui.specifics_io.setText(response[1])
        self.ui.specifics_io.setStyleSheet('color:{};'.format(response[0]))


    def to_external_maya_commands_2(self):

        import external_maya_commands
        reload(external_maya_commands)
        
        input = [self.rgba_doubles[0].value(), self.rgba_doubles[1].value(), self.rgba_doubles[2].value()]
        if self.ui.rgb_checkbox_alpha.isChecked():
            input.append(self.rgba_doubles[3].value())

        response = external_maya_commands.maya_constant(input)
        self.ui.specifics_io.setText(response[1])
        self.ui.specifics_io.setStyleSheet('color:{};'.format(response[0]))


    def to_external_maya_IO(self):

        import external_maya_commands
        reload(external_maya_commands)

        input = self.ui.specifics_io.text()
        response = external_maya_commands.maya_IO(input)
        self.ui.specifics_io.setText(response[1])
        self.ui.specifics_io.setStyleSheet('color:{};'.format(response[0]))


    def to_maya_set(self):

        import external_maya_commands
        reload(external_maya_commands)

        color = [self.rgba_doubles[0].value(), self.rgba_doubles[1].value(), self.rgba_doubles[2].value()]

        if self.ui.rgb_checkbox_alpha.isChecked():
            color.append(self.rgba_doubles[3].value())
        else:
            color.append(1)
        response = external_maya_commands.maya_set(str(self.ui.specifics_set_input.text()), color)
        self.ui.specifics_io.setText(response[1])
        self.ui.specifics_io.setStyleSheet('color:{};'.format(response[0]))


    def to_maya_get(self):

        import external_maya_commands
        reload(external_maya_commands)

        response = external_maya_commands.maya_get(str(self.ui.specifics_get_input.text()))
        self.ui.specifics_io.setText(response[1])
        self.ui.specifics_io.setStyleSheet('color:{};'.format(response[0]))


    def to_external_nuke_commands_0(self):

        import external_nuke_commands
        reload(external_nuke_commands)

        r, g, b = self.ui.rgb_int_red.value(), self.ui.rgb_int_green.value(), self.ui.rgb_int_blue.value()
        input = int('{:02X}{:02X}{:02X}{:02X}'.format(r, g, b, 1), 16)
        response = external_nuke_commands.nuke_paint_nodes(input)
        self.ui.specifics_io.setText(response[1])
        self.ui.specifics_io.setStyleSheet('color:{};'.format(response[0]))


    def to_external_nuke_commands_1(self):

        import external_nuke_commands
        reload(external_nuke_commands)

        input = [self.rgba_doubles[0].value(), self.rgba_doubles[1].value(), self.rgba_doubles[2].value()]
        if self.ui.rgb_checkbox_alpha.isChecked():
            input.append(self.rgba_doubles[3].value())
        else:
            input.append(1)
        response = external_nuke_commands.nuke_constant(input)
        self.ui.specifics_io.setText(response[1])
        self.ui.specifics_io.setStyleSheet('color:{};'.format(response[0]))

    def to_external_nuke_commands_2(self):

        import external_nuke_commands
        reload(external_nuke_commands)

        r, g, b = self.ui.rgb_int_red.value(), self.ui.rgb_int_green.value(), self.ui.rgb_int_blue.value()
        input = int('{:02X}{:02X}{:02X}{:02X}'.format(r, g, b, 1), 16)
        response = external_nuke_commands.nuke_backdrop(input)
        self.ui.specifics_io.setText(response[1])
        self.ui.specifics_io.setStyleSheet('color:{};'.format(response[0]))
                
            
    def to_external_nuke_IO(self):
        
        import external_nuke_commands
        reload(external_nuke_commands)

        input = self.ui.specifics_io.text()
        response = external_nuke_commands.nuke_IO(input)
        self.ui.specifics_io.setText(response[1])
        self.ui.specifics_io.setStyleSheet('color:{};'.format(response[0]))
    
    
    def to_nuke_set(self):

        import external_nuke_commands
        reload(external_nuke_commands)

        color = [self.rgba_doubles[0].value(), self.rgba_doubles[1].value(), self.rgba_doubles[2].value()]

        if self.ui.rgb_checkbox_alpha.isChecked():
            color.append(self.rgba_doubles[3].value())
        else:
            color.append(1)
        response = external_nuke_commands.nuke_set(str(self.ui.specifics_set_input.text()), color)
        self.ui.specifics_io.setText(response[1])
        self.ui.specifics_io.setStyleSheet('color:{};'.format(response[0]))


    def to_nuke_get(self):

        import external_nuke_commands
        reload(external_nuke_commands)

        response = external_nuke_commands.nuke_get(str(self.ui.specifics_get_input.text()))
        self.ui.specifics_io.setText(response[1])
        self.ui.specifics_io.setStyleSheet('color:{};'.format(response[0]))


    def open_web(self):

        import webbrowser
        webbrowser.open('www.jaimervq.com')


    def run(self):
        self.show()