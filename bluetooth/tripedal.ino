#include <Servo.h>

Servo ankle; 
Servo center_leg;  
Servo left_knee;  
Servo right_knee;  
Servo left_thigh;  
Servo right_thigh;  
Servo bottom_foot;

int ankle_pos = 70;   
int center_leg_pos = 90;  
int left_knee_pos = 60;   
int right_knee_pos = 60;    
int left_thigh_pos = 90;    
int right_thigh_pos = 85;      
int bottom_foot_pos = 180; 

int STEPS_COUNT = 7; // Now not a const
int steps[7][7]; // Change the size accordingly, but be careful with memory on Arduino

bool new_data_received = false;  // Add this flag to keep track of new data

void setup() {

  ankle.attach(2);  
  center_leg.attach(5);  
  left_knee.attach(4); 
  right_knee.attach(7);  
  left_thigh.attach(6); 
  right_thigh.attach(8); 
  bottom_foot.attach(3); 

    // initialize servos to the upright position
  ankle.write(ankle_pos);
  center_leg.write(center_leg_pos);
  left_knee.write(left_knee_pos);
  right_knee.write(right_knee_pos);
  left_thigh.write(left_thigh_pos);
  right_thigh.write(right_thigh_pos);
  bottom_foot.write(bottom_foot_pos);


  delay(100); 
  Serial.begin(9600);

}

int counter = 0; // Counter to keep track of received numbers

void readBluetoothData() {
  if (Serial.available()) {
    int value = Serial.parseInt();  // Read the value
    int step_idx = counter / 7;  // Determine which step this value belongs to
    int value_idx = counter % 7;  // Determine the index within that step
    steps[step_idx][value_idx] = value;  // Assign the value to steps array
    Serial.print(value);  // Debugging line
    Serial.print(", ");  // Debugging line
    
    counter++;  // Increment the counter
    if (counter >= 49) {  // Reset counter if it reaches 49
      counter = 0;
      new_data_received = true;  // Flag to indicate a new set of steps is received
    }
  }
}




void updateServoPos(Servo &servo, int &current_pos, int target_pos) {
  if (current_pos < target_pos) {
    current_pos++;
  } else if (current_pos > target_pos) {
    current_pos--;
  }
  servo.write(current_pos);
}
void walkSequence() {
  for(int step = 0; step < STEPS_COUNT; ++step) {
    // Update target positions by adding deltas
    int center_leg_target = center_leg_pos + steps[step][0];
    int left_thigh_target = left_thigh_pos + steps[step][1];
    int right_thigh_target = right_thigh_pos + steps[step][2];
    int left_knee_target = left_knee_pos + steps[step][3];
    int right_knee_target = right_knee_pos + steps[step][4];
    int ankle_target = ankle_pos + steps[step][5];
    int bottom_foot_target = bottom_foot_pos + steps[step][6];

    // Make sure positions are in valid range
    center_leg_target = constrain(center_leg_target, 0, 180);
    left_thigh_target = constrain(left_thigh_target, 0, 180);
    right_thigh_target = constrain(right_thigh_target, 0, 180);
    left_knee_target = constrain(left_knee_target, 0, 180);
    right_knee_target = constrain(right_knee_target, 0, 180);
    ankle_target = constrain(ankle_target, 0, 180);
    bottom_foot_target = constrain(bottom_foot_target, 0, 180);


    // Wait until all servos have reached their target positions
    while(center_leg.read() != center_leg_target || left_thigh.read() != left_thigh_target || 
      right_thigh.read() != right_thigh_target || left_knee.read() != left_knee_target || 
      right_knee.read() != right_knee_target || ankle.read() != ankle_target || 
      bottom_foot.read() != bottom_foot_target) {

      // Update servo positions
      updateServoPos(center_leg, center_leg_pos, center_leg_target);
      updateServoPos(left_thigh, left_thigh_pos, left_thigh_target);
      updateServoPos(right_thigh, right_thigh_pos, right_thigh_target);
      updateServoPos(left_knee, left_knee_pos, left_knee_target);
      updateServoPos(right_knee, right_knee_pos, right_knee_target);
      updateServoPos(ankle, ankle_pos, ankle_target);
      updateServoPos(bottom_foot, bottom_foot_pos, bottom_foot_target);

      
      delay(10); // Slow down the servo movements
    }
  }
}

void loop() {
    readBluetoothData(); 

    if (new_data_received) {  // Only execute walkSequence if new data has been received
        while(true) {
            walkSequence();
        }
    }
    
    delay(100); 
}