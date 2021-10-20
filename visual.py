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

acc_max = 10
ani_window_sec = 5.0
ani_interval = 100
box_bound = 100.0
moving_trail = 3




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')
conn, addr = s.accept()
print('connected by ' + str(addr))


# while True:
#     conn, addr = s.accept()
#     print('connected by ' + str(addr))

#     while True:
#         indata = conn.recv(8192)
#         if len(indata) == 0: # connection closed
#             conn.close()
#             print('client closed connection.')
#             break
#         print('recv: ' + indata.decode())



fig = plt.figure()
ax = fig.add_subplot(2, 1, 1, projection='3d')
ax_x = fig.add_subplot(2, 3, 4)
ax_y = fig.add_subplot(2, 3, 5)
ax_z = fig.add_subplot(2, 3, 6)

# create time axis
ani_window_len = ani_window_sec * 1000 / ani_interval
time_axis = np.array([i * ani_interval / 1000 for i in range(int(ani_window_len))])
time_axis -= ani_window_sec

# data buffer
x_data = collections.deque(np.zeros(int(ani_window_len)))
y_data = collections.deque(np.zeros(int(ani_window_len)))
z_data = collections.deque(np.zeros(int(ani_window_len)))


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

# postition buffer
x_position = collections.deque(np.zeros(moving_trail))
y_position = collections.deque(np.zeros(moving_trail))
z_position = collections.deque(np.zeros(moving_trail))


def refresh_plot(i):
    global ani_interval
    global time_axis

    # read and parse data
    indata = conn.recv(8192)
    if len(indata) == 0: # connection closed
        conn.close()
        print('client closed connection.')
        exit()

    i_data = json.loads(indata.decode())
    #print('recv: ' + i_data)
    x_acc = i_data["accellerox"]
    y_acc = i_data["accelleroy"]
    z_acc = i_data["accelleroz"]

    ## emulate i_data
    # data_sensor = json.dumps({
    #     "acceleratorx": 12,
    #     "acceleratory": 123,
    #     "acceleratorz": 456,
    #     "gyrox" : 789,
    #     "gyroy": 765,
    #     "gyroz": 987
    # })
    # i_data = json.loads(data_sensor)
    # x_acc = (np.random.rand()-0.5)*100
    # y_acc = (np.random.rand()-0.5)*100
    # z_acc = (np.random.rand()-0.5)*100
    
    position["x"] += velocity["x"]*dt + x_acc*x_acc*dt/2
    velocity["x"] += x_acc*dt
    position["y"] += velocity["y"]*dt + y_acc*y_acc*dt/2
    velocity["y"] += x_acc*dt
    position["z"] += velocity["z"]*dt + z_acc*z_acc*dt/2
    velocity["z"] += z_acc*dt


    # plot x, y, z acceleration in time axis
    time_axis += ani_interval/1000

    x_data.popleft()
    x_data.append(x_acc)
    ax_x.cla()
    ax_x.set_xlabel('time')
    ax_x.set_xlim(time_axis[0], time_axis[-1])
    ax_x.set_ylabel('x-axis accelerator')
    ax_x.plot(time_axis, x_data)

    y_data.popleft()
    y_data.append(y_acc)
    ax_y.cla()
    ax_y.set_xlabel('time')
    ax_y.set_xlim(time_axis[0], time_axis[-1])
    ax_y.set_ylabel('y-axis accelerator')
    ax_y.plot(time_axis, y_data)
    
    z_data.popleft()
    z_data.append(z_acc)
    ax_z.cla()
    ax_z.set_xlabel('time')
    ax_z.set_xlim(time_axis[0], time_axis[-1])
    ax_z.set_ylabel('z-axis accelerator')
    ax_z.plot(time_axis, z_data)


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





