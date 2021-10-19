import collections
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

acc_max = 10
ani_t_scale = 5.0
ani_interval = 200
ani_total = ani_t_scale * 1000 / ani_interval


fig = plt.figure()
ax_x = fig.add_subplot(2, 3, 4)
ax_y = fig.add_subplot(2, 3, 5)
ax_z = fig.add_subplot(2, 3, 6)

time_axis = np.array([i * ani_interval / 1000 for i in range(int(ani_total))])
time_axis -= ani_t_scale


# modify data here
x_accelerator = np.random.rand(200) * 10
y_accelerator = np.random.rand(200) * 10
z_accelerator = np.random.rand(200) * 10
x_data = collections.deque(np.zeros(int(ani_total)))
y_data = collections.deque(np.zeros(int(ani_total)))
z_data = collections.deque(np.zeros(int(ani_total)))

def refresh_plot(i):
    global ani_interval
    global time_axis

    time_axis += ani_interval/1000

    x_data.popleft()
    x_data.append(x_accelerator[i])
    ax_x.cla()
    ax_x.set_xlabel('time')
    ax_x.set_xlim(time_axis[0], time_axis[-1])
    ax_x.set_ylabel('x-axis accelerator')
    # ax_x.set_ylim(-acc_max, acc_max)
    ax_x.plot(time_axis, x_data)

    y_data.popleft()
    y_data.append(y_accelerator[i])
    ax_y.cla()
    ax_y.set_xlabel('time')
    ax_y.set_xlim(time_axis[0], time_axis[-1])
    ax_y.set_ylabel('y-axis accelerator')
    # ax_y.set_ylim(-acc_max, acc_max)
    ax_y.plot(time_axis, y_data)
    
    z_data.popleft()
    z_data.append(z_accelerator[i])
    ax_z.cla()
    ax_z.set_xlabel('time')
    ax_z.set_xlim(time_axis[0], time_axis[-1])
    ax_z.set_ylabel('z-axis accelerator')
    # ax_z.set_ylim(-acc_max, acc_max)
    ax_z.plot(time_axis, z_data)

ani = FuncAnimation(fig, refresh_plot, interval=ani_interval)
plt.show()






# ax = fig.add_subplot(1, 2, 1, projection='3d')
# ax.set_xlim3d([0.0, 10.0])
# ax.set_xlabel('X')
# ax.set_ylim3d([0.0, 10.0])
# ax.set_ylabel('Y')
# ax.set_zlim3d([0.0, 10.0])
# ax.set_zlabel('Z')
# for k in range(X_range-1):
#     ax.plot(x_input[k:k+1], y_input[k:k+1], z_input[k:k+1], 'ro')