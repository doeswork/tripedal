
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10);  // CE, CSN

String incomingData = "";  // variable to store the incoming data

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  radio.setPALevel(RF24_PA_LOW);
}

void loop() {
  if (Serial.available()) {
    // read the incoming string
    incomingData = Serial.readStringUntil('\n');
    
    // check if it's a "start", "run" or a step
    if (incomingData == "start") {
      // Do nothing for now, or signal the other Arduino that a new sequence is starting
    } else if (incomingData == "run") {
      // Signal the other Arduino to run the steps
      radio.write("run", sizeof("run"));
    } else {
      // Send the step
      char stepChar[32]; // Adjust size as needed
      incomingData.toCharArray(stepChar, sizeof(stepChar));
      radio.write(&stepChar, sizeof(stepChar));
    }
  }
}
