#include <Servo.h>

Servo servos[9];  // Array to hold 9 servo objects

// Assign each servo to a digital pin on the Arduino
const int servoPins[9] = {2, 3, 4, 5, 6, 7, 8, 9, 10};

// Initial positions for each servo
const int initialPositions[9] = {90, 90, 90, 90, 90, 90, 90, 90, 90}; 

void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud rate

  // Initialize all servos and set them to their initial positions
  for (int i = 0; i < 9; i++) {
    servos[i].attach(servoPins[i]);
    servos[i].write(initialPositions[i]); // Set initial position
  }
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming string
    String data = Serial.readStringUntil('\n');
    int positions[9];
    int servoIndex = 0;

    // Parse the string into integers
    while (data.length() > 0 && servoIndex < 9) {
      int commaIndex = data.indexOf(',');
      if (commaIndex == -1) {
        positions[servoIndex++] = data.toInt();
        break;
      } else {
        positions[servoIndex++] = data.substring(0, commaIndex).toInt();
        data = data.substring(commaIndex + 1);
      }
    }

    // Move each servo to its corresponding position
    for (int i = 0; i < 9; i++) {
      servos[i].write(positions[i]);
    }
  }
}
