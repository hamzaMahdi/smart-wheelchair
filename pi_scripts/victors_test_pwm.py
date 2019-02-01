import RPi.GPIO as GPIO
import time as time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(35, GPIO.OUT)

servo = GPIO.PWM(35,500)
servo.start(0)
while (1):
	for dc in range(50,101,5):
		servo.ChangeDutyCycle(dc)
		time.sleep(0.5)
	for dc in range(100,45,-5):
		servo.ChangeDutyCycle(dc)
		time.sleep(0.5)
servo.stop()
GPIO.cleanup();
