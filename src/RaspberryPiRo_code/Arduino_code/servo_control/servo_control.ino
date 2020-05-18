//#include<Servo.h> // include server library
//Servo ser; // create servo object to control a servo
//int poser = 0; // initial position of server
//int val; // initial value of input
//
//void setup() {
//  Serial.begin(9600); // Serial comm begin at 9600bps
//  ser.attach(5);// server is connected at pin 9
//}
//
//void loop() {
//  if (Serial.available()) // if serial value is available 
//  {
//    val = Serial.read();// then read the serial value
//    if (val == 'd') //if value input is equals to d
//    {
//      poser += 1; //than position of servo motor increases by 1 ( anti clockwise)
//      ser.write(poser);// the servo will move according to position 
//      delay(15);//delay for the servo to get to the position
//      Serial.println("d");
//     }
//    if (val == 'a') //if value input is equals to a
//    {
//      poser -= 1; //than position of servo motor decreases by 1 (clockwise)
//      ser.write(poser);// the servo will move according to position 
//      delay(15);//delay for the servo to get to the position
//      Serial.println("a");
//    }
// 
#include <Servo.h>

int servoPinPan = 5;
int servoPinTilt = 6;

Servo servo1;
Servo servo2;
int panAngle = 0;  // servo pan position in degrees
int tiltAngle = 0;  // servo tilt position in degrees

void setup() {
    servo1.attach(servoPinPan);
    servo2.attach(servoPinTilt);
}

void loop() {

    // 105 degrees of travel 35 - 140 on pan
    // Pan right from 35 to 140 degrees pan
    for(panAngle = 35; panAngle < 140; panAngle++) {
        servo1.write(panAngle);
        delay(15);
    }
    
//    // Pan left from 140 to 35 degrees pan
//    for(panAngle = 140; panAngle > 35; panAngle--) {
//        servo1.write(panAngle);
//        delay(15);
//    }

//    // 105 degrees of travel 0 - 105 on tilt
//    // Tilt down from 0 to 105 degrees tilt
//    for(tiltAngle = 0; tiltAngle < 105; tiltAngle++) {
//        servo2.write(tiltAngle);
//        delay(15);
//    }
    
//    // Tilt up from 105 to 0 degrees tilt
//    for(tiltAngle = 105; tiltAngle > 0; tiltAngle--) {
//        servo2.write(tiltAngle);
//        delay(15);
//    }
}
