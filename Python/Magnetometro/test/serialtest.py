import serial
serial = serial.Serial('/dev/ttyACM0', 115200, timeout=2) 
while True:
   data = serial.readline()
   print data
   try: 
      x, y, z, d = data.split(';')
      print (x, y, z, d)
   except: 
      print ("incomplete data")
   
   
   

 

