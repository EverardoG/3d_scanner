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

// motor settings
int pan_inc = 1;
int tilt_inc = 1;

int pan_max = 100;
int pan_min = 60;

int tilt_max = 125;
int tilt_min = 75;

int pan_delay = 15 * pan_inc;
int tilt_delay = 15 * tilt_inc;
int long_tilt_delay = 5 * (tilt_max - tilt_min);
int long_pan_delay = 15 * (pan_max  - pan_min);

// ir sensor info
int sensor_value = 0;
float cm = 0;

// filter variables
float cm_lp = 0;
float filterFrequency_lp = 2.5;
float sensor_value_lp = 0;

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
  panServo.write(pan_min);
  delay(long_pan_delay);

  // iterate through pan positions
  for (pan_pos = pan_min; pan_pos <= pan_max; pan_pos += pan_inc) {

    // set pan servo
    panServo.write(pan_pos);
    delay(pan_delay); // 50

    tiltServo.write(tilt_min);
    delay(long_tilt_delay); //500

    // iterate through tilt positions
    for (tilt_pos = tilt_min; tilt_pos <= tilt_max; tilt_pos += tilt_inc) {

      // set tilt servo
      tiltServo.write(tilt_pos);
      delay(tilt_delay); //50

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

float valueToDistance(int sensor_value) {
  float voltage = sensor_value/1023.0;
  float cm = 22.2829 * pow(voltage, -0.757409) - 17.7591;
  return cm;
}
