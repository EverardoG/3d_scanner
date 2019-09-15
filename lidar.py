import serial
import math

import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from matplotlib import style
# style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

arduinoComPort = "/dev/ttyACM0"

baudRate = 9600

serialPort = serial.Serial(arduinoComPort, baudRate, timeout = 1)

angleList = []
magList = []
i = 0
while i < 360:
    # try:
    lineOfData = serialPort.readline().decode()

    # except:
    #     pass


    if len(lineOfData) > 0 and ":" in lineOfData:
        angle, magnitude = lineOfData.split(":");
        # print(angle, magnitude)

        angleList.append(int(angle))
        magList.append(int(magnitude))
        # plt.show()
        i+=1

# ax1.clear()
# ax1.plot(angleList,magList,'.')
# print(angleList)
# print(magList)

xs = []
ys = []

for i in range(len(angleList)):
    cm = magList[i]
    if cm > 150:
        cm = 150

    xs.append( cm * math.cos(3.14/180.0 * angleList[i]) )
    ys.append( cm * math.sin(3.14/180.0 * angleList[i]) )

ax1.plot(xs,ys,'.')
ax1.set_xlim(-150, 150)
ax1.axis('equal')

plt.show()

        # print(lineOfData)
        # print(len(lineOfData))
        # for char in lineOfData:
        #     if char == ":":
        #         print(":")
        #         angle, magnitude = lineOfData.split(":")
        # # print(angle, ":" , magnitude)