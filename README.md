# ESlab_hw2

## Overview

The purpose of this exercise is to send the value read by the accelerometer and  
gyroscope of B-L475E-IOT01A2 to a Python socket server hosted on Windows10.

## Usage

    python visual.py
1.  Start the server, modify the host name and port number if needed.
2.  build the image using main.cpp in the repository, modify the configuration  
    in mbed_app.json and the port number in main.cpp if needed, then the preparation is      done.
    
## Implementation

1.  Move the subfolder of the example project of “DISCO_L475VG_IOT01-Sensors-BSP”  
    under “mbed-os-example-sockets”.
2.  Modify the default port number to the port number opened on our server  
    ![Imgur](https://i.imgur.com/c1L941o.png)
3.  Modify the host name of the “mbed_app.json”  
    ![Imgur](https://i.imgur.com/TikVwRA.png)
4.  Merge some of the code in the main.cpp of the sensor example into  
    the main.cpp of the sockets. including the sensor initialization part   
    and sensor value reading part
5.  In the method run() of the class SocketDemo, We removed the part of sending  
    HTTP request and receiving HTTP response, then We added a while(1) loop to  
    implement sensor reading and sending data to the socket server.
6.  For data visualization, we use matplotlib to visualize acceleration in three 
    dimensions.   
    In addition, we provide a three dimensional model to display the relative position  
    of the board. Moreover, we display the three dimensions of the gyro with three charts.


