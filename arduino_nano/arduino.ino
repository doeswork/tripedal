#include <Servo.h>

Servo myservo1;  // Create first servo object
Servo myservo2;  // Create second servo object
int pos1 = 0;    // Variable to store the servo1 position
int pos2 = 0;    // Variable to store the servo2 position

void setup() {
  Serial.begin(9600);
  myservo1.attach(6); // Attaches the first servo on pin 6
  myservo2.attach(7); // Attaches the second servo on pin 7
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '7') {
      pos1 = max(0, pos1 - 5); // Decrease servo position
      myservo1.write(pos1);
    } else if (command == '8') {
      pos1 = min(180, pos1 + 5); // Increase servo position
      myservo1.write(pos1);
    }
    else if (command == '4') {
      pos2 = max(0, pos2 - 5); // Decrease second servo position
      myservo2.write(pos2);
    } else if (command == '5') {
      pos2 = min(180, pos2 + 5); // Increase second servo position
      myservo2.write(pos2);
    }
  }
}
