void setup() {
  // Start the hardware serial communication with the computer and the Bluetooth module
  Serial.begin(9600);
  while (!Serial) {
    ; // Wait for the serial port to connect. This is needed for some boards such as the Leonardo, but not for the Uno
  }
}

void loop() {
  Serial.println("Hello, world!");

  Serial.println("AT"); // Ask the module about its state
  delay(100); // Give it a little time to respond

  while(Serial.available()) { // If there's data coming from the module
    char c = Serial.read();
    Serial.write(c); // Print this data to the main serial (to the computer)
  }

  delay(8000);
}
