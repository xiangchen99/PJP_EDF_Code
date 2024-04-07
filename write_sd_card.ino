#include <SPI.h>
#include <SD.h>

File myFile;
const int chipSelect = 4;

void setup() {
  Serial.begin(9600); // Initialize serial communication at the same baud rate as the sender
  if (!SD.begin(chipSelect)) {
    Serial.println("Initialization failed!");
    while (1); // Infinite loop to halt further execution
  }
  Serial.println("SD card is ready.");

  // If the data file does not exist, create it and add the header
  if (!SD.exists("data.csv")) {
    myFile = SD.open("data.csv", FILE_WRITE);
    if (myFile) {
      myFile.println("Reading A, Load A, Reading B, Load B");
      myFile.close();
    }
  }
}

void loop() {
  String dataString = "";

  // Check if data is available to read
  if (Serial.available()) {
    delay(100); // Small delay to allow the buffer to fill
    dataString = Serial.readStringUntil('\n'); // Read the incoming data until newline

    // Open the file in write mode
    myFile = SD.open("data.csv", FILE_WRITE);
    if (myFile) {
      myFile.println(dataString); // Write the data string to the file
      myFile.close(); // Close the file
      Serial.println("Data written to SD card: " + dataString);
    } else {
      Serial.println("Error opening the file.");
    }
  }
}
