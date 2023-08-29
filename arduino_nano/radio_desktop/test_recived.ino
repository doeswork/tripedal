#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10);  // CE, CSN
int steps[7][7];    // Assuming 7 steps with 7 integers each
bool startReceived = false;
int stepIndex = 0;

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(1, 0xF0F0F0F0E1LL);
  radio.setPALevel(RF24_PA_LOW);
  radio.startListening();
}

void loop() {
  if (radio.available()) {
    char receivedData[50] = {0};
    radio.read(&receivedData, sizeof(receivedData));
    receivedData[sizeof(receivedData) - 1] = '\0';

    if (strcmp(receivedData, "start") == 0) {
      startReceived = true;
      stepIndex = 0;
    } else if (strcmp(receivedData, "run") == 0) {
      startReceived = false;
      Serial.println("Received Complete Data");
      // Print the parsed steps array
      for (int i = 0; i < 7; i++) {
        Serial.print("Step ");
        Serial.print(i);
        Serial.print(": ");
        for (int j = 0; j < 7; j++) {
          Serial.print(steps[i][j]);
          if (j < 6) Serial.print(", ");
        }
        Serial.println();
      }
    } else if (startReceived) {
      // Parse and store
      char* token = strtok(receivedData, ",");
      int valueIndex = 0;
      while (token != NULL && valueIndex < 7) {
        steps[stepIndex][valueIndex] = atoi(token);
        token = strtok(NULL, ",");
        valueIndex++;
      }
      stepIndex++;
    }
  }
}
