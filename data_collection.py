import serial
import math
import numpy as np
from datetime import datetime as dt

# arduino set up
arduinoComPort = "/dev/ttyACM0"
baudRate = 9600
serialPort = serial.Serial(arduinoComPort, baudRate, timeout = 1)

# lists for storing data from scan
pan_angleList = []
tilt_angleList = []
magList = []
magListFiltered = []

# setup variables for scanning
keep_scanning = True
scan_started = False

# main data collection loop
while keep_scanning:
    # get the new line of data
    lineOfData = serialPort.readline().decode()

    # start scanning
    if "START" in lineOfData and not scan_started:
        scan_started = True
        print("scan started")

    # get the line of data, store information, keep scanning
    elif scan_started and len(lineOfData) > 0 and ":" in lineOfData:
        pan_angle, tilt_angle, magnitude, mag_filtered = lineOfData.split(":")

        pan_angleList.append(int(pan_angle))
        tilt_angleList.append(int(tilt_angle))
        magList.append(float(magnitude))
        magListFiltered.append(float(mag_filtered))

    # stop scanning
    elif scan_started and "START" in lineOfData:
        keep_scanning = False
        print("scan finished")

# convert lists to numpy arrays for storage
pans_ = np.asarray(pan_angleList)
tilts_ = np.asarray(tilt_angleList)
cms_ = np.asarray(magList)
cms_f = np.asarray(magListFiltered)

# add a time stamp to the data and save it
timestamp = "_".join(str(dt.now()).split())
np.savez('data_' + timestamp + '.npz', p = pans_, t = tilts_, c = cms_, f = cms_f)