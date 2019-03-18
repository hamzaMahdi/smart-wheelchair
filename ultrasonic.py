#!/usr/bin/python
#Libraries
import RPi.GPIO as GPIO  #allow us to control and interact with GPIO pins, without it we cant talk with distance sensor from RP
import time   #allow us to control time, working and sleeping time 
 
#GPIO Mode (BOARD / BCM)   #set GPIO mode to GPIO.BOARD, this means we are using the physcial pin numbers and not the BCM numbers.
      GPIO.setmode(GPIO.BOARD)
 
      PIN_TRIGGER = 7 #physical pins that we have the trigger and echo wired to
      PIN_ECHO = 11   

      GPIO.setup(PIN_TRIGGER, GPIO.OUT) #Next we setup both our pins to either expect an output or an input. Our trigger pin is obviously an output pin as we need to ping this pin to start the sensor
      GPIO.setup(PIN_ECHO, GPIO.IN)	#Echo pin is where we expect our data from, so we set this to receive input.

      GPIO.output(PIN_TRIGGER, GPIO.LOW) #set our PIN_TRIGGER GPIO Pin, so it doesn’t send out anything by setting it to “Low”. more consistent readings. 
      
      print "Waiting for sensor to settle"

      time.sleep(2) #ensure we give distance sensor enough time to settle 

      print "Calculating distance"

      GPIO.output(PIN_TRIGGER, GPIO.HIGH) # HC-SR04 distance sensor to trigger that why we set this pin to high

      time.sleep(0.00001)  #we need it to sleep for a nano second  that distance sensor requires a pulse of nano second 

      GPIO.output(PIN_TRIGGER, GPIO.LOW) #immediately after sleep. we set PIN_TRIGGER to low 
					 
      while GPIO.input(PIN_ECHO)==0:    #while loop to check if pin_echo is low (0) then set pulse start time to current time till it goes to high
            pulse_start_time = time.time()
      while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time() #once pin echo read high, we set end time to current time, to bring pin echo back tp low 

      pulse_duration = pulse_end_time - pulse_start_time
      distance = round(pulse_duration * 17150, 2)
      print "Distance:",distance,"cm"

finally:
      GPIO.cleanup()