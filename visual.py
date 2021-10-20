import collections
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import socket
import time


# config
HOST = '192.168.41.105'
PORT = 7414

ani_window_sec = 5.0
ani_interval = 200
acceleration_max = 400
box_bound = 20000.0
moving_trail = 5

fake_data = False


if not fake_data:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)

    print('server start at: %s:%s' % (HOST, PORT))
    print('wait for connection...')
    conn, addr = s.accept()
    print('connected by ' + str(addr))


fig = plt.figure()
ax = fig.add_subplot(2, 2, 1, projection='3d')
ax_x = fig.add_subplot(4, 4, 13)
ax_y = fig.add_subplot(4, 4, 14)
ax_z = fig.add_subplot(4, 4, 15)
ax_gyro_x = fig.add_subplot(4, 4, 4)
ax_gyro_y = fig.add_subplot(4, 4, 8)
ax_gyro_z = fig.add_subplot(4, 4, 12)

# create time axis
ani_window_len = ani_window_sec * 1000 / ani_interval
time_axis = np.array([i * ani_interval / 1000 for i in range(int(ani_window_len))])
time_axis -= ani_window_sec

# data buffer
x_data = collections.deque(np.zeros(int(ani_window_len)))
y_data = collections.deque(np.zeros(int(ani_window_len)))
z_data = collections.deque(np.zeros(int(ani_window_len)))
x_data_gyro = collections.deque(np.zeros(int(ani_window_len)))
y_data_gyro = collections.deque(np.zeros(int(ani_window_len)))
z_data_gyro = collections.deque(np.zeros(int(ani_window_len)))


# plot 3d moving
ax.set_xlim3d([-box_bound, box_bound])
ax.set_xlabel('X')
ax.set_ylim3d([-box_bound, box_bound])
ax.set_ylabel('Y')
ax.set_zlim3d([-box_bound, box_bound])
ax.set_zlabel('Z')
velocity = {
    "x": 0.0,
    "y": 0.0,
    "z": 0.0
}
position = {
    "x": 0.0,
    "y": 0.0,
    "z": 0.0
}
dt = ani_interval / 1000
dtdt_2 = dt*dt/2

# postition buffer
x_position = collections.deque(np.zeros(moving_trail))
y_position = collections.deque(np.zeros(moving_trail))
z_position = collections.deque(np.zeros(moving_trail))


def refresh_plot(i):
    global ani_interval
    global time_axis


    # read and parse data
    if not fake_data:
        indata = conn.recv(1<<13)
        if len(indata) == 0: # connection closed
            conn.close()
            print('client closed connection.')
            exit()
        i_data = json.loads(indata.decode())
        x_acc = i_data["accelerox"]
        y_acc = i_data["acceleroy"]
        z_acc = i_data["acceleroz"]
        x_gyro = i_data["gyrox"]
        y_gyro = i_data["gyroy"]
        z_gyro = i_data["gyroz"]
    else:
        # emulate i_data
        x_acc = (np.random.rand()-0.5)*1000
        y_acc = (np.random.rand()-0.5)*1000
        z_acc = (np.random.rand()-0.5)*1000
        x_gyro = (np.random.rand()-0.5)*1000
        y_gyro = (np.random.rand()-0.5)*1000
        z_gyro = (np.random.rand()-0.5)*1000
    
    position["x"] += velocity["x"]*dt + x_acc*dtdt_2
    velocity["x"] += x_acc*dt
    position["y"] += velocity["y"]*dt + y_acc*dtdt_2
    velocity["y"] += y_acc*dt
    position["z"] += velocity["z"]*dt + z_acc*dtdt_2
    velocity["z"] += z_acc*dt


    # plot x, y, z acceleration in time axis
    time_axis += ani_interval/1000

    x_data.popleft()
    x_data.append(x_acc)
    ax_x.cla()
    ax_x.set_xlabel('time')
    ax_x.set_xlim(time_axis[0], time_axis[-1])
    ax_x.set_ylabel('x-axis acceleration')
    ax_x.set_ylim(-acceleration_max, acceleration_max)
    ax_x.plot(time_axis, x_data)

    y_data.popleft()
    y_data.append(y_acc)
    ax_y.cla()
    ax_y.set_xlabel('time')
    ax_y.set_xlim(time_axis[0], time_axis[-1])
    ax_y.set_ylabel('y-axis acceleration')
    ax_y.set_ylim(-acceleration_max, acceleration_max)
    ax_y.plot(time_axis, y_data)
    
    z_data.popleft()
    z_data.append(z_acc)
    ax_z.cla()
    ax_z.set_xlabel('time')
    ax_z.set_xlim(time_axis[0], time_axis[-1])
    ax_z.set_ylabel('z-axis acceleration')
    ax_z.set_ylim(-acceleration_max, acceleration_max)
    ax_z.plot(time_axis, z_data)

    x_data_gyro.popleft()
    x_data_gyro.append(x_gyro)
    ax_gyro_x.cla()
    ax_gyro_x.set_xlabel('time')
    ax_gyro_x.set_xlim(time_axis[0], time_axis[-1])
    ax_gyro_x.set_ylabel('x-axis gyro')
    ax_gyro_x.plot(time_axis, x_data_gyro)

    y_data_gyro.popleft()
    y_data_gyro.append(y_gyro)
    ax_gyro_y.cla()
    ax_gyro_y.set_xlabel('time')
    ax_gyro_y.set_xlim(time_axis[0], time_axis[-1])
    ax_gyro_y.set_ylabel('y-axis gyro')
    ax_gyro_y.plot(time_axis, y_data_gyro)

    z_data_gyro.popleft()
    z_data_gyro.append(z_gyro)
    ax_gyro_z.cla()
    ax_gyro_z.set_xlabel('time')
    ax_gyro_z.set_xlim(time_axis[0], time_axis[-1])
    ax_gyro_z.set_ylabel('z-axis gyro')
    ax_gyro_z.plot(time_axis, z_data_gyro)


    # plot 3d position
    x_position.popleft()
    x_position.append(position["x"])
    y_position.popleft()
    y_position.append(position["y"])
    z_position.popleft()
    z_position.append(position["z"])
    ax.cla()
    ax.set_xlim3d([-box_bound, box_bound])
    ax.set_xlabel('X')
    ax.set_ylim3d([-box_bound, box_bound])
    ax.set_ylabel('Y')
    ax.set_zlim3d([-box_bound, box_bound])
    ax.set_zlabel('Z')
    for j in range(moving_trail-1):
        ax.plot3D(
            [x_position[j], x_position[j+1]],
            [y_position[j], y_position[j+1]],
            [z_position[j], z_position[j+1]]
        , 'ro')


ani = FuncAnimation(fig, refresh_plot, interval=ani_interval)
plt.show()





