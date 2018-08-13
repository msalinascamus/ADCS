#include <SoftwareSerial.h>

SoftwareSerial BT(9,8); // Define RX && TX pin on Arduino conected to a serial debuger

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  BT.begin(115200);
}

void loop()
{
  if(BT.available())    // Si llega un dato por el puerto BT se envía al monitor serial
  {
    Serial.write(BT.read());
  }
  if(Serial.available())  // Si llega un dato por el monitor serial se envía al puerto BT
  {
     BT.write(Serial.read());
  }
}
