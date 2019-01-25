import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI
import time                            #calling time to provide delays in program
import serial
ser = serial.Serial('/dev/ttyACM0', 115200)
IO.setwarnings(False)           #do not show any warnings

IO.setmode (IO.BOARD)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)

IO.setup(35,IO.OUT)           # initialize GPIO19 as an output.
IO.setup(40,IO.OUT)
IO.setup(32,IO.OUT)
IO.setup(38,IO.OUT)
IO.output(40,0)
p = IO.PWM(35,100)          #GPIO19 as PWM output, with 100Hz frequency
q = IO.PWM(32,100)
p.start(0)                              #generate PWM signal with 0% duty cycle
q.start(0)
dirL = 1
dirR = 1
x=0
y=0

mag = 0
while 1:                               #execute loop forever
  i = 0
  if(ser.in_waiting>0):
    line = ser.readline()
    line = line.decode('utf8')
    line = line.split(',')
    for c in line:
      c.strip()
      if(i==0):
        x = float(c) 
        
      else:
        y = float(c)
      i= i+1
    if(abs(x)>abs(y)) : 
      mag = abs(x)
      if(x<0):
          dirL = 1
          dirR = 1
      else:
          dirL = 0
          dirR = 0
    else:
      mag = abs(y)
      if(y<0):
          dirL = 0
          dirR = 1
      else:
          dirL = 1
          dirR = 0
  IO.output(38,dirL)
  IO.output(40,dirR)
  p.ChangeDutyCycle(mag)
  q.ChangeDutyCycle(mag)
  print(x)
  print(y)
  print('----------')
  time.sleep(0.2)
   # for x in range (100):                          #execute loop for 50 times, x being incremented from 0 to 49.
       # p.ChangeDutyCycle(x)               #change duty cycle for varying the brightness of LED.
       # time.sleep(0.1)                           #sleep for 100m second
      
    #for x in range (100):                         #execute loop for 50 times, x being incremented from 0 to 49.
       # p.ChangeDutyCycle(100-x)        #change duty cycle for changing the brightness of LED.
       # time.sleep(0.1)                          #sleep for 100m second