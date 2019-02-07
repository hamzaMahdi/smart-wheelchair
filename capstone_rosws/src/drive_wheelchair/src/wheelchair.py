#!/usr/bin/env python
import bluetooth
import RPi.GPIO as IO
import time                            #calling time to provide delays in program
import numpy
import rospy
from std_msgs.msg import Float32MultiArray
bd_addr = "98:D3:21:FC:88:AB" 
port = 1
sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
sock.connect((bd_addr,port))
data = ""
x = 75
y = 76
def sender():
		pub = rospy.Publisher('motors', Float32MultiArray, queue_size=1)
		rospy.init_node('controller', anonymous=True)
		rate = rospy.Rate(10) # 10hz

		hello_float = Float32MultiArray()
		hello_float.data = []
		while not rospy.is_shutdown():
			i = 0
			data += (sock.recv(100024)).decode("utf-8") 
			#data += (sock.recv(1024)).decode("utf-8")
			data_end = data.find("\n")
			if data_end != -1:
				data = data.split(',')
				print(data)
				for c in data:
					c.strip()
					if(i==0):
						x = float(c) 
					else:
						y = float(c)
					i= i+1
					print (float(c))
				data = ""
			if(abs(x)>90):
				x = x/x*90
			if(abs(y)>90):
				y = y/y*90
			if(abs(x)>abs(y)) : 
				x = numpy.interp(x,[-90,90],[50,100]) #rescale ACCEL to MOTOR values
			else:
				y1 = numpy.interp(y,[-90,90],[50,100]) #rescale ACCEL to MOTOR values
				y2 = numpy.interp(y,[-90,90],[100,50]) #rescale ACCEL to MOTOR values
			hello_float.data = []
			hello_float.data.insert([x,y])
			pub.publish(hello_float)
			rate.sleep()

try:
    sender()
    while 1:
    	time.sleep(5)

except rospy.ROSInterruptException:
    pass
sock.close()
#fix socket closure