#include <Servo.h>
#include <Filters.h>

// setting up servo objects
Servo panServo;
Servo tiltServo;

// servo positions
int pan_pos = 0;
int tilt_pos = 0;

//offsets
int pos_offset = 0;
int tilt_offset = 90;

// ir sensor info
int sensor_value = 0;
int cm = 0;

// filter variables
int cm_lp = 0;
float filterFrequency_lp = 2.5;
int sensor_value_lp = 0;

// setting up filter object
FilterOnePole lowpassFilter( LOWPASS, filterFrequency_lp );

void setup() {
  // set up servos
  tiltServo.attach(10);
  panServo.attach(11);
  Serial.begin(9600);
}

void loop() {

  Serial.println("START");
  // startup sequence
  panServo.write(60);
  delay(1000);

  // iterate through pan positions
  for (pan_pos = 76; pan_pos <= 100; pan_pos += 1) {

    // set pan servo
    panServo.write(pan_pos);
    delay(50);

    tiltServo.write(90);
    delay(500);

    // iterate through tilt positions
    for (tilt_pos = 90; tilt_pos <= 150; tilt_pos += 1) {

      // set tilt servo
      tiltServo.write(tilt_pos);
      delay(50);

      // get the sensor value
      sensor_value = analogRead(A5);
      sensor_value_lp = lowpassFilter.input(sensor_value);
      cm = valueToDistance(sensor_value);
      cm_lp = valueToDistance(sensor_value_lp);

      Serial.print(pan_pos); Serial.print(" : "); Serial.print(tilt_pos - tilt_offset); 
      Serial.print(" : ");   Serial.print(cm);    Serial.print(" : "); Serial.println(cm_lp);
    }

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
