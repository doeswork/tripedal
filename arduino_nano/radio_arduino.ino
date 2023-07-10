#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <Servo.h>

#define CE_PIN 9
#define CSN_PIN 10

RF24 radio(CE_PIN, CSN_PIN); // Create a Radio
Servo myservo1; // Create a Servo object
int pos1 = 0;    // Variable to store the servo6 position

void setup() {
  myservo1.attach(6);  // Attaches the first servo on pin 6
  radio.begin();
  radio.openReadingPipe(1, 0xF0F0F0F0E1LL);
  radio.setPALevel(RF24_PA_HIGH);
  radio.startListening(); // Start listening for messages
}

void loop() {
  if (radio.available()) {
    char text[32] = "";
    radio.read(&text, sizeof(text));

    // Let's assume 'l' for left (0 degrees) and 'r' for right (180 degrees)
    if (text[0] == 'l') {
      pos1 = max(0, pos1 - 5); // Decrease servo position
      myservo1.write(pos1);
    } else if (text[0] == 'r') {
      pos1 = max(0, pos1 + 5); // increase servo position
      myservo1.write(pos1);
    }
  }
}