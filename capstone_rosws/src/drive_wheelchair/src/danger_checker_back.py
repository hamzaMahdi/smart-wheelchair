#Libraries
import RPi.GPIO as GPIO
import time
import rospy
from std_msgs.msg import Bool
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
 
#set GPIO Pins
GPIO_TRIGGER = [7,11,12]
GPIO_ECHO = [13,15,16]
 
#set GPIO direction (IN / OUT)
for i in range(3):
    GPIO.setup(GPIO_TRIGGER[i], GPIO.OUT)
    GPIO.setup(GPIO_ECHO[i], GPIO.IN)
 
def distance(ultrasonic_index):
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER[ultrasonic_index], True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER[ultrasonic_index], False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO[ultrasonic_index]) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO[ultrasonic_index]) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        pub = rospy.Publisher('back_danger_flag', Bool, queue_size=1)
        rospy.init_node('ultrsonic_danger_checker', anonymous=True)
        rate = rospy.Rate(10) # 10hz
        while True:
            flag = Bool()
            flag = False
            dist[0] = distance(0)
            dist[1] = distance(1)
            dist[2] = distance(2)
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
            for i in range(3):
                if(dist[i]>30):
                    flag = True
            pub.publish(flag)
            rospy.loginfo(flag)
            flag = False
            rate.sleep()
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()