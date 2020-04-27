GUI for the v412-ctl package on Linux.

Used to adjust some basic parameters of your webcam.

The basic parameters have been added to the script, but your mileage may vary depending on what webcam you have. To see a list of your webcam supported parameters, run `v4l2-ctl --list-ctrls`

You will also probably want to change the default values and steps for each parameter, as the ones in the script are for my particular camera (oem Chinese from Amazon thing)

![alt tag](https://cloud.githubusercontent.com/assets/8195877/23632581/b2fd3aee-02c2-11e7-8cbe-f7b983798d92.png)
![alt tag](https://cloud.githubusercontent.com/assets/8195877/23632582/b2fe2cf6-02c2-11e7-803e-5a45f8a06a5f.png)

### Requirements:
- Python 3 (due to Qt5)
- Qt5 backend
- v4l-utils (Use your package manger of choice (e.g. apt-get install v4l-utils)

#### Pip packages
- pip install sh
- pip install pyqt5 (needs Qt5 backend on system)
    
### Usage:
    python main.py
