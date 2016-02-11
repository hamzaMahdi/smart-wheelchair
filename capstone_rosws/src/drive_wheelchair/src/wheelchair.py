#!/usr/bin/env python
import bluetooth
import RPi.GPIO as IO
import time                            #calling time to provide delays in program
import numpy
import rospy
from std_msgs.msg import Float32MultiArray
bd_addr = "98:D3:91:FD:3C:D5" 
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
		data = ""
		x = 75
		y = 76
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
					elif i==1:
						y = float(c)
					i= i+1
					#print (float(c))
				data = ""
			if(abs(x)>90):
				x = x/x*90
			if(abs(y)>90):
				y = y/y*90
			deadzone  = 10
			max_angle = 60
			if(abs(x)<deadzone):
				x = 0
			if(abs(y)<deadzone):
				y = 0
			if(abs(x)>abs(y)) : 
				x1 = numpy.interp(x+y,[-max_angle,max_angle],[60,90]) #rescale ACCEL to MOTOR values
				x2 = numpy.interp(x-y,[-max_angle,max_angle],[60,90]) #rescale ACCEL to MOTOR values
				#y1 = numpy.interp(y,[-max_angle,max_angle],[70,80]) #rescale ACCEL to MOTOR values
                                #y2 = numpy.interp(y,[-max_angle,max_angle],[80,70]) #rescale ACCEL to MOTOR values
				hello_float.data = [x1,x2]
			else:
				y1 = numpy.interp(y,[-max_angle,max_angle],[60,90]) #rescale ACCEL to MOTOR values
				y2 = numpy.interp(y,[-max_angle,max_angle],[90,60]) #rescale ACCEL to MOTOR values
				hello_float.data = [y1,y2]
			#hello_float.data = []
			#hello_float.data=([x,y])
			pub.publish(hello_float)
			rospy.loginfo(hello_float)
			rate.sleep()

try:
    sender()
    while 1:
    	time.sleep(5)

except rospy.ROSInterruptException:
    pass
sock.close()
#fix socket closure
