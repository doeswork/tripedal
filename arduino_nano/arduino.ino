#include <Servo.h>

Servo myservo1;  // Create first servo object
Servo myservo2;  // Create second servo object
Servo myservo3;  // Create third servo object
Servo myservo4;  // Create fourth servo object
Servo myservo5;  // Create fifth servo object
Servo myservo6;  // Create sixth servo object

int pos1 = 0;    // Variable to store the servo1 position
int pos2 = 0;    // Variable to store the servo2 position
int pos3 = 0;    // Variable to store the servo3 position
int pos4 = 0;    // Variable to store the servo4 position
int pos5 = 0;    // Variable to store the servo5 position
int pos6 = 0;    // Variable to store the servo6 position

void setup() {
  Serial.begin(9600);
  myservo1.attach(6); // Attaches the first servo on pin 6
  myservo2.attach(7); // Attaches the second servo on pin 7
  myservo3.attach(12); // Attaches the third servo on pin 12
  myservo4.attach(9); // Attaches the fourth servo on pin 9
  myservo5.attach(10); // Attaches the fifth servo on pin 10
  myservo6.attach(11); // Attaches the sixth servo on pin 11
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'w') {
      pos1 = max(0, pos1 - 5); // Decrease servo position
      myservo1.write(pos1);
    } else if (command == 's') {
      pos1 = min(180, pos1 + 5); // Increase servo position
      myservo1.write(pos1);
    } else if (command == 'e') {
      pos2 = max(0, pos2 - 5); // Decrease second servo position
      myservo2.write(pos2);
    } else if (command == 'd') {
      pos2 = min(180, pos2 + 5); // Increase second servo position
      myservo2.write(pos2);
    } else if (command == 'r') {
      pos3 = max(0, pos3 - 5); // Decrease third servo position
      myservo3.write(pos3);
    } else if (command == 'f') {
      pos3 = min(180, pos3 + 5); // Increase third servo position
      myservo3.write(pos3);
    } else if (command == 't') {
      pos4 = max(0, pos4 - 5); // Decrease fourth servo position
      myservo4.write(pos4);
    } else if (command == 'g') {
      pos4 = min(180, pos4 + 5); // Increase fourth servo position
      myservo4.write(pos4);
    } else if (command == 'y') {
      pos5 = max(0, pos5 - 5); // Decrease fifth servo position
      myservo5.write(pos5);
    } else if (command == 'h') {
      pos5 = min(180, pos5 + 5); // Increase fifth servo position
      myservo5.write(pos5);
    } else if (command == 'u') {
      pos6 = max(0, pos6 - 5); // Decrease sixth servo position
      myservo6.write(pos6);
    } else if (command == 'j') {
      pos6 = min(180, pos6 + 5); // Increase sixth servo position
      myservo6.write(pos6);
    }
  }
}
