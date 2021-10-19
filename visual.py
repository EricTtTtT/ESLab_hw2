import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

acc_max = 5.0


plt.ion()
fig = plt.figure()
ax_xy = fig.add_subplot(2, 2, 2)
ax_xy.set_xlim([-acc_max, acc_max])
ax_xy.set_xlabel('a_x')
ax_xy.set_ylim([-acc_max, acc_max])
ax_xy.set_ylabel('a_y')


ax_z = fig.add_subplot(2, 10, 18)
ax_z.set_ylim([-acc_max, acc_max])
ax_z.set_ylabel('a_z')

ax_z.set_xlim([0, 1])


ax = fig.add_subplot(1, 2, 1, projection='3d')
ax.set_xlim3d([0.0, 10.0])
ax.set_xlabel('X')

ax.set_ylim3d([0.0, 10.0])
ax.set_ylabel('Y')

ax.set_zlim3d([0.0, 10.0])
ax.set_zlabel('Z')

X_range = 100
x_input = [i*0.1 for i in range(X_range)]
y_input = [i*0.1 for i in range(X_range)]
z_input = [i*0.1 for i in range(X_range)]

for k in range(X_range-1):
    ax.plot(x_input[k:k+1], y_input[k:k+1], z_input[k:k+1], 'ro')

    # ax_xy.plot()

    plt.draw()
    plt.pause(0.001)
    if k % 50 == 0:
        plt.cla()
        ax.set_xlim3d([0.0, 10.0])
        ax.set_xlabel('X')

        ax.set_ylim3d([0.0, 10.0])
        ax.set_ylabel('Y')

        ax.set_zlim3d([0.0, 10.0])
        ax.set_zlabel('Z')
    
