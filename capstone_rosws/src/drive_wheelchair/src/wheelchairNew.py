#!/usr/bin/env python
import bluetooth
#import RPi.GPIO as IO
import time                            #calling time to provide delays in program
import numpy
import rospy
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Vector3Stamped
from tf.transformations import euler_from_quaternion
from sensor_msgs.msg import Imu
bd_addr = "98:D3:91:FD:3C:D5" 
port = 1
sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
sock.connect((bd_addr,port))
data = ""
x = 75
y = 76
heading = 0
diff = 0
DECLINATION = -10

def sender():
		'''
		def callback(mag):
			global heading
  			if (mag.vector.y == 0):
				if mag.vector.x < 0:
					heading = numpy.pi
				else:
					heading = 0
				#heading = (mag.vector.x < 0) ? pi : 0
  			else:
    				heading = numpy.arctan2(mag.vector.x, mag.vector.y)

  			heading -= DECLINATION * numpy.pi / 180

  			if (heading > numpy.pi):
				 heading -= (2 * numpy.pi)
  			elif (heading < -numpy.pi):
				 heading += (2 * numpy.pi)

  			# Convert everything from radians to degrees:
  			heading *= 180.0 / numpy.pi
			#list = [mag.orientation.x,mag.orientation.y,mag.orientation.z,mag.orientation.w]
			#(row,pitch,yaw) = euler_from_quaternion(list)
			rospy.loginfo("%f,%f",heading,z)
		'''
		pub = rospy.Publisher('motors', Float32MultiArray, queue_size=1)
		rospy.init_node('controller', anonymous=True)
		#rospy.Subscriber("imu/mag", Vector3Stamped, callback)
		rate = rospy.Rate(10) # 10hz
		data = ""
		x = 75
		y = 76
		z = 0
		ref1 = 0
		ref2 = 0
		ref = 0
		count = 0
		diff1 = 0
		diff2 = 0
		diff = 0
		heading = -100
		test = 0
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
					elif i==2:
						z = float(c)
					i= i+1
					#print (float(c))
				data = ""
			#rospy.Subscriber("imu/mag", Vector3Stamped, callback)
			if (count<15):
				if((heading>=0 and z>=0) or (heading<=0 and z<=0)):
					ref = abs(abs(heading) - abs(z))
				else:
					alt1 = 180 - abs(z)
					alt2 = 180 - abs(heading)
					ref = min(abs(z)+abs(heading),alt1+alt2)
				sign = abs(heading) >abs(z)
				ref1 = heading
				ref2 = z
				#test = z
				count += 1
			else:
				if(numpy.sign(heading) == numpy.sign(ref1)):
					 diff1 = abs(ref1 - heading)
				else:
					alt1 = 180 - abs(heading)
					alt2 = 180 - abs(ref1)
					diff1 =min(abs(ref1)+abs(heading),alt1+alt2)
				if(numpy.sign(z) == numpy.sign(ref2)):
                                        diff2 = abs(ref2 - z)
                                else:
                                        alt1 = 180 - abs(z)
                                        alt2 = 180 - abs(ref2)
                                        diff2 =min(abs(ref2)+abs(z),alt1+alt2) 
				diff = diff2 - diff1
				#if((heading>=0 and z>=0) or (heading<=0 and z<=0)):
					#if (sign == (abs(heading) >abs(z))):
					#diff =abs(ref- abs(abs(heading) - abs(z)))
					#else:
					#	diff = ref + abs(abs(heading) - abs(z))
		                #else:
                			#alt1 = 180 - abs(z)
                    			#alt2 = 180 - abs(heading)
					#if (sign == (abs(heading)>abs(z))):
                    			#diff =abs(ref -  min(abs(z)+abs(heading),alt1+alt2))
					#else:
					#	diff =abs(ref -  max(abs(z)+abs(heading),alt1+alt2))
                        		#diff1 = abs(ref1 - heading)
				#diff2 = abs(ref2 - z)
				#diff = diff2 - diff1
			print(z)
			print(heading)
			print(diff)
            		if(abs(x)>90):
            			x = x/x*90
            		if(abs(y)>90):
				y = y/y*90
			if (diff>50):
				x = 0
				y = 0
				print("STOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOP")
			elif(abs(x)>abs(y)) : 
				x = numpy.interp(x,[-90,90],[50,100]) #rescale ACCEL to MOTOR values
				if(z >400):
                                	#x = 74
					print()
				hello_float.data = [x,x]
			else:
				y1 = numpy.interp(y,[-90,90],[50,100]) #rescale ACCEL to MOTOR values
				y2 = numpy.interp(y,[-90,90],[100,50]) #rescale ACCEL to MOTOR values
				if(z >400):
					print()
                               		#y1 = 74
                                	#y2 = 74
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
