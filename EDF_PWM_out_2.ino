/*
PJP ECU S-EDF A60010000J PWM code 2
By Jake Donnini and ECU team ;)
*/

const byte PWMPin = 10;  // Timer 1 "B" output: OC1B
const byte POTENTIOMETER = A0;
// set the frequency you want the PWM signal
const long FREQUENCY = 8000;
// set the bounds of the duty cycle of the PWM in %
const int MAX_PWM_BOUND = 90;
const int MIN_PWM_BOUND = 60;
int receivedDutyCycle;
bool newDataReceived;
int timer;

const long timer1_OCR1A_Setting = F_CPU / FREQUENCY;
void setup() 
 {
   Serial.begin(9600); // Set the baud rate for serial communication
  pinMode (PWMPin, OUTPUT);
  // Fast PWM top at OCR1A
  TCCR1A = _BV (WGM10) | _BV (WGM11) | _BV (COM1B1); // fast PWM, clear OC1B on compare
  TCCR1B = _BV (WGM12) | _BV (WGM13) | _BV (CS10);   // fast PWM, no prescaler
  // OCR1A will compare
  OCR1A =  timer1_OCR1A_Setting - 1;  // zero relative 
  newDataReceived = false;
  }  // end of setup

void loop() 
  { 
  //set a timer for printout debugging
  timer = timer + 1;
  // Check for available serial data
  if (Serial.available()) {
    // Read the duty cycle value
    receivedDutyCycle = Serial.parseInt();
  }

  // Validate the received value
  if (receivedDutyCycle < MIN_PWM_BOUND || receivedDutyCycle > MAX_PWM_BOUND) {
    if (timer % 100 == 50){
      // Error handling
      Serial.println("Please enter a value between 60 and 90");
      return;
    }
  } else {
    // Convert the duty cycle to a PWM value
    long pwmValue = map(receivedDutyCycle, MIN_PWM_BOUND, MAX_PWM_BOUND, 
                    0, 1023);

    // Set the PWM output based on the received value
    OCR1B = pwmValue;
  }
  
  }
