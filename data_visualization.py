import math
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from os import listdir
from os.path import isfile, join

if True:
    npz_files = [f for f in listdir(".") if isfile(f) and ".npz" in f]
    npz_files.sort(reverse=True)
    npz_file = npz_files[0]

npz_data = np.load(npz_file)

pan_angleList = npz_data['p']
tilt_angleList = npz_data['t']
magList = npz_data['c']
magList = npz_data['f']

xs = []
ys = []
zs = []
for i in range(len(pan_angleList)):
    cm = float(magList[i])
    y_offset = 0
    x_offset = 0
    z_offset = 0

    x = cm * math.cos(3.14/180.0 *  pan_angleList[i]) + z_offset
    z = cm * math.sin(3.14/180.0 *  pan_angleList[i]) * math.sin( 3.14/180.0 * tilt_angleList[i] ) + y_offset
    y = cm * math.sin(3.14/180.0 *  pan_angleList[i]) * math.cos( 3.14/180.0 * tilt_angleList[i] ) + z_offset

    if True: #cm < 150.0 and y < 30 and y > 25 and z < 40:
        xs.append( x )
        ys.append( y )
        zs.append( z )

fig = plt.figure()
ax1 = fig.add_subplot(111, projection = "3d")

# this experiment was neat but pretty much fruitless
surface = False
if surface:
    import matplotlib.tri as mtri
    u = np.linspace( -2.0 * np.pi, 2.0 * np.pi, endpoint=True, num=25)
    v = np.linspace( -2.0 * np.pi, 2.0 * np.pi, endpoint=True, num=25)
    u, v = np.meshgrid(u, v)
    u, v = u.flatten(), v.flatten()

    # Triangulate parameter space to determine the triangles
    tri = mtri.Triangulation(u, v)

    # Plot the surface.  The triangles in parameter space determine which x, y, z
    # points are connected by an edge.
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    # ax.plot_trisurf(xs, ys, zs, cmap=plt.cm.Spectral)
    # ax.set_zlim(-1, 1)
    ax.plot(xs,ys,zs, ".")

    ax.set_xlim(-15, 15)
    ax.set_ylim(0, 30)
    ax.set_zlim(0,30)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    # ax1.plot_trisurf(X = xs, Y = ys, triangles = triangles, Z = zs)
    # x = 0

# let's see if I can throw ml at it
ml = True
if ml:

    X = np.ones((len(xs), 1))
    Y = np.ones((len(xs), 1))
    Z = np.ones((len(xs), 1))

    X[:,0] = np.asarray(xs)
    Y[:,0] = np.asarray(ys)
    Z[:,0] = np.asarray(zs)

    INPUT = np.concatenate((X,Z), axis = 1)

    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process import kernels
    gp = GaussianProcessRegressor(kernel=kernels.RBF(10, (1e-2, 1e2)))
    gp.fit(INPUT, Z)

    ax = fig.add_subplot(1, 1, 1, projection='3d')

    ax.plot(xs,ys,zs, ".")

    ax.set_xlim(-15, 15)
    ax.set_ylim(0, 30)
    ax.set_zlim(0,30)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

else:
    ax1.plot(xs,ys,zs, ".")
    ax1.set_xlim(-15, 15)
    ax1.set_ylim(0, 35)
    ax1.set_zlim(0,30)
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_zlabel("z")
    # ax1.axis('equal')

plt.show()
