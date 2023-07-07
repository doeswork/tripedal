#include <SoftwareSerial.h>

SoftwareSerial mySerial(2, 3); // RX, TX

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);  // Bluetooth serial port
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    mySerial.write(command);
  }
}
