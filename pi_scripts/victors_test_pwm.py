import RPi.GPIO as GPIO
import time as time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

servo = GPIO.PWM(18,500)
servo.start(0)
try:
     while True:
          for dc in range(50,101,5):
               servo.ChangeDutyCycle(dc)
               time.sleep(0.5)
          for dc in range(100,45,-5):
               servo.ChangeDutyCycle(dc)
               time.sleep(0.5)
except KeyboardInterrupt:
     pass
servo.stop()
GPIO.cleanup();