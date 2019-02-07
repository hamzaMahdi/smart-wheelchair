#!/usr/bin/env python
import rospy
import RPi.GPIO as IO
import time                            #calling time to provide delays in program
from std_msgs.msg import Float32MultiArray
IO.setwarnings(False)           #do not show any warnings

IO.setmode (IO.BOARD)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)

IO.setup(35,IO.OUT)           
IO.setup(32,IO.OUT)
p = IO.PWM(35,500)          
q = IO.PWM(32,500)
p.start(75)                              
q.start(75)

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    p.ChangeDutyCycle(data.data[0])
    q.ChangeDutyCycle(data.data[1])

    
def listener():

    rospy.init_node('drive', anonymous=True)

    rospy.Subscriber("motors", Float32MultiArray, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()