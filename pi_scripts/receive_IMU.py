import bluetooth
import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI
import time                            #calling time to provide delays in program
import numpy
bd_addr = "98:D3:21:FC:88:AB" 
port = 1
sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
sock.connect((bd_addr,port))
IO.setwarnings(False)           #do not show any warnings

IO.setmode (IO.BOARD)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)

IO.setup(35,IO.OUT)           
IO.setup(32,IO.OUT)
p = IO.PWM(35,100)          
q = IO.PWM(32,100)
p.start(75)                              
q.start(75)
data = ""
while 1:
	try:
		data = (sock.recv(100024)).decode("utf-8") 
		#data += (sock.recv(1024)).decode("utf-8")
		data_end = data.find("\n")
		if data_end != -1:
			data = data.split(',')
			for c in line:
				c.strip()
				if(i==0):
					x = float(c) 
				else:
					y = float(c)
				i= i+1
			print (data)
#			data = ""
		if(abs(x)>abs(y)) : 
			x = numpy.interp(x,[-90,90],[50,100]) #rescale ACCEL to MOTOR values
			p.ChangeDutyCycle(x)
			q.ChangeDutyCycle(x)

		else:
			if(y<0):
				y1 = numpy.interp(y,[-90,90],[50,100]) #rescale ACCEL to MOTOR values
				y2 = numpy.interp(y,[-90,90],[100,50]) #rescale ACCEL to MOTOR values
			else:
				y1 = numpy.interp(y,[-90,90],[100,50]) #rescale ACCEL to MOTOR values
				y2 = numpy.interp(y,[-90,90],[50,100]) #rescale ACCEL to MOTOR values
			p.ChangeDutyCycle(y1)
			q.ChangeDutyCycle(y2)
	except KeyboardInterrupt:
		break
sock.close()
