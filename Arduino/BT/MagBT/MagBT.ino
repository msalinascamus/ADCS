#include <MPU9250_asukiaaa.h>
#include <SoftwareSerial.h>

#ifdef _ESP32_HAL_I2C_H_
#define SDA_PIN 26
#define SCL_PIN 25
#endif

MPU9250 mySensor;

uint8_t sensorId;
float mDirection, mX, mY, mZ;

SoftwareSerial BT(9,8); // Define RX && TX pin on Arduino conected to a serial debuger

typedef struct{
    float mx;
    float my;
    float mz;
    uint8_t checksum;
}Datos;


Datos datos;

void setup()
{
    Serial.begin(115200);
    BT.begin(115200);
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

void loop()
{
    mySensor.magUpdate();
    mX = mySensor.magX();
    mY = mySensor.magY();
    mZ = mySensor.magZ();
    datos.mx=mX;
    datos.my = mY;
    datos.mz = mZ;
    //datos.mx=80.5;
    //datos.my = 100.53;
    //datos.mz = -40.222;
    datos.checksum = checksum((uint8_t*)&datos, sizeof(datos));
    BT.write((uint8_t*)&datos, sizeof(datos));
    Serial.println(String(mX) + ";"+ String(mY) + ";" +  String(mZ));
    //Serial.print("a");// Serial.println(sizeof(datos));
    //Serial.write((uint8_t*)&datos, sizeof(datos));
    //Serial.print("b");
    delay(100);
}

uint8_t checksum(uint8_t *packet, uint8_t n)
{
    uint32_t sum = 0;
    for (int j=0;j<n-1;j++) sum += packet[j];
    return sum & 0x00FF;
}