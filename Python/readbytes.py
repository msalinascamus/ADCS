import serial
serial = serial.Serial('/dev/ttyACM0', 115200, timeout=2) 
while True:
   data = serial.read(1)
   if data == "a":
   	print "start frame"
   elif data == "b":
   	print "end frame"
   else:
   	print ord(data)
   
   