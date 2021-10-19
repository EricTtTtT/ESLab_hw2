import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import collections
import psutil

def my_function(i):
    data = serial.readline()
    data_sensor = data.decode('utf8')
    if(data_sensor[:10] == "ACCELERO_X" or 
        data_sensor[:10] == "ACCELERO_Y" or 
        data_sensor[:10] == "ACCELERO_Z"):
        print("fuck") 
    # get data
    accelleroX.popleft()
    accelleroX.append(psutil.cpu_percent())
    accelleroY.popleft()
    accelleroY.append(psutil.virtual_memory().percent)
    accelleroZ.popleft()
    accelleroZ.append(500)
    # clear axis
    ax.cla()
    ax1.cla()
    #ax2.cla()
    # plot accelleroX
    ax.plot(accelleroX)
    ax.scatter(len(accelleroX)-1, accelleroX[-1])
    ax.text(len(accelleroX)-1, accelleroX[-1]+2, "{}".format(accelleroX[-1]))
    ax.set_ylim(-1000,1000)
    # plot accelleroY
    ax1.plot(accelleroY)
    ax1.scatter(len(accelleroY)-1, accelleroY[-1])
    ax1.text(len(accelleroY)-1, accelleroY[-1]+2, "{}".format(accelleroY[-1]))
    ax1.set_ylim(-1000,1000)
"""     # plot accelleroZ
    #ax2.plot(accelleroZ)
    ax2.scatter(len(accelleroZ)-1, accelleroZ[-1])
    ax2.text(len(accelleroZ)-1, accelleroZ[-1]+2, "{}".format(accelleroZ[-1]))
    ax2.set_ylim(-1000,1000) """


accelleroX = collections.deque(np.zeros(10))
accelleroY = collections.deque(np.zeros(10))
accelleroZ = collections.deque(np.zeros(10))

fig = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
ax = plt.subplot(121)
ax1 = plt.subplot(122)
#ax2 = plt.subplot(131)
ax.set_facecolor('#DEDEDE')
ax1.set_facecolor('#DEDEDE')
#ax2.set_facecolor('#DEDEDE')

# animate


#連線串列埠
serial = serial.Serial('COM3',9600,timeout=2)  #連線COM13,波特率位115200
if serial.isOpen():
    print('串列埠已開啟')
    while True:
        ani = FuncAnimation(fig, my_function, interval=1000)
        plt.show()
else:
	print('串列埠未開啟')



#關閉串列埠
serial.close()

if serial.isOpen():
	print('串列埠未關閉')
else:
	print('串列埠已關閉')