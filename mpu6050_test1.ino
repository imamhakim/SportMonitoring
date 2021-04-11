#include <Wire.h>
#include <math.h>

float AccX, AccY, AccZ;
float GyroX, GyroY, GyroZ;
float theta_acc;

int MPU_register = 0x68; //alamat register dari MPU6050
void setup() {
  Serial.begin(115200); //Baud rate transfer data
  Wire.begin();
  Wire.beginTransmission(MPU_register); //start acces MPU6050
  Wire.write(0x6B); //konfigurasi MPU6050 mode
  Wire.write(0x00); //normalize konfigurasi MPU6050 to reset value
  Wire.endTransmission(true); // stop acces MPU6050

  Wire.beginTransmission(MPU_register); //start acces MPU6050
  Wire.write(0x1B); //acces register gyro config to configurationn scale range gyro
  Wire.write(0x10); //set the scale range gyro to 1000 degree/s 
  Wire.endTransmission(true); //stop acces MPU6050

  Wire.beginTransmission(MPU_register); //start acces MPU6050
  Wire.write(0x1C); //acces register accelerometer config to configuration scale range accelerometer
  Wire.write(0x10); //set the scale range accelerometer to 8G
  Wire.endTransmission(true);//stop acces MPU6050
  delay(10);
}

void loop() {
  Wire.beginTransmission(MPU_register); //start acces MPU6050
  Wire.write(0x3B); // start acces measurement of accelerometer
  Wire.endTransmission(false); 
  Wire.requestFrom(MPU_register,6,true); // from MPU6050 take 6 data 
  AccX = (Wire.read() << 8 | Wire.read());// 16384.0; //X-axis value
  AccY = (Wire.read() << 8 | Wire.read());// 16384.0; //Y-axis value
  AccZ = (Wire.read() << 8 | Wire.read());// 16384.0; //Z-axis value

  Wire.beginTransmission(MPU_register); // start acces MPU6050
  Wire.write(0x43); // start acces measurement of gyroscope
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_register,6,true); // from MPU6050 take 6 data

  GyroX = (Wire.read() << 8 | Wire.read()); // 131.0; //X axis value
  GyroY = (Wire.read() << 8 | Wire.read()); // 131.0; //Y axis value
  GyroZ = (Wire.read() << 8 | Wire.read()); // 131.0; //Z axis value

  theta_acc = -atan2((AccZ/4096),(AccX/4096))/2/3.141592653*360;

  Serial.print(AccX/4096);Serial.print(" ");
  Serial.print(AccY/4096);Serial.print(" ");
  Serial.print(AccZ/4096);Serial.print(" ");
  Serial.print(GyroX/32.8);Serial.print(" ");
  Serial.print(GyroY/32.8);Serial.print(" ");
  Serial.print(GyroZ/32.8);Serial.print(" ");
  Serial.print(theta_acc-5);Serial.println(",");
  delay(30);
}
