import math
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from os import listdir
from os.path import isfile, join

# if statement for loading in the most recently taken data
if True:
    npz_files = [f for f in listdir(".") if isfile(f) and ".npz" in f]
    npz_files.sort(reverse=True)
    npz_file = npz_files[0]

# selecting a file
npz_data = np.load(npz_file)

# loading in the data
pan_angleList = npz_data['p']
tilt_angleList = npz_data['t']
magList = npz_data['c']
# magList = npz_data['f']

# convert the spherical data to xyz data
xs = []
ys = []
zs = []
for i in range(len(pan_angleList)):
    cm = float(magList[i])

    x = cm * math.cos(3.14/180.0 *  pan_angleList[i])
    z = cm * math.sin(3.14/180.0 *  pan_angleList[i]) * math.sin( 3.14/180.0 * tilt_angleList[i] )
    y = cm * math.sin(3.14/180.0 *  pan_angleList[i]) * math.cos( 3.14/180.0 * tilt_angleList[i] )

    if y < 40: #cm < 150.0 and y < 30 and y > 25 and z < 40:
        xs.append( x )
        ys.append( y )
        zs.append( z )

# create a figure for plotting on
fig = plt.figure()
ax1 = fig.add_subplot(111, projection = "3d")


# this if statement was an experiment in plotting points as a mesh
# - interesting but fruitless
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

# this if statement was exploring the possibility of filling in
# missing data points using a machine learning algorithm
# This one was actually pretty awesome
ml = 0
if ml:
    # pre processing data
    X = np.ones((len(xs), 1))
    Y = np.ones((len(xs), 1))
    Z = np.ones((len(xs), 1))

    X[:,0] = np.asarray(xs)
    Y[:,0] = np.asarray(ys)
    Z[:,0] = np.asarray(zs)

    # our input will be the x and z data
    INPUT = np.concatenate((X,Z), axis = 1)

    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process import kernels
    gp = GaussianProcessRegressor(kernel=kernels.RBF(10, (1e-2, 1e2)))
    import time

    # and now we fit the y data to the x and z data
    # so that the letter appears as a surface
    print("machine learning started at " + str(time.time()))
    gp.fit(INPUT, Y)
    print("finished at " + str(time.time()))

    # we create a grid of x and z points
    full_arr = np.array([[],[]]).transpose()
    z_shape = np.linspace(-10,30,50)
    zss = np.ones((len(z_shape), 1))
    zss[:,0] = z_shape
    for x_val in np.linspace(-15,30,50):
        row_arr = np.ones(zss.shape)
        row_arr*= x_val
        row_arr2 = np.concatenate( ( row_arr, zss ) , axis = 1 )
        full_arr = np.concatenate( (full_arr, row_arr2), axis = 0 )

    # and then we put all of it together by predicting y values for everything
    Y_pred = gp.predict(full_arr)

    ax = fig.add_subplot(1, 2, 1, projection='3d')

    ax.plot(full_arr[:,0],Y_pred,full_arr[:,1],"b.")
    ax.plot(xs,ys,zs, "r.")

    ax.set_xlim(-15, 15)
    ax.set_ylim(0, 30)
    ax.set_zlim(0,30)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    # filtered out to just an outline the letter
    xs_ = []
    ys_ = []
    zs_ = []
    for i in range(full_arr.shape[0]):
        if Y_pred[i] < 0.1:
            xs_.append(full_arr[i,0])
            ys_.append(Y_pred[i])
            zs_.append(full_arr[i,1])

    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.plot(xs_, ys_, zs_ , "b.")
    ax2.plot(xs,ys,zs, "r.")
    ax2.set_xlim(-15, 15)
    ax2.set_ylim(0, 30)
    ax2.set_zlim(0,30)
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_zlabel("z")

# this is the default behaviour where it just
# visualizes our data as a point cloud
else:
    ax1.plot(xs,ys,zs, "r.")
    ax1.set_xlim(-5, 25)
    ax1.set_ylim(15, 45)
    ax1.set_zlim(-10,20)
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_zlabel("z")
    # ax1.axis('equal')

plt.show()