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

void walkSequence() {
    // Step 1
    center_leg_pos = 180;
    center_leg.write(center_leg_pos);
    delay(500);

    // Step 2
    left_thigh_pos = 0;
    right_thigh_pos = 180;
    left_thigh.write(left_thigh_pos);
    right_thigh.write(right_thigh_pos);
    delay(500);

    // Step 3
    left_knee_pos = 0;
    right_knee_pos = 180;
    left_knee.write(left_knee_pos);
    right_knee.write(right_knee_pos);
    delay(500);

    // Step 4
    ankle_pos = 50;
    ankle.write(ankle_pos);
    delay(500);

    // Step 5
    left_knee_pos = 90;
    right_knee_pos = 90;
    left_knee.write(left_knee_pos);
    right_knee.write(right_knee_pos);
    delay(500);

    // Step 6
    center_leg_pos = 0;
    center_leg.write(center_leg_pos);
    delay(500);
}


void loop() {
    walkSequence();
}

