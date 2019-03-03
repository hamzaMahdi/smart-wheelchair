#!/usr/bin/env python
import bluetooth
import RPi.GPIO as IO
import time                            #calling time to provide delays in program
import numpy
import rospy
import serial
from std_msgs.msg import Float32MultiArray
ser = serial.Serial('/dev/ttyUSB0',115200)
bd_addr = "98:D3:21:FC:88:AB" 
port = 1
#sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
#$sock.connect((bd_addr,port))

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
		speed = 0
		hello_float = Float32MultiArray()
		hello_float.data = []
		while not rospy.is_shutdown():
			i = 0
			'''data += (sock.recv(100024)).decode("utf-8") 
			#data += (sock.recv(1024)).decode("utf-8")
			data_end = data.find("\n")
			if data_end != -1:'''
			if(ser.in_waiting>0):
				line = ser.readLine()
				data = line.decode('utf8')
				data = data.split(',')
				print(data)
				for c in data:
					c.strip()
					if(i==0):
						x = float(c) 
					elif(i==1):
						y = float(c)
					else:
						z= float(c)	#Data for the yaw (reset/close)
					i= i+1
					print (float(c))
				data = ""
			if(abs(x)>90):
				x = x/x*90
			if(abs(y)>90):
				y = y/y*90


			if(z>700):
				break	#Shut Down algorithm
			elif(z<-700):	#Positive Yaw
				x = 75
				y = 76

			elif(abs(x)>abs(y) and abs(x)>30) :	#Implement a specific range 30 to 90 
				x = numpy.interp(x,[-90,90],[50,99]) #rescale ACCEL to MOTOR values
				hello_float.data = [x,x]
			elif(abs(y)>abs(x) and abs(y)>30): #Implement a specific range 30 to 90
				y1 = numpy.interp(y,[-90,90],[50,99]) #rescale ACCEL to MOTOR values
				y2 = numpy.interp(y,[-90,90],[99,50]) #rescale ACCEL to MOTOR values
				hello_float.data = [y1,y2]
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
