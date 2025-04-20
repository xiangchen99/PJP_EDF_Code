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
int speed;

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
  int potValue = analogRead(POTENTIOMETER); // Reads from 0 to 1023
  int dutyCycle = map(potValue, 0, 1023, MIN_PWM_BOUND, MAX_PWM_BOUND);

  // Convert duty cycle % to OCR1B value
  long pwmValue = map(dutyCycle, 0, 100, 0, OCR1A); // scale to timer top

  OCR1B = pwmValue; // update PWM

  // Optional debug output
  Serial.print("Potentiometer: "); Serial.print(potValue);
  Serial.print(" | Duty Cycle: "); Serial.print(dutyCycle);
  Serial.print("% | PWM Value: "); Serial.println(pwmValue);

  delay(100); // smooth update
  
  }
