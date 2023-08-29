#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10); // CE, CSN

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(0xF0F0F0F0E1LL);  // you should use the same address on both Arduinos
}

void loop() {
  if(Serial.available()) {
    // Assume data will fit within 256 characters.
    char receivedData[256];
    Serial.readBytesUntil('\n', receivedData, sizeof(receivedData));
    
    // Send receivedData via NRF24L01+
    radio.write(&receivedData, sizeof(receivedData));
  }
}
