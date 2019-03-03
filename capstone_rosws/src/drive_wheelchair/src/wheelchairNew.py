#!/usr/bin/env python
import bluetooth
import RPi.GPIO as IO
import time                            #calling time to provide delays in program
import numpy
import rospy
import serial
from std_msgs.msg import Float32MultiArray
ser = serial.Serial('/dev/ttyACM0',115200)
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
				speed = 0
			if(abs(y)>90):
				y = y/y*90
				speed = 0


			if(z>700):
				break	#Shut Down algorithm
			elif(z<-700):	#Positive Yaw
				cycle = speed/100
				while speed != 0:
					speed = speed - cycle
				speed= 0 #Restart speed after 

			elif(abs(x)>abs(y) and abs(x)>30 and abs(x)>abs(speed)) :	#Implement a specific range 30 to 90 
				speed = x	#Take the highest speed until 90
				if (x>0) :
					x = numpy.interp(x,[30,90],[75,100]) #rescale ACCEL to MOTOR values

				else:
					x = numpy.interp(x,[-90,-30],[75,50]) #rescale ACCEL to MOTOR values
				
				hello_float.data = [x,x]
			elif(abs(y)>abs(x) and abs(y)>30 and abs(y)>abs(speed)): #Implement a specific range 30 to 90
				speed = y #Take the highest speed until 90
				if (y>0):
					y1 = numpy.interp(y,[30,90],[75,100]) #rescale ACCEL to MOTOR values
					y2 = numpy.interp(y,[30,90],[75,50]) #rescale ACCEL to MOTOR values
				else:
					y1 = numpy.interp(y,[-90,-30],[75,50]) #rescale ACCEL to MOTOR values
					y2 = numpy.interp(y,[-90,-30],[75,100]) #rescale ACCEL to MOTOR values
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
