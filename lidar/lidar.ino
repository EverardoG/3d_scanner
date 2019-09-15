#include <Servo.h>
#include <Filters.h>

Servo panServo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
int sensor_value = 0;
int cm = 0;

// filter variables
int cm_lp = 0;
float filterFrequency_lp = 2.5;
int sensor_value_lp = 0;

FilterOnePole lowpassFilter( LOWPASS, filterFrequency_lp ); 

void setup() {
  panServo.attach(11);  // attaches the servo on pin 9 to the servo object
  Serial.begin(9600);
}

void loop() {
  panServo.write(0);
  delay(1000);
  for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    panServo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
    sensor_value = analogRead(A5);
    cm = valueToDistance(sensor_value);

    sensor_value_lp = lowpassFilter.input(sensor_value);
    cm_lp = valueToDistance(sensor_value_lp);
    
    Serial.print(pos); Serial.print(" : "); Serial.println(cm_lp);
  }
  
// code for scanning backwards
//  for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
//    panServo.write(pos);              // tell servo to go to position in variable 'pos'
//    delay(15);                       // waits 15ms for the servo to reach the position
//    sensor_value = analogRead(A5);
//    cm = valueToDistance(sensor_value);
//
//    sensor_value_lp = lowpassFilter.input(sensor_value);
//    cm_lp = valueToDistance(sensor_value_lp);
//    
//    Serial.print(pos); Serial.print(" : "); Serial.println(cm_lp);
//  }

// code for checking that the servo really got to 180 degrees
//  panServo.write(180);
//  delay(1000);
}

int valueToDistance(int sensor_value) {
  float cm = 10650.08 * pow(sensor_value, -0.935) - 10;
  return cm;
}
