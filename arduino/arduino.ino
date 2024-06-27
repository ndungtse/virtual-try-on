#include <SoftwareSerial.h>

SoftwareSerial bluetoothSerial(10, 11);  // RX, TX pins for SoftwareSerial

const int buzzer = 9;

void setup() {
  Serial.begin(38400);           // Serial monitor for debugging
  bluetoothSerial.begin(38400);  // Bluetooth serial connection
  pinMode(buzzer, OUTPUT);
}

void loop() {
  // Read data from Bluetooth module (slave module)
  if (bluetoothSerial.available()) {
    String receivedData = bluetoothSerial.readString();           // Read the data received from Bluetooth module
    Serial.println("Received data from slave: " + receivedData);  // Print received data to serial monitor (for debugging)

    // Example: Send received data back to slave HC-05 module
    bluetoothSerial.write(receivedData.c_str());  // Uncomment to send data back to slave
  }

  // Read data from Serial monitor (connected to your computer running Python script)
  if (Serial.available()) {
    String sendData = Serial.readString();    // Read the data from Serial monitor
    bluetoothSerial.write(sendData.c_str());  // Send data received from Serial monitor over Bluetooth to slave HC-05 module

    // Print the sent data to serial monitor (for debugging)
    Serial.println("Sent data to slave: " + sendData);
  }

  // buzzer tone
  tone(buzzer, 1000);  // Send 1KHz sound signal...
  delay(1000);         // ...for 1 sec
  noTone(buzzer);      // Stop sound...
  delay(1000);
}
