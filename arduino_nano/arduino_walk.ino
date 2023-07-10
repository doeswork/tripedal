#include <Servo.h>
//#include <SoftwareSerial.h>

Servo ankle; 
Servo center_leg;  
Servo left_knee;  
Servo right_knee;  
Servo left_thigh;  
Servo right_thigh;  

//SoftwareSerial mySerial(2, 3); // RX, TX

int ankle_pos = 0;   
int center_leg_pos = 0;  
int left_knee_pos = 0;   
int right_knee_pos = 0;    
int left_thigh_pos = 0;    
int right_thigh_pos = 0;    

void setup() {
  Serial.begin(9600);
  //mySerial.begin(9600);  // Bluetooth serial port

  ankle.attach(6);  
  center_leg.attach(7);  
  left_knee.attach(12); 
  right_knee.attach(11);  
  left_thigh.attach(8); 
  right_thigh.attach(9); 
}

void moveToPos(Servo &servo, int &currentPos, int newPos, int delayMs) {
  if (newPos > currentPos) {
    for (; currentPos <= newPos; currentPos++) {
      servo.write(currentPos);
      delay(delayMs);
    }
  } else {
    for (; currentPos >= newPos; currentPos--) {
      servo.write(currentPos);
      delay(delayMs);
    }
  }
}

void walkSequence() {
  // Step 1
  moveToPos(center_leg, center_leg_pos, 180, 10);

  // Step 2
  moveToPos(left_thigh, left_thigh_pos, 0, 10);
  moveToPos(right_thigh, right_thigh_pos, 180, 10);

  // Step 3
  moveToPos(left_knee, left_knee_pos, 0, 10);
  moveToPos(right_knee, right_knee_pos, 180, 10);

  // Step 4
  moveToPos(ankle, ankle_pos, 50, 10);

  // Step 5
  moveToPos(left_knee, left_knee_pos, 90, 10);
  moveToPos(right_knee, right_knee_pos, 90, 10);

  // Step 6
  moveToPos(center_leg, center_leg_pos, 0, 10);
}


void loop() {
    walkSequence();
}

