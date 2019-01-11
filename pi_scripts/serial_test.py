import serial
ser = serial.Serial('/dev/cu.usbmodem14201', 115200)
while 1: 
    if(ser.in_waiting >0):
        line = ser.readline()
        line = line.decode('utf8')
        line = line.split(',')
        for c in line:
        	if c.strip():
        		print(int(float(c)))

