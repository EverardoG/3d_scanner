import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

npzfile = np.load("data.npz")
pan_angleList = npzfile['p']
# tilt_angleList = np.zeros((144))
tilt_angleList = npzfile['t']
magList = npzfile['c']

# for i in range(cms.shape[0]):
#     if cms[i] > 150.0:
#         cms[i] = 150

# print(pans)
# print(tilts)
# print(cms)

xs = []
ys = []
zs = []
for i in range(len(pan_angleList)):
    # if ( tilt_angleList[i] == -30 ):
    cm = float(magList[i])
    if cm > 150.0:
        cm = 150.0

    y_offset = 0
    x_offset = 0
    z_offset = 0

    # x = cm * math.cos(3.14/180.0 *  pan_angleList[i])
    # y = cm * math.sin(3.14/180.0 *  pan_angleList[i])
    # z = math.sqrt(x**2 + y**2) * math.sin(3.14/180.0 * tilt_angleList[i])

    y = cm * math.cos(3.14/180.0 *  pan_angleList[i])
    x = cm * math.sin(3.14/180.0 *  pan_angleList[i]) * math.sin( 3.14/180.0 * tilt_angleList[i] )
    # z = math.sqrt(x**2 + y**2) * math.sin(3.14/180.0 * tilt_angleList[i]) *1.0/2.0
    z = cm * math.sin(3.14/180.0 *  pan_angleList[i]) * math.cos( 3.14/180.0 * tilt_angleList[i] ) + z_offset

    xs.append( x )
    ys.append( y )
    zs.append( z )

# print(xs)
# print(ys)
# print(zs)

fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)
ax1 = fig.add_subplot(111, projection = "3d")

# ax1.plot_wireframe(np.asarray(xs), np.asarray(ys), np.asarray(zs),'.')


# X , Y = np.meshgrid(xs, ys)

# for i in X.shape[0]:
#     for j in X.shape[1]:
#         Z[i,j] =

# print(X.shape)
# print(Y.shape)
# print(Z.shape)

# ax1.plot_wireframe(X, Y, Z)


ax1.plot(xs,ys,zs, ".")
ax1.set_xlim(-50, 50)
ax1.set_ylim(0, 30)
ax1.set_zlim(-10,30)
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.set_zlabel("z")
# ax1.axis('equal')

plt.show()
