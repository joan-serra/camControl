#Quick solution to control a Microsoft Live Cam through the v412-ctl package on Linux
#Author: Christian Dorfer (dorfer@phys.ethz.ch)


import sh
import sys
from time import sleep
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QSlider
from PyQt5.Qt import Qt, QLabel, QGridLayout, QPushButton


class CameraControl(object):
    
    def __init__(self):
        self.cmd = sh.Command("/usr/bin/v4l2-ctl")
        
        self.backlight_compensation_min = 0
        self.backlight_compensation_max = 10
        self.brightness_min = 30
        self.brightness_max = 255
        self.focus_absolute_min = 0
        self.focus_absolute_max = 40
        
    def getControls(self):
        return self.cmd("--list-ctrls")

    def getBacklightCompensation(self):
        ret = self.cmd("--get-ctrl", "backlight_compensation")
        num = [int(s) for s in ret.split() if s.isdigit()]
        return num[0]  
    
    def setBacklightCompensation(self, val):
        self.cmd("--set-ctrl", ("brightness=" + str(val)))  
         
    def getBrightness(self):
        ret = self.cmd("--get-ctrl", "brightness")
        num = [int(s) for s in ret.split() if s.isdigit()]
        return num[0]  
  
    def setBrightness(self, val):
        self.cmd("--set-ctrl", ("backlight_compensation=" + str(val)))      
    
    def getFocusAbsolute(self):
        ret = self.cmd("--get-ctrl", "focus_absolute")
        num = [int(s) for s in ret.split() if s.isdigit()]
        return num[0]
    
    def setFocusAbsolute(self, val):
        self.cmd("--set-ctrl", ("focus_absolute=" + str(val)))
        
    def resetControls(self):
        self.cmd("--set-ctrl", "backlight_compensation=5")
        self.cmd("--set-ctrl", "brightness=133")
        self.cmd("--set-ctrl", "focus_absolute=5")
  
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
        self.backlight_comp_sl.setValue(self.camCtr.getBacklightCompensation())
        self.backlight_comp_sl.setTickInterval(1)
        self.backlight_comp_sl.setMaximum(self.camCtr.backlight_compensation_max)
        self.backlight_comp_sl.setMinimum(self.camCtr.backlight_compensation_min)
        self.backlight_comp_sl.valueChanged.connect(self.backlight_com_sl_Change)
        self.backlight_comp_sl.setMinimumWidth(200)
        self.grid.addWidget(self.backlight_comp_sl, 10,2,1,1, Qt.AlignRight)
        
        self.brightness_lbl = QLabel("Brightness")
        self.grid.addWidget(self.brightness_lbl, 12,1,1,1, Qt.AlignLeft)
        self.brightness_sl = QSlider()
        self.brightness_sl.setOrientation(Qt.Horizontal)   
        self.brightness_sl.setValue(self.camCtr.getFocusAbsolute())
        self.brightness_sl.setTickInterval(1)
        self.brightness_sl.setMaximum(self.camCtr.brightness_max)
        self.brightness_sl.setMinimum(self.camCtr.brightness_min)
        self.brightness_sl.valueChanged.connect(self.brighness_sl_Change)
        self.brightness_sl.setMinimumWidth(200)
        self.grid.addWidget(self.brightness_sl, 12,2,1,1, Qt.AlignRight)
          
        self.focabs_lbl = QLabel("Absolute Focus")
        self.grid.addWidget(self.focabs_lbl, 13,1,1,1, Qt.AlignLeft)
        self.focabs_sl = QSlider()
        self.focabs_sl.setOrientation(Qt.Horizontal)   
        self.focabs_sl.setValue(self.camCtr.getFocusAbsolute())
        self.focabs_sl.setTickInterval(1)
        self.focabs_sl.setMaximum(self.camCtr.focus_absolute_max)
        self.focabs_sl.setMinimum(self.camCtr.focus_absolute_min)
        self.focabs_sl.valueChanged.connect(self.focabs_sl_Change)
        self.focabs_sl.setMinimumWidth(200)
        self.grid.addWidget(self.focabs_sl, 13,2,1,1, Qt.AlignRight)
        
        self.reset = QPushButton()
        self.reset.setText('Reset')
        self.reset.clicked.connect(self.reset_Slot)
        self.grid.addWidget(self.reset, 14,1,1,2, Qt.AlignCenter)
        
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.grid)
        self.setLayout(self.mainLayout)
        self.show()
  
  
  
    def backlight_com_sl_Change(self):
        self.camCtr.setBacklightCompensation(self.backlight_comp_sl.value())
        print(self.backlight_comp_sl.value())

    def brighness_sl_Change(self):
        self.camCtr.setBrightness(self.brightness_sl.value())
        print(self.brightness_sl.value())
        
    def focabs_sl_Change(self):
        self.camCtr.setFocusAbsolute(self.focabs_sl.value())
        print(self.focabs_sl.value())
       
    def reset_Slot(self):
        self.camCtr.resetControls()
        self.backlight_comp_sl.setValue(self.camCtr.getBacklightCompensation())
        self.brightness_sl.setValue(self.camCtr.getFocusAbsolute())
        self.focabs_sl.setValue(self.camCtr.getFocusAbsolute())
        
      
        
if __name__ == '__main__':
    camCtr = CameraControl()
    app = QApplication(sys.argv)
    window = Window(camCtr)
    sys.exit(app.exec_())
