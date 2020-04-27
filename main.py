#Quick solution to control the settings of your webcam through the v412-ctl package available on Linux.
#Authors: Christian Dorfer (dorfer@phys.ethz.ch), Joan Serra (serrajoan@me.com)

"""
Requirements:
    - pip install sh
    - pip install pyqt5 (needs Qt5 backend on system)
    - v4l-utils: Use your package manger of choice (e.g. apt-get install v4l-utils)
    
Usage:
    python main.py
    
"""

import sh
import re
import sys
import logging
from time import sleep
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QSlider
from PyQt5.Qt import Qt, QLabel, QGridLayout, QPushButton


logging.basicConfig(level=logging.DEBUG)

class CameraControl(object):
    """
    Interface class to the v4l2-ctl package.
    All possible controls in the __init__ method were obtained by running 'v4l2-ctl --list-ctrls'.
    """
    
  
    def __init__(self):
        self.cmd = sh.Command("/usr/bin/v4l2-ctl")
        self.autofocus = False
        
        #key=name : type, min, max, step, default
        self.ctrls={
        'brightness':['int',-64,64,1,0],
        'contrast':['int',0,64,1,32],
        'backlight_compensation':['int',0,2,1,1],
        'exposure_absolute':['int',1,5000,1,156],
        'exposure_auto':['menu',0,3,1,3],
        'power_line_frequency':['menu',0,2,1,1],
        'saturation':['int',0,128,1,64],
        'sharpness':['int',0,6,1,0],
        'white_balance_temperature':['int',2800,6500,1,4600],
        'white_balance_temperature_auto':['bool', 1,1,1,1],
        }
        
    def getValue(self, name):
        try:
            ret = self.cmd("--get-ctrl", name)
            logging.debug("Got return: {}".format(ret))
            val = [int(d) for d in re.findall(r'-?\d+', str(ret))]
            logging.debug("Got value: {}".format(val))
            return val[0]
        except:        
            print('Ups, could not read value.')
            pass
        
    def setValue(self, name, val):
        try:
            self.cmd("--set-ctrl", (name+"="+str(val)))
        except:
            print('Ups, could not set value for ', name, '.')
            pass
    
     
    def resetControls(self):
        self.setValue('backlight_compensation', self.ctrls['backlight_compensation'][4])
        self.setValue('brightness', self.ctrls['brightness'][4])
        self.setValue('sharpness', self.ctrls['sharpness'][4])
        self.setValue('contrast', self.ctrls['contrast'][4])


class Window(QWidget):  
    def __init__(self, cc):
        super().__init__()
        
        self.camCtr = cc
        self.initUI()
        
        
    def initUI(self):
        self.setWindowTitle('Camera Control')
        self.setMinimumWidth(260)
        self.grid = QGridLayout()
        self.grid.setContentsMargins(4, 4, 4, 4)
        self.grid.setSpacing(2)
        
        ### add control elements ###
        self.backlight_lbl = QLabel("Backlight Compensation")
        self.grid.addWidget(self.backlight_lbl, 10,1,1,1, Qt.AlignLeft)
        self.backlight_comp_sl = QSlider()
        self.backlight_comp_sl.setOrientation(Qt.Horizontal)   
        self.backlight_comp_sl.setValue(self.camCtr.getValue('backlight_compensation'))
        self.backlight_comp_sl.setTickInterval(1)
        self.backlight_comp_sl.setMaximum(self.camCtr.ctrls['backlight_compensation'][2])
        self.backlight_comp_sl.setMinimum(self.camCtr.ctrls['backlight_compensation'][1])
        self.backlight_comp_sl.valueChanged.connect(self.backlight_com_sl_Change)
        self.backlight_comp_sl.setMinimumWidth(200)
        self.grid.addWidget(self.backlight_comp_sl, 10,2,1,1, Qt.AlignRight)
        
        self.brightness_lbl = QLabel("Brightness")
        self.grid.addWidget(self.brightness_lbl, 12,1,1,1, Qt.AlignLeft)
        self.brightness_sl = QSlider()
        self.brightness_sl.setOrientation(Qt.Horizontal)   
        self.brightness_sl.setValue(self.camCtr.getValue('brightness'))
        self.brightness_sl.setTickInterval(1)
        self.brightness_sl.setMaximum(self.camCtr.ctrls['brightness'][2])
        self.brightness_sl.setMinimum(self.camCtr.ctrls['brightness'][1])
        self.brightness_sl.valueChanged.connect(self.brighness_sl_Change)
        self.brightness_sl.setMinimumWidth(200)
        self.grid.addWidget(self.brightness_sl, 12,2,1,1, Qt.AlignRight)

        self.sharpness_lbl = QLabel("Sharpness")
        self.grid.addWidget(self.sharpness_lbl, 13,1,1,1, Qt.AlignLeft)
        self.sharpness_sl = QSlider()
        self.sharpness_sl.setOrientation(Qt.Horizontal)   
        self.sharpness_sl.setValue(self.camCtr.getValue('sharpness'))
        self.sharpness_sl.setTickInterval(1)
        self.sharpness_sl.setMaximum(self.camCtr.ctrls['sharpness'][2])
        self.sharpness_sl.setMinimum(self.camCtr.ctrls['sharpness'][1])
        self.sharpness_sl.valueChanged.connect(self.sharpness_sl_Change)
        self.sharpness_sl.setMinimumWidth(200)
        self.grid.addWidget(self.sharpness_sl, 13,2,1,1, Qt.AlignRight)
        
        self.contrast_lbl = QLabel("Contrast")
        self.grid.addWidget(self.contrast_lbl, 14,1,1,1, Qt.AlignLeft)
        self.contrast_sl = QSlider()
        self.contrast_sl.setOrientation(Qt.Horizontal)   
        self.contrast_sl.setValue(self.camCtr.getValue('contrast'))
        self.contrast_sl.setTickInterval(1)
        self.contrast_sl.setMaximum(self.camCtr.ctrls['contrast'][2])
        self.contrast_sl.setMinimum(self.camCtr.ctrls['contrast'][1])
        self.contrast_sl.valueChanged.connect(self.contrast_sl_Change)
        self.contrast_sl.setMinimumWidth(200)
        self.grid.addWidget(self.contrast_sl, 14,2,1,1, Qt.AlignRight)
        
        self.reset = QPushButton()
        self.reset.setText('Reset')
        self.reset.clicked.connect(self.reset_Slot)
        self.grid.addWidget(self.reset, 17,1,1,1, Qt.AlignCenter)
        
        ### end adding control elements      
        
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.grid)
        self.setLayout(self.mainLayout)
        self.show()
  
  
    def backlight_com_sl_Change(self):
        self.camCtr.setValue('backlight_compensation', self.backlight_comp_sl.value())

    def brighness_sl_Change(self):
        self.camCtr.setValue('brightness', self.brightness_sl.value())
        
    def sharpness_sl_Change(self):
        self.camCtr.setValue('sharpness', self.sharpness_sl.value())
        
    def contrast_sl_Change(self):
        self.camCtr.setValue('contrast', self.contrast_sl.value())

       
    def reset_Slot(self):
        self.camCtr.resetControls()
        self.backlight_comp_sl.setValue(self.camCtr.ctrls['backlight_compensation'][4])
        self.brightness_sl.setValue(self.camCtr.ctrls['brightness'][4])
        self.sharpness_sl.setValue(self.camCtr.ctrls['sharpness'][4])
        self.contrast_sl.setValue(self.camCtr.ctrls['contrast'][4])           
            
            
            
if __name__ == '__main__':
    camCtr = CameraControl()
    app = QApplication(sys.argv)
    window = Window(camCtr)
    sys.exit(app.exec_())
