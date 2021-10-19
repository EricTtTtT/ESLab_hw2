import collections
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json

# config
acc_max = 10
ani_window_sec = 5.0
ani_interval = 100

fig = plt.figure()
ax_x = fig.add_subplot(2, 3, 4)
ax_y = fig.add_subplot(2, 3, 5)
ax_z = fig.add_subplot(2, 3, 6)

ani_window_len = ani_window_sec * 1000 / ani_interval
time_axis = np.array([i * ani_interval / 1000 for i in range(int(ani_window_len))])
time_axis -= ani_window_sec

x_data = collections.deque(np.zeros(int(ani_window_len)))
y_data = collections.deque(np.zeros(int(ani_window_len)))
z_data = collections.deque(np.zeros(int(ani_window_len)))

def refresh_plot(i):
    global ani_interval
    global time_axis

    # read and parse data
    # data = serial.readline()
    # data_sensor = data.decode('utf8')
    data_sensor = json.dumps({
        "acceleratorx": 12,
        "acceleratory": 123,
        "acceleratorz": 456,
        "gyrox" : 789,
        "gyroy": 765,
        "gyroz": 987
    })
    i_data = json.loads(data_sensor)
    i_acc_x = i_data["acceleratorx"]
    # i_acc_y = i_data["acceleratory"]
    # i_acc_z = i_data["acceleratorz"]
    i_acc_y = np.random.rand()*100
    i_acc_z = np.random.rand()*100

    time_axis += ani_interval/1000

    x_data.popleft()
    x_data.append(i_acc_x)
    ax_x.cla()
    ax_x.set_xlabel('time')
    ax_x.set_xlim(time_axis[0], time_axis[-1])
    ax_x.set_ylabel('x-axis accelerator')
    # ax_x.set_ylim(-acc_max, acc_max)
    ax_x.plot(time_axis, x_data)

    y_data.popleft()
    y_data.append(i_acc_y)
    ax_y.cla()
    ax_y.set_xlabel('time')
    ax_y.set_xlim(time_axis[0], time_axis[-1])
    ax_y.set_ylabel('y-axis accelerator')
    # ax_y.set_ylim(-acc_max, acc_max)
    ax_y.plot(time_axis, y_data)
    
    z_data.popleft()
    z_data.append(i_acc_z)
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