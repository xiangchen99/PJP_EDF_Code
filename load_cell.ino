// Arduino with two load cells - Sender

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
int interval = 250; // Take a reading every 250 ms

void setup() {
  Serial.begin(9600);
}

void loop() {
  float newReadingA = analogRead(loadCellAPin);
  float newReadingB = analogRead(loadCellBPin);

  // Calculate load based on A and B readings above
  float loadA = ((bLoad0 - aLoad0) / (bReading0 - aReading0)) * (newReadingA - aReading0) + aLoad0;
  float loadB = ((bLoad1 - aLoad1) / (bReading1 - aReading1)) * (newReadingB - aReading1) + aLoad1;

  // millis returns the number of milliseconds since the board started the current program
  if (millis() > time + interval) {
    // Construct the data string
    String dataString = String(newReadingA, 5) + "," + String(loadA, 5) + "," + String(newReadingB, 5) + "," + String(loadB, 5);

    // Send the data string to the second Arduino
    Serial.println(dataString); // Using println to add a newline character at the end

    time = millis();
  }
}
