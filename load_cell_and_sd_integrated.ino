#include <SPI.h>
#include <SD.h>

File myFile;
const int chipSelect = 4;
String fileName;

bool isActive = false; // Tracks whether logging is active

float aReading0 = 415;
float aLoad0 = 0; // lbs.
float bReading0 = 413;
float bLoad0 = .577; // lbs.

float aReading1 = 413;
float aLoad1 = 0; // lbs.
float bReading1 = 383;
float bLoad1 = 9.3; // lbs.

int loadCellAPin = A0;
int loadCellBPin = A1;

long time = 0;
int interval = 250; // Interval between readings

void setup() {
  Serial.begin(9600);
  if (!SD.begin(chipSelect)) {
    Serial.println("Initialization failed!");
    while (1); // Halt execution
  }
  Serial.println("SD card is ready. Press Enter to start.");
}

void loop() {
  if (Serial.available() > 0) {
    Serial.readStringUntil('\n'); // Clear the serial buffer and wait for Enter
    if (!isActive) {
      // Start logging
      isActive = true;
      // Generate a unique filename and open a new file
      unsigned long timeStamp = millis();
      fileName = String(timeStamp) + ".csv";
      myFile = SD.open(fileName, FILE_WRITE);
      if (myFile) {
        myFile.println("Reading A, Load A, Reading B, Load B");
        myFile.close();
        Serial.println("Logging started. Press Enter to stop.");
      } else {
        Serial.println("Error creating file: " + fileName);
      }
    } else {
      // Stop logging
      isActive = false;
      Serial.println("Logging stopped. Press Enter to start again.");
    }
  }

  if (isActive && millis() > time + interval) {
    float newReadingA = analogRead(loadCellAPin);
    float newReadingB = analogRead(loadCellBPin);
    float loadA = ((bLoad0 - aLoad0) / (bReading0 - aReading0)) * (newReadingA - aReading0) + aLoad0;
    float loadB = ((bLoad1 - aLoad1) / (bReading1 - aReading1)) * (newReadingB - aReading1) + aLoad1;

    String dataString = String(newReadingA, 5) + "," + String(loadA, 5) + "," + String(newReadingB, 5) + "," + String(loadB, 5);

    // Write data to the current CSV file if logging is active
    myFile = SD.open(fileName, FILE_WRITE);
    if (myFile) {
      myFile.println(dataString);
      myFile.close();
      Serial.println("Data written to " + fileName + ": " + dataString);
    } else {
      Serial.println("Error opening file: " + fileName);
    }

    time = millis(); // Update the time for the next reading
  }
}
