#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
import numpy
pub = rospy.Publisher("danger_flag",Bool,queue_size=1)

def multi_range(l, *args):
	output = []
	for indices in args:
		output += l[indices[0]:indices[1]]
		return output
def check_obstacles(data):
	flag = Bool()
	flag = False
	front = [data.ranges[i] for i in range(0,90)]
	front +=[data.ranges[i] for i in range(650,720)]
	#print front
	window =  50
	for i in range(len(front)/window):
		avg = numpy.mean(front[i*window:(i+1)*window])
		if (avg>1):
			flag = True
			break
		else :
			flage  = False
	pub.publish(flag)
rospy.init_node('danger_checker', anonymous=True)
rospy.Subscriber("/scan", LaserScan, check_obstacles,queue_size=1)
rospy.spin()