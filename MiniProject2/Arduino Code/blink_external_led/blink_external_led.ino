// Basic control of an external LED with Arduino Uno
// Written by James Crall
// Ento 375: Digital Ecology, S'23
// This is a comment! (note difference from python)
// Wiring: red LED should be connected to digital pin 10 on the Arduino with a 270 ohm resistor in-line


int led_pin = 10; // This line intializes variable named 'led_pin' and sets its value to 10.
// The 'int' here defines this variable type as an integer
// notce the ';' at the end of the line, which needs to be present at the end of every line of code
// (except loop statements, etc)

void setup() {
  //setup loop: this runs only once at code initiation
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(led_pin, OUTPUT);
}

void loop() {
  // the 'loop' section runs continuously after initialization, so put the code you want to run continuously here
  digitalWrite(led_pin, HIGH); // Write the LED pin (10) to 'high' = 5v = on
  delay(1000); // Wait 1000 ms = 1 second
  digitalWrite(led_pin, LOW); //Write the LED pin to 'low' = 0v = off
  delay(1000); //Wait again
  Serial.println('blinked!');
}
