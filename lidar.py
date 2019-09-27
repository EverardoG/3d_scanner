import serial
import math
import matplotlib.pyplot as plt

# create our figure for plotting
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

# set up with the arduino
arduinoComPort = "/dev/ttyACM0"
baudRate = 9600
serialPort = serial.Serial(arduinoComPort, baudRate, timeout = 1)

# get 360 points worth of data from the scanner
angleList = []
magList = []
i = 0
while i < 360:
    # get data from serial
    lineOfData = serialPort.readline().decode()

    # extract angle and magnitude
    if len(lineOfData) > 0 and ":" in lineOfData:
        angle, magnitude = lineOfData.split(":");
        angleList.append(int(angle))
        magList.append(float(magnitude))
        i+=1

# map the polar coordinates to xy coordinates
xs = []
ys = []
for i in range(len(angleList)):
    cm = magList[i]
    if cm > 150:
        cm = 150

    xs.append( cm * math.cos(3.14/180.0 * angleList[i]) )
    ys.append( cm * math.sin(3.14/180.0 * angleList[i]) )

# plot our data
ax1.plot(xs,ys,'.')
ax1.set_xlim(-150, 150)
ax1.axis('equal')
plt.show()