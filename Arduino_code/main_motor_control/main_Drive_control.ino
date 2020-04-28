#include <Wire.h>
#include <Servo.h>


#define SLAVE_ADDRESS 0x18

bool set_auto = false;

// defines pins numbers
const int fwdTrigPin = 28;
const int fwdEchoPin = 29;
const int lFwdTrigPin = 30;
const int lFwdEchoPin = 31;
const int rFwdTrigPin = 32;
const int rFwdEchoPin = 33;
const int aftTrigPin = 34;
const int aftEchoPin = 35;
const int camTrigPin = 36;
const int camEchoPin = 37;

// defines variables
long fDuration;
long lFDuration;
long rFDuration;
long aDuration;
long cDuration;
int fDistance;
int lFDistance;
int rFDistance;
int aDistance;
int cDistance;

volatile boolean receiveFlag = false;
char temp[32];
int command;

// Motor variables
int direction_L;
int brake_L;
int speed_L;
int direction_R;
int brake_R;
int speed_R;
int runTime;

float maxDist = 150.00;
float mi1Dist = 110.00;
float mi2Dist= 70.00;
float minDist = 40.00;

String move_fwd_full = "1-0-255-0-0-255-00";
String move_fwd_mi1 = "1-0-220-0-0-215-00";
String move_fwd_mi2 = "1-0-180-0-0-175-00";
String move_fwd_close = "1-0-120-0-0-120-00";

String reverse = "0-0-120-1-0-120-000";

String all_stop = "1-0-000-0-0-000-00";

String spin_right = "1-0-155-1-0-155-250";
String spin_left = "0-0-155-0-0-155-250";

String turn_right = "1-0-155-1-0-155-2000";
String turn_left = "0-0-155-0-0-155-2000";

void setup() {
    // initialize i2c as slave
    Wire.begin(SLAVE_ADDRESS);
    
    // define callbacks for i2c communication
    Wire.onReceive(receiveEvent);
    Serial.begin(9600); // Starts the serial communication  
      
    pinMode(fwdTrigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(fwdEchoPin, INPUT); // Sets the echoPin as an Input
    pinMode(lFwdTrigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(lFwdEchoPin, INPUT); // Sets the echoPin as an Input
    pinMode(rFwdTrigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(rFwdEchoPin, INPUT); // Sets the echoPin as an Input
    pinMode(aftTrigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(aftEchoPin, INPUT); // Sets the echoPin as an Input
    pinMode(camTrigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(camEchoPin, INPUT); // Sets the echoPin as an Input
}

void loop() {

    if (receiveFlag == true) {
        Serial.println(temp);
        String phrase;
        phrase = String(phrase + temp);
        command = phrase.substring(0, 3).toInt();
        Serial.println(command);

        // Need to add an option for manual or autonomous driving sofar 1 is auto 2,3,4,5 are fwd, rev, L and R   
        if (set_auto == false) {
//           Drive motor activated
    
            if (command == 2) {
                  // Drive motor activated forward
                  Serial.println("Drive motor activated forward manual forward");
                  direction_L = 1;
                  brake_L = 0;
                  speed_L = 255;
                  direction_R = 0;
                  brake_R = 0;
                  speed_R = 255;
                  runTime = 1;
                  
                  motorControl(direction_L, brake_L, speed_L, direction_R, brake_R, speed_R, runTime);
                  receiveFlag = false;
            }
    
            if (command == 3) {
                  // Drive motor activated reverse
                  Serial.println("Drive motor activated reverse manual reverse");
                  direction_L = 0;
                  brake_L = 0;
                  speed_L = 255;
                  direction_R = 1;
                  brake_R = 0;
                  speed_R = 255;
                  runTime = 1;
                  
                  motorControl(direction_L, brake_L, speed_L, direction_R, brake_R, speed_R, runTime);
                  receiveFlag = false;
            }
    
            if (command == 4) {
                  // Drive motor activated left
                  Serial.println("Drive motor activated left manual left");
                  direction_L = 0;
                  brake_L = 0;
                  speed_L = 200;
                  direction_R = 1;
                  brake_R = 0;
                  speed_R = 200;
                  runTime = 1;
                  
                  motorControl(direction_L, brake_L, speed_L, direction_R, brake_R, speed_R, runTime);
                  receiveFlag = false;
            }
    
            if (command == 5) {
                  // Drive motor activated right
                  Serial.println("Drive motor activated right manual right");
                  direction_L = 1;
                  brake_L = 0;
                  speed_L = 200;
                  direction_R = 0;
                  brake_R = 0;
                  speed_R = 200;
                  runTime = 1;
      
                  motorControl(direction_L, brake_L, speed_L, direction_R, brake_R, speed_R, runTime);
                  receiveFlag = false;
            }
        }

        if (command == 6) {
            set_auto = true;
            receiveFlag = false;
          
        }

        if (command == 7) {
            set_auto = false;
            // Drive motor stoped
            Serial.println("Drive motor stopped");
            direction_L = 1;
            brake_L = 1;
            speed_L = 000;
            direction_R = 0;
            brake_R = 1;
            speed_R = 000;
            runTime = 1;
            
            motorControl(direction_L, brake_L, speed_L, direction_R, brake_R, speed_R, runTime);
            receiveFlag = false;
        }
    } 
      
    if (set_auto == true){
        maneuver(); 
        Serial.print("Automatic mode ");
    }
    
//    receiveFlag = false;

    delay(1);

    
}

float get_fwd_distance() {
    // Clears the trigPin
    digitalWrite(fwdTrigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(fwdTrigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(fwdTrigPin, LOW);
    delayMicroseconds(2);
    
    // Reads the echoPin, returns the sound wave travel time in microseconds
    fDuration = pulseIn(fwdEchoPin, HIGH);
    
    // Calculating the distance
    fDistance = (fDuration/2)/29.1;

    // Prints the distance on the Serial Monitor
    Serial.print("Fwd Distance: ");
    Serial.println(fDistance);
    
    return fDistance;
}

float get_left_fwd_distance() {
    // Clears the trigPin
    digitalWrite(lFwdTrigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(lFwdTrigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(lFwdTrigPin, LOW);
    delayMicroseconds(2);
    
    // Reads the echoPin, returns the sound wave travel time in microseconds
    lFDuration = pulseIn(lFwdEchoPin, HIGH);

    // Calculating the distance
    lFDistance = (lFDuration/2)/29.1;

    // Prints the distance on the Serial Monitor
    Serial.print("Left Fwd Distance: ");
    Serial.println(lFDistance);
    
    return lFDistance;
}


float get_right_fwd_distance() {
    // Clears the trigPin
    digitalWrite(rFwdTrigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(rFwdTrigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(rFwdTrigPin, LOW);
    delayMicroseconds(2);
    
    // Reads the echoPin, returns the sound wave travel time in microseconds
    rFDuration = pulseIn(rFwdEchoPin, HIGH);

    // Calculating the distance
    rFDistance = (rFDuration/2)/29.1;

    // Prints the distance on the Serial Monitor
//    Serial.print("Right Fwd Distance: ");
//    Serial.println(rFDistance);

    return rFDistance;
    
}

float get_aft_distance() {
    // Clears the trigPin
    digitalWrite(aftTrigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(aftTrigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(aftTrigPin, LOW);
    
    // Reads the echoPin, returns the sound wave travel time in microseconds
    aDuration = pulseIn(aftEchoPin, HIGH);

    // Calculating the distance
    aDistance = (aDuration/2)/29.1;

    // Prints the distance on the Serial Monitor
//    Serial.print("Aft Distance: ");
//    Serial.println(aDistance);

    return aDistance;
    
}

float get_cam_distance() {
    // Clears the trigPin
    digitalWrite(camTrigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(camTrigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(camTrigPin, LOW);
    
    // Reads the echoPin, returns the sound wave travel time in microseconds
    cDuration = pulseIn(camEchoPin, HIGH);

    // Calculating the distance
    cDistance = (cDuration/2)/29.1;

    // Prints the distance on the Serial Monitor
//    Serial.print("Cam Distance: ");
//    Serial.println(cDistance);

    return cDistance;  
}

void motorControl(int direction_L, int brake_L, int speed_L, int direction_R, int brake_R, int speed_R, int runTime) {
  
    //Motor A forward full speed
    digitalWrite(12, direction_L);                                      // Establishes forward direction of Motor A
    digitalWrite(9, brake_L);                                           // Disengage the Brake for Motor A
    analogWrite(3, speed_L);                                            // Spins the motor on Motor A at full speed
  
    //Motor B forward full speed
    digitalWrite(13,direction_R);                                       // Establishes forward direction of Motor B
    digitalWrite(8, brake_R);                                           // Disengage the Brake for Motor B
    analogWrite(11, speed_R);                                           // Spins the motor on Motor B at full speed
  
    delay(runTime);
}


void receiveEvent(int howMany) {
//    Serial.print(howMany);
    for (int i = 0; i < howMany; i++) {
        temp[i] = Wire.read();
        temp[i + 1] = '\0'; // Add null after each char
    }
  
    //RPi first byte is cmd byte so shift everything to the left 1 pos so temp contains string
    for (int i = 0; i < howMany; i++)
        temp[i] = temp[i + 1];
  
    receiveFlag = true;
}

void move_command(String command) {
    direction_L = command.substring(0, 1).toInt();
    brake_L = command.substring(2, 3).toInt();
    speed_L = command.substring(4, 7).toInt();
    direction_R = command.substring(8, 9).toInt();
    brake_R = command.substring(10, 11).toInt();
    speed_R = command.substring(12, 15).toInt();
    runTime = command.substring(16).toInt();

    Serial.println("Drive motor activated");

    motorControl(direction_L, brake_L, speed_L, direction_R, brake_R, speed_R, runTime);
    
}

void maneuver() {

    float forD = get_fwd_distance();
    float forL = get_left_fwd_distance();
    float forR = get_right_fwd_distance();

    if (forL < 30.00) {
      move_command(spin_right);
      
    } else if (forR < 30.00) {
        move_command(spin_left);
        
    }
     
    if (forD > maxDist) {
        Serial.println("Max Distance -- Forward full speed");
        move_command(move_fwd_full);
//        break;

    } else if (forD > mi1Dist && forD < maxDist) {
        Serial.println("Mid 1 Range -- Forward Mid 1 speed");
        move_command(move_fwd_mi1);
//        break;

    } else if (forD > mi2Dist && forD < mi1Dist) {
        Serial.println("Mid 2 Range -- Forward Mid 2 speed");
        move_command(move_fwd_mi2);
//        break;

    } else if (forD > minDist && forD < mi1Dist) {
        Serial.println("Min Distance -- Forward close speed");
        move_command(move_fwd_close);
//        break;

    } else {

        if (forD < minDist) {
            move_command(all_stop);

        float forD = get_fwd_distance();
        float forL = get_left_fwd_distance();
        float forR = get_right_fwd_distance();
        
        }
        
        if ((forD + forL) > (forD + forR)) { 
            Serial.println("Turning left");
            move_command(turn_left);
        } else {
            Serial.println("Turning right");
            move_command(turn_right);
        }
        
        if (forL + forR < 10.00) 
            float forD = get_fwd_distance();
            float forL = get_left_fwd_distance();
            float forR = get_right_fwd_distance();
            float aftD = get_aft_distance();
          
            if (forL > forR) {
                move_command(spin_left);
                Serial.println("Turning left");
            } else if (forL < forR) {
                move_command(spin_right);
                Serial.println("Turning right");
            } else if (forD < aftD) {
                Serial.println("This vehicle is reversing");          
                move_command(reverse); 
            } else if (aftD < minDist) {
                move_command(all_stop);
            }
       
        }     
    }
