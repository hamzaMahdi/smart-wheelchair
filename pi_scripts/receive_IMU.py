import bluetooth

bd_addr = "98:D3:21:FC:88:AB" 
port = 1
sock = bluetooth.BluetoothSocket (bluetooth.RFCOMM)
sock.connect((bd_addr,port))
  
data = ""
while 1:
	try:
		data += (sock.recv(100024)).decode("utf-8") 
		#data += (sock.recv(1024)).decode("utf-8")
		data_end = data.find("\n")
		if data_end != -1:
			print (data)
			data = ""
	except KeyboardInterrupt:
		break
sock.close()
