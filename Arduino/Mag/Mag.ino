#include <MPU9250_asukiaaa.h>

#ifdef _ESP32_HAL_I2C_H_
#define SDA_PIN 26
#define SCL_PIN 25
#endif

MPU9250 mySensor;

uint8_t sensorId;
float mDirection, mX, mY, mZ;

void setup() {
  Serial.begin(115200);

#ifdef _ESP32_HAL_I2C_H_
  Wire.begin(SDA_PIN, SCL_PIN)
#else
  Wire.begin();
#endif

  mySensor.setWire(&Wire);
  mySensor.beginMag();
  mySensor.beginAccel();
  mySensor.beginGyro();
  sensorId = mySensor.readId();

}

void loop() {
  mySensor.magUpdate();
  mX = mySensor.magX();
  mY = mySensor.magY();
  mZ = mySensor.magZ();
  mDirection = mySensor.magHorizDirection();
  Serial.println(String(mX) + ";"+ String(mY) + ";" +  String(mZ) + ";" + String(mDirection));
  delay(100);
}  

