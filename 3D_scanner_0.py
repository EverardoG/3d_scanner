import serial
import math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
# import matplotlib.animation as animation
# from matplotlib import style
# style.use('fivethirtyeight')

fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)
ax1 = fig.add_subplot(111, projection = "3d")

arduinoComPort = "/dev/ttyACM0"

baudRate = 9600

serialPort = serial.Serial(arduinoComPort, baudRate, timeout = 1)

pan_angleList = []
tilt_angleList = []
magList = []

keep_scanning = True
scan_started = False

k = 0

while keep_scanning:
    # try:
    lineOfData = serialPort.readline().decode()

    if "START" in lineOfData and not scan_started:
        scan_started = True
        print("scan started")

    elif scan_started and len(lineOfData) > 0 and ":" in lineOfData:
        pan_angle, tilt_angle, magnitude = lineOfData.split(":")

        pan_angleList.append(int(pan_angle))
        tilt_angleList.append(int(tilt_angle))
        magList.append(int(magnitude))

    elif scan_started and "START" in lineOfData:
        keep_scanning = False
        print("scan finished")

    print(k)
    k+=1

xs = []
ys = []
zs = []

for i in range(len(pan_angleList)):
    cm = float(magList[i])
    if cm > 150.0:
        cm = 150.0

    x = cm * math.cos(3.14/180.0 *  pan_angleList[i])
    y = cm * math.sin(3.14/180.0 *  pan_angleList[i])
    z = math.sqrt(x**2 + y**2) * math.sin(3.14/180.0 * tilt_angleList[i])
    xs.append( x )
    ys.append( y )
    zs.append( z )

pans_ = np.asarray(pan_angleList)
tilts_ = np.asarray(tilt_angleList)
cms_ = np.asarray(magList)

np.savez('data.npz', p = pans_, t = tilts_, c = cms_)

# with open('data.pickle','wb') as f:
#     pickle.dump()

ax1.plot(xs, ys, zs,'.')
ax1.set_xlim(-150, 150)
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.set_zlabel("z")
# ax1.axis('equal')

plt.show()
