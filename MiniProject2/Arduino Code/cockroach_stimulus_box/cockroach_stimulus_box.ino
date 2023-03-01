/*
  Motion detector and light stimulus activity
  Designed for experiments with Blaberus discoidalis (False Death's Head cockroach)
  Written by James Crall (james.crall@wisc.edu) for ENto 375: Digital Ecology (S'23)
  Further materials available at: https://github.com/Crall-Lab/DigitalEcology
*/
#include "RTClib.h"
#include <SPI.h>
#include <SD.h>

const int chipSelect = 10;

RTC_PCF8523 rtc;

//Set up variables that will not change during the script (LED pins and sensors pins)
#define LEDPIN_1 9
#define LEDPIN_2 8
#define SENSORPIN_1 3
#define SENSORPIN_2 4

int LIGHT_PIN = 7;
//Pin 7 will be for actually turning on leds, this will switch to 6 as a dummy variable (nothing attached to 6)

#define ST_PIN 7 //Define a pin that the stimulus LEDs are actually connected to
#define DUMMY_PIN 6;

String stimulus_mode = "on";

int TRIGGER_PIN = SENSORPIN_1; // Set the stimulus light LEDs to trigger off of sensor pin 1

// variables that will change:
int sensorState_1 = 0, sensorState_2 = 0, lastState_1 = 0, lastState_2 = 0, s1_counter = 0, s2_counter = 0, s1_movement = 0, s2_movement = 0;

//Set timing
int time_int = 100; //Interval between loop steps
int max_recording_iters = 10 * 60 * 1; //currently set for 4 minute recording intervals (1 loop = 100 ms, so 10 loops = 1 sec, 10 loop * 60 sec * 4 mins)
int counter = 0; //Initialize a counter for recording cycle

void setup() {
  // initialize the LED pin as an output:
  pinMode(LEDPIN_1, OUTPUT);
  pinMode(LEDPIN_2, OUTPUT);
  pinMode(LIGHT_PIN, OUTPUT);

  // initialize the sensor pins as an input:
  pinMode(SENSORPIN_1, INPUT);
  digitalWrite(SENSORPIN_1, HIGH); // turn on the pullup

  // initialize the sensor pins as an input:
  pinMode(SENSORPIN_2, INPUT);
  digitalWrite(SENSORPIN_2, HIGH); // turn on the pullup

  Serial.begin(9600);

  //  Set up real-time clock
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    Serial.flush();
    while (1) delay(10);
  }



  //Set up the SD card

  Serial.print("Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    while (1);
  }
  Serial.println("card initialized.");
}




void loop() {

  counter = 0; //For each loop round, reset the counter
  s1_counter = 0;
  s2_counter = 0;
  s1_movement = 0;
  s2_movement = 0;

  //Record mode - check whether the light pin is connected to the stimulus pin (meaning stimulus after being triggered), or not (in which case, stimulus is off)
  if (LIGHT_PIN == ST_PIN) {
    stimulus_mode = "on";
  } else {
    stimulus_mode = "off";
  }

  Serial.print("Starting cycle, stimulus is ");
  Serial.println(stimulus_mode);
  while (counter < max_recording_iters) {

    //Sensor 1

    // read the state of the pushbutton value:
    sensorState_1 = digitalRead(SENSORPIN_1);


    // check if the sensor beam is broken
    // if it is, the sensorState is LOW:
    if (sensorState_1 == LOW) {
      // turn LED on:
      digitalWrite(LEDPIN_1, HIGH);
      s1_counter += 1; //increment the s1 counter
      //If this is the trigger pin, also turn on the white LED
      if (TRIGGER_PIN == SENSORPIN_1) {
        digitalWrite(LIGHT_PIN, HIGH);
      }
    } else {
      // turn LED off:
      digitalWrite(LEDPIN_1, LOW);

      if (TRIGGER_PIN == SENSORPIN_1) {
        digitalWrite(LIGHT_PIN, LOW);
      }
    }

    //Check if movement is newly detected
    if (!sensorState_1 && lastState_1) {
      Serial.println("Movement on beam 1");
      s1_movement += 1; //Add one to the sensor 1 movement counter
    }
    lastState_1 = sensorState_1;



    //Sensor 2
    // read the state of the pushbutton value:
    sensorState_2 = digitalRead(SENSORPIN_2);

    // check if the sensor beam is broken
    // if it is, the sensorState is LOW:
    if (sensorState_2 == LOW) {
      // turn LED on:
      digitalWrite(LEDPIN_2, HIGH);
      s2_counter += 1; //increment the s2 counter

      //If this is the trigger pin, also turn on the white LED
      if (TRIGGER_PIN == SENSORPIN_2) {
        digitalWrite(LIGHT_PIN, HIGH);
      }
    } else {
      // turn LED off:
      digitalWrite(LEDPIN_2, LOW);

      if (TRIGGER_PIN == SENSORPIN_2) {
        digitalWrite(LIGHT_PIN, LOW);
      }
    }

    //Check if movement is newly detected
    if (!sensorState_2 && lastState_2) {
      Serial.println("Movement on beam 2");
      s2_movement += 1; //Add one to the sensor 2 movement counter
    }
    lastState_2 = sensorState_2;

    //Delay until next loop round
    delay(time_int);
    counter += 1;

  }
  
  //Open file and log data
  File dataFile = SD.open("ActLgr.csv", FILE_WRITE); //NB you can change the filename, but must be shorter than 8 characters total

  //Get and print timestamp
  if (dataFile) {
    DateTime now = rtc.now();
    dataFile.print(now.year(), DEC);
    dataFile.print('-');
    dataFile.print(now.month(), DEC);
    dataFile.print('-');
    dataFile.print(now.day(), DEC);
    dataFile.print("_");
    dataFile.print(now.hour(), DEC);
    dataFile.print(':');
    dataFile.print(now.minute(), DEC);
    dataFile.print(':');
    dataFile.print(now.second(), DEC);
    dataFile.print(',');
    dataFile.print(s1_counter);
    dataFile.print(',');
    dataFile.print(s2_counter);
    dataFile.print(',');
    dataFile.print(s1_movement);
    dataFile.print(',');
    dataFile.print(s2_movement);
    dataFile.print(',');
    dataFile.print(stimulus_mode);
    dataFile.println(""); //End the line in the csv file
    dataFile.close(); //Close out the file
    Serial.println("Data written to SD card");
  } else {
    Serial.println("error opening logging file");
  }

  Serial.println("Finished recording cycle, data recorded");

  //Turn stimulus LED off if it was on
  digitalWrite(ST_PIN, LOW);

  //Alternate between stimulus being on and off
  if (LIGHT_PIN == ST_PIN) {
    LIGHT_PIN = DUMMY_PIN;
  } else {
    LIGHT_PIN = ST_PIN;
  }

}
