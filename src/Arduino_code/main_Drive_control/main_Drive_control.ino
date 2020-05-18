#include <Wire.h>

#include <Servo.h>

#define SLAVE_ADDRESS 0x18

int i = 0;
int main_loop_counter = 0;

// Timer variables
unsigned long startMillis;
unsigned long currentMillis;
const unsigned long period = 1000;  //milliseconds

// Defines servo pins
int servoPinPan = 5;
int servoPinTilt = 6;

// Servo setup for pan and tilt
Servo servo1;
Servo servo2;
int panAngle = 110;  // servo pan position in degrees
int tiltAngle = 95;  // servo tilt position in degreesall
String cv_data = "";

int x1 = 0;
int x2 = 0;
int y1 = 0;
int y2 = 0;
int trigger = 0;
int confirm = 0;
int item = 0;
double percent = 0.0;
int cx = 200;
int cy = 150;
int width = 400;
int mid_width = 200;
int height = 300;
int mid_height = 150;
int box_width = 0;
int box_height = 0;
int left_width = 0;
//int top_height = 0;
volatile boolean initial_start_up = true;
volatile boolean set_auto = false;
volatile boolean pan_left = false;
volatile boolean pan_right = false;
volatile boolean tilt_up = false;
volatile boolean tilt_down = false;
volatile boolean investigate = false;
volatile boolean pan_cent = true;
volatile boolean tilt_cent = true;
int top_height = 0;

//int pan_left = 0;
//int pan_right = 0;
//int tilt_up = 0;
//int tilt_down = 0;
//int investigate = 0;
//int centered = 1;


// laser pin setup
int laserPin = 7;

//["background", "aeroplane", "bicycle", "bird", "boat",
//        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
//        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
//        "sofa", "train", "tvmonitor"]

// defines ultrasonic pin numbers
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
const int leftTrigPin = 40;
const int leftEchoPin = 41;
const int rightTrigPin = 38;
const int rightEchoPin = 39;

// defines distance time variables
long fDuration;
long lFDuration;
long rFDuration;
long aDuration;
long cDuration;
long lDuration;
long rDuration;
int fDistance;
int lFDistance;
int rFDistance;
int aDistance;
int cDistance;
int lDistance;
int rDistance;

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

// Ultrasonic distance tresholds
float maxDist = 150.00;
float mi1Dist = 110.00;
float mi2Dist = 70.00;
float minDist = 40.00;

// Built in motor movements
String move_fwd_full = "1-0-200-0-0-200-00";
String move_fwd_mi1 = "1-0-180-0-0-180-00";
String move_fwd_mi2 = "1-0-160-0-0-160-00";
String move_fwd_close = "1-0-140-0-0-140-00";

String reverse = "0-0-130-1-0-200-700";
String all_stop = "1-0-000-0-0-000-00";

String spin_right = "1-0-230-1-0-100-250";
String spin_left = "0-0-100-0-0-230-250";

String spin_right_2 = "1-0-230-1-0-175-250";
String spin_left_2 = "0-0-175-0-0-230-250";

String turn_right = "1-0-230-1-0-230-250";
String turn_left = "0-0-230-0-0-230-250";

void setup() {
    // initialize i2c as slave
    Wire.begin(SLAVE_ADDRESS);

    // define callbacks for i2c communication
    Wire.onReceive(receiveEvent);
    Serial.begin(9600); // Starts the serial communication

    pinMode(fwdTrigPin, OUTPUT);  // Sets the trigPin as an Output
    pinMode(fwdEchoPin, INPUT);   // Sets the echoPin as an Input
    pinMode(lFwdTrigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(lFwdEchoPin, INPUT);  // Sets the echoPin as an Input
    pinMode(rFwdTrigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(rFwdEchoPin, INPUT);  // Sets the echoPin as an Input
    pinMode(aftTrigPin, OUTPUT);  // Sets the trigPin as an Output
    pinMode(aftEchoPin, INPUT);   // Sets the echoPin as an Input
    pinMode(camTrigPin, OUTPUT);  // Sets the trigPin as an Output
    pinMode(camEchoPin, INPUT);   // Sets the echoPin as an Input
    pinMode(leftTrigPin, OUTPUT);  // Sets the trigPin as an Output
    pinMode(leftEchoPin, INPUT);   // Sets the echoPin as an Input
    pinMode(rightTrigPin, OUTPUT);  // Sets the trigPin as an Output
    pinMode(rightEchoPin, INPUT);   // Sets the echoPin as an Input

    // Camera pan and tilt setup
    servo1.attach(servoPinPan);
    servo1.write(panAngle);
    servo2.attach(servoPinTilt);
    servo2.write(tiltAngle); 


    // laser output 
    pinMode(laserPin, OUTPUT);

    initial_start_up = true;
    set_auto = false;
    pan_left = false;
    pan_right = false;
    tilt_up = false;
    tilt_down = false;
    investigate = false;
    pan_cent = true;
    tilt_cent = true;
    
//    startMillis = millis();  //initial start time
}

void loop() {  

    if (receiveFlag == true) {
//        float forD = get_fwd_distance();
//        float forL = get_left_fwd_distance();
//        float forR = get_right_fwd_distance();
//        float aftD = get_aft_distance();
//        float camD = get_cam_distance();
//        float leftD = get_left_distance();
//        float rightD = get_right_distance();
    
//        Serial.println(forD);
//        Serial.println(forL);
//        Serial.println(forR);
//        Serial.println(aftD);
//        Serial.println(camD);
//        Serial.println(leftD);
//        Serial.println(rightD);
        
        String phrase;
        phrase = String(phrase + temp);
        command = phrase.substring(0, 3).toInt();
        cv_data = phrase.substring(3, -1);
        Serial.print("In Command is ");
        Serial.println(command);
        
        if (initial_start_up == true) {
            Serial.println("System Initializing..");
//          set_auto = false;
        // Drive motor stoped
            Serial.println("Drive motor stopped");
//            set_to_manual();
       
            investigate = false;
            pan_cent = true;
            tilt_cent = true;
            initial_start_up = false;
        }
       
//        if (command == 7) {
//            set_to_manual();     

//            Serial.print("Investigate = ");
//            Serial.println(investigate);
//            Serial.print("Set_auto = ");
//            Serial.println(set_auto);
//            Serial.print("Command = ");
//            Serial.println(command);
        
//        }

      
        if (set_auto == false) {         
            Serial.print("Set_auto = ");
            Serial.println(set_auto);
            // Manual drive motor activated
            if (command == 7) {
               set_to_manual();            
            }  
                
            if (command == 6) {
                set_to_auto();
            }
    
            if (command == 2) {
                manual_drive_forward(); 
            } 
            
            if (command == 3) {
                manual_drive_reverse();
            }

            if (command == 4) {
                manual_drive_left();            
            }
    
            if (command == 5) {
                manual_drive_right();        
            }
    
            if (command == 8) {
                manual_tilt_down();            
            }
        
            if (command == 9) {
                manual_tilt_up();
            }


            if (command == 10) {
                manual_pan_right();
            }
    
            if (command == 11) {
                manual_pan_left();
            }
  
            // Pan camera servo center command
            if (command == 12) {
                manual_pan_to_center();
            }
    
            if (command == 13) {
                // Activate laser 
                laser_on();
            }
    
            if (command == 14) {
                // Deactivate laser
                laser_off();               
            }
  
            Serial.println("End of False loop");
        }
        receiveFlag = false;
    
    Serial.println(command);
//    if (command == 7) {
//            set_to_manual();                 
//    }
                
    if (set_auto == true) { 
      
        Serial.print("Auto mode = ");
        Serial.println(set_auto);
        if (receiveFlag == true) {                      
            if (command == 7) {
                set_to_manual();                 
            }
    
            if (command == 20) {
                set_investigate_on();
            }
            receiveFlag == false;
        }
    

        if (investigate == true) { 
            parse_cv_data(cv_data);     
            Serial.print("Investigate = ");
            Serial.println(investigate);
            // Runs the auto investigate. Center bounding box in camera view
            // Pan left from 140 to 35 degrees pan > 35 -- Pan right from 35 to 140 degrees pan < 140 ++
               
            Serial.println("Beginning object investigation...");                       
            // Now we have bounding box x and y positions mid_width and mid_height will either be bigger 
            // or smaller meaning left or right of center of the bounding box. Now cx and cy are centers of the box
            check_center();                      
//                Now center camera if necessary                                                                
            if (pan_cent == false) {
                pan_center();   
            } else if (tilt_cent == false) {
                tilt_center();
            } else {
                investigate_maneuver();
            }        
             
//            if (command == 7) {
//                set_to_manual();
//            }
        } 
        
        if (investigate == false) {
            Serial.print("Investigate = ");
            Serial.println(investigate);
            search_maneuver(); 
//            receiveFlag = false;
            
//            if (command == 7) {
//               set_to_manual();            
//            }             
        }
        
 
        }
    }
    receiveFlag = false;
//    main_loop_counter+=1;
//    currentMillis = millis();  //get the current time 
//    Serial.print("Loop time is ");
//    Serial.println(currentMillis - startMillis);
//    Serial.print("Main Loop counter is now ");
//    Serial.println(main_loop_counter);
//    startMillis = currentMillis;   
}

void manual_drive_forward() {   
    // Drive motor activated forward
    Serial.println("Manual forward");
    direction_L = 1;
    brake_L = 0;
    speed_L = 230;
    direction_R = 0;
    brake_R = 0;
    speed_R = 230;
    runTime = 0;

    motorControl(direction_L, brake_L, speed_L, direction_R, brake_R, speed_R, runTime);
    receiveFlag = false;
}

void manual_drive_reverse() {
    // Drive motor activated reverse
    Serial.println("Manual reverse");
    direction_L = 0;
    brake_L = 0;
    speed_L = 130;
    direction_R = 1;
    brake_R = 0;
    speed_R = 200;
    runTime = 0;
    motorControl(direction_L, brake_L, speed_L, direction_R, brake_R, speed_R, runTime);
    receiveFlag = false;
}

void manual_drive_left() {             
    // Drive motor activated left
    Serial.println("Manual left");
    direction_L = 0;
    brake_L = 0;
    speed_L = 150;
    direction_R = 0;
    brake_R = 0;
    speed_R = 150;
    runTime = 0;
    
    motorControl(direction_L, brake_L, speed_L, direction_R, brake_R, speed_R, runTime);
    receiveFlag = false;
}

void manual_drive_right() {
    // Drive motor activated right
    Serial.println("Manual right");
    direction_L = 1;
    brake_L = 0;
    speed_L = 150;
    direction_R = 1;
    brake_R = 0;
    speed_R = 150;
    runTime = 0;
  
    motorControl(direction_L, brake_L, speed_L, direction_R, brake_R, speed_R, runTime);
  //                command = 0;
    receiveFlag = false;
}

void manual_tilt_down() {
    // Tilt down
    Serial.println("Manual tilt down");
    if (tiltAngle < 97) {
        tiltAngle+=8;
        servo2.write(tiltAngle); 
    }                 
    receiveFlag = false;
}

void manual_tilt_up() {
    // Tilt up
    Serial.println("Manual tilt up");
    if (tiltAngle > 8) {
        tiltAngle-=8;
        servo2.write(tiltAngle);
    }
    receiveFlag = false; 
}

void manual_pan_left() {
    // Pan camera servo left command
    // Pan left from 140 to 35 degrees pan
    Serial.println("Manual pan left");
    if (panAngle > 43) {
         panAngle-=8;

         servo1.write(panAngle);
    }
    receiveFlag = false;
}

void manual_pan_right() {
    // Pan camera servo right command
    // Pan right from 35 to 140 degrees pan
    Serial.println("Manual pan right");
    Serial.println(panAngle);
    if (panAngle < 132) {
        panAngle+=8;
        servo1.write(panAngle);
    }
    receiveFlag = false;
}

void manual_pan_to_center() {
    // Pan center 110, Tilt center 90
    Serial.println("Manual Center cameras");
    panAngle = 80;
    tiltAngle = 95;
    servo1.write(panAngle);
    servo2.write(tiltAngle);
    receiveFlag = false;                            
}

void laser_on () {
    // Activate laser
    Serial.println("Manual laser on"); 
    digitalWrite(laserPin, HIGH);
    receiveFlag = false;
}

void laser_off () {
    // Deactivate laser
    Serial.println("Manual laser off");
    digitalWrite(laserPin, LOW);
    receiveFlag = false;                
}

void set_to_auto() {
    Serial.println("Auto mode activated");
    set_auto = true;
    pan_cent = true;
    tilt_cent = true;                    
    investigate = false;
    cx = 200;
    cy = 150;
    manual_pan_to_center();
    receiveFlag = false;
}

void set_to_manual() {
    Serial.println("Manual mode activated");
    set_auto = false;
    pan_cent = true;
    tilt_cent = true;
    investigate = false;
    // Drive motor stoped
    direction_L = 1;
    brake_L = 1;
    speed_L = 000;
    
    direction_R = 0;
    brake_R = 1;
    speed_R = 000;
    runTime = 1;

    motorControl(direction_L, brake_L, speed_L, direction_R, brake_R, speed_R, runTime);
    
    pan_cent = true;
    tilt_cent = true;                    
    investigate = false;
    cx = 200;
    cy = 150;

    receiveFlag = false;
}

void set_investigate_on() {
    Serial.println("Investigate mode activated");
    investigate = true;
     receiveFlag = false;      
}

void set_investigate_off() {
    Serial.println("Investigate mode deactivated");
    pan_cent = true;
    tilt_cent = true;
    investigate = false;
    cx = 200;
    cy = 150;
//    command = "";
    receiveFlag = false;
//    Serial.print("Pan_cent = ");
//    Serial.println(pan_cent);
//    Serial.print("Tilt_cent = ");
//    Serial.println(tilt_cent);                    
//    Serial.print("investigate = ");
//    Serial.println(investigate);
//    Serial.print("Center x = ");
//    Serial.println(cx);
//    Serial.print("Center y = ");
//    Serial.println(cy);
}

void search_maneuver() {
   
//    delayMicroseconds(1000);
    pan_cent = true;
    tilt_cent = true;                    
    investigate = false;
    cx = 200;
    cy = 150;
    Serial.print("Hey get moving we're on the clock!!!"); 
    maneuver();
    
    if (command == 7) {
       set_to_manual();            
    }
}
    
void investigate_maneuver() {
    return;
}

void investigate_reset() {
    Serial.println("Investigate mode deactivated");
    pan_cent = true;
    tilt_cent = true;
    investigate = false;
    cx = 200;
    cy = 150;
//    command = "";
    receiveFlag = false;
//    Serial.print("Pan_cent = ");
//    Serial.println(pan_cent);
//    Serial.print("Tilt_cent = ");
//    Serial.println(tilt_cent);                    
//    Serial.print("investigate = ");
//    Serial.println(investigate);
//    Serial.print("Center x = ");
//    Serial.println(cx);
//    Serial.print("Center y = ");
//    Serial.println(cy);
}

void tilt_center() {
    Serial.print("Tilt centered = ");
    Serial.println(tilt_cent);
    Serial.println("Now tilt to center object in view");                    
    if (tilt_up == true) {
        if (cy < mid_height - 10) {
            if (tiltAngle > 0) {
                tiltAngle-=2;
                servo2.write(tiltAngle);  
                Serial.println("Tilting up");
                delayMicroseconds(15);
            }                                           
        }
    } else if (tilt_down == true) {
        if (cy > mid_height + 10) { 
            if (tiltAngle < 105) {
                tiltAngle+=2;    
                servo2.write(tiltAngle);  
                Serial.println("Tilting down"); 
                delayMicroseconds(15);
            }
        }                                                      
    } else {
        tilt_cent = true;                                                    
    }
}

void pan_center() {
    Serial.print("Pan centered = ");
    Serial.println(pan_cent);
    Serial.println("Now pan to center object in view");
    if (pan_left == true) {
        if (cx > mid_width + 10) {
            if (panAngle > 35) {
                panAngle-=2;
                servo1.write(panAngle); 
                Serial.println("Panning Left");
                delayMicroseconds(15);                                
            } 
        }
    } else if (pan_right == true) {
        if (cx < mid_width - 10) {
            if (panAngle < 140) {
                panAngle+=2;
                servo1.write(panAngle);
                Serial.println("Panning Right");
                delayMicroseconds(15);
            }                     
        }
    } else {
        pan_cent = true;                                                    
    }
}


void check_center() { 
    Serial.println("Check centered position");
    Serial.print("Cx = ");                        
    Serial.println(cx);
    
    if (cx < mid_width - 10) {
        pan_cent = false;
        pan_left = true;
        pan_right = false;
        Serial.println("pan_left");
  
    } else if (cx > mid_width + 10) {
        pan_cent = false;
        pan_right = true;
        pan_left = false;
        Serial.println("pan_right");
    } else {
        pan_cent = true;
    }   
    if (cy < mid_height - 10) {
        tilt_cent = false;
        tilt_up = true;
        tilt_down = false;
        Serial.println("tilt_up");
    } else if (cy > mid_height + 10) {
        tilt_cent = false;
        tilt_down = true;
        tilt_up = false;
        Serial.println("tilt_down");
    } else {
        tilt_cent = true;
    }
}
 
int parse_cv_data(String cv_data) {
    Serial.println("Parse string data");
    x1 = cv_data.substring(0, 3).toInt();
    y1 = cv_data.substring(3, 6).toInt();
    x2 = cv_data.substring(6, 9).toInt();
    y2 = cv_data.substring(9, 12).toInt();
//    percent = atof(cv_data.substring(12, 17));
    item = cv_data.substring(17,20).toInt();
    trigger = cv_data.substring(20,23).toInt();
    confirm = cv_data.substring(23, -1).toInt();
//    Serial.print("x1 = ");
//    Serial.println(x1);
//    Serial.print("y1 = ");
//    Serial.println(y1);
//    Serial.print("x2 = ");
//    Serial.println(x2);
//    Serial.print("y1 = ");
//    Serial.println(y2);
//    Serial.print("Item no = ");
//    Serial.println(item);
//    Serial.print("Trigger val = ");
//    Serial.println(trigger);
//    Serial.print("Confirmed = ");
//    Serial.println(confirm);
    box_width = x2 - x1;
    box_height = y2 - y1;
    left_width = (width - box_width)/2;
    top_height = (height - box_height)/2;
    
    cx = (box_width / 2) + x1;
    if (cx == 0) {
        cx = 200;
    }
    cy = (box_height / 2) + y1;
    if (cy == 0) {
        cy = 150;
    }
    Serial.print("Cx = ");
    Serial.println(cx);
    Serial.print("Cy = ");
    Serial.println(cy);
//    command == "000";
//    cv_data = "";
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
    fDistance = (fDuration / 2) / 29.1;

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
    lFDistance = (lFDuration / 2) / 29.1;

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
    rFDistance = (rFDuration / 2) / 29.1;

    // Prints the distance on the Serial Monitor
    Serial.print("Right Fwd Distance: ");
    Serial.println(rFDistance);

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
    aDistance = (aDuration / 2) / 29.1;

    // Prints the distance on the Serial Monitor
    Serial.print("Aft Distance: ");
    Serial.println(aDistance);

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
    cDistance = (cDuration / 2) / 29.1;

    // Prints the distance on the Serial Monitor
     Serial.print("Cam Distance: ");
     Serial.println(cDistance);

    return cDistance;
}

float get_left_distance() {
    // Clears the trigPin
    digitalWrite(leftTrigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(leftTrigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(leftTrigPin, LOW);
    delayMicroseconds(2);

    // Reads the echoPin, returns the sound wave travel time in microseconds
    lDuration = pulseIn(leftEchoPin, HIGH);

    // Calculating the distance
    lDistance = (lDuration / 2) / 29.1;

    // Prints the distance on the Serial Monitor
    Serial.print("Left Distance: ");
    Serial.println(lDistance);

    return lDistance;
}

float get_right_distance() {
    // Clears the trigPin
    digitalWrite(rightTrigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(rightTrigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(rightTrigPin, LOW);
    delayMicroseconds(2);

    // Reads the echoPin, returns the sound wave travel time in microseconds
    rDuration = pulseIn(rightEchoPin, HIGH);

    // Calculating the distance
    rDistance = (rDuration / 2) / 29.1;

    // Prints the distance on the Serial Monitor
    Serial.print("right Distance: ");
    Serial.println(rDistance);

    return rDistance;
}

void motorControl(int direction_L, int brake_L, int speed_L, int direction_R, int brake_R, int speed_R, int runTime) {

    //Motor A forward full speed
    digitalWrite(12, direction_L); // Establishes forward direction of Motor A
    digitalWrite(9, brake_L);      // Disengage the Brake for Motor A
    analogWrite(3, speed_L);       // Spins the motor on Motor A at full speed

    //Motor B forward full speed
    digitalWrite(13, direction_R); // Establishes forward direction of Motor B
    digitalWrite(8, brake_R);      // Disengage the Brake for Motor B
    analogWrite(11, speed_R);      // Spins the motor on Motor B at full speed

    delay(runTime);
}

void receiveEvent(int howMany) {
    //    Serial.print(howMany);
    for (int i = 0; i < howMany; i++) {
        temp[i] = Wire.read();
        temp[i + 1] = '\0'; // Add null after each char
    }

    //RPi first byte is cmd byte so shift everything to the left 1 pos so temp contains string
    for (int i = 0; i < howMany; i++) {
        temp[i] = temp[i + 1];
    }

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

void turn_choice() {
    Serial.println("Turn choice");
    float forL = get_left_fwd_distance();
    float forR = get_right_fwd_distance();
    float leftD = get_left_distance();
    float rightD = get_right_distance();

//         if (forL < 50 || leftD < 30) {
//                move_command(spin_right);
//            } else if (forR < 50 || rightD < 30) {
//                move_command(spin_left);
//            }
    if (forL < forR || leftD < rightD) {
        if (forL < 30.00 || leftD < 30.00) {
            move_command(spin_right_2);
        } else if (forL < 70.00 || leftD < 70.00) {
            move_command(spin_right);
        }
    } else if (forR <= forL || rightD <= leftD) {
        if (forR < 30.00 || rightD < 30.00) {
            move_command(spin_left_2);
        } else if (forR < 70.00 || rightD < 70.00) {
            move_command(spin_left);
        }
    }   
}

void move_forward() {
    Serial.println("Forward reverse choice");
    float forD = get_fwd_distance();
    float camD = get_cam_distance();
    if (forD > 1000 || camD > 1000) {
        if (forD > 1000) {
            Serial.println("Sensor ERROR: forward ultrasonic sensor distance is over 600");
        }
        if (camD > 1000) {
            Serial.println("Sensor ERROR: forward ultrasonic sensor distance is over 600");
        }
        move_forward();

    } else if (forD > maxDist && camD > maxDist) {
        Serial.println("Max Distance -- Forward full speed");
        move_command(move_fwd_full);
        // break;
    } else if ((forD > mi1Dist && forD < maxDist) && (camD > mi1Dist && camD < maxDist)) {
        Serial.println("Mid 1 Range -- Forward Mid 1 speed");
        move_command(move_fwd_mi1);
        // break;
    } else if ((forD > mi2Dist && forD < mi1Dist) and (camD > mi2Dist && camD < mi1Dist)) {
        Serial.println("Mid 2 Range -- Forward Mid 2 speed");
        move_command(move_fwd_mi2);
        // break;
    } else if ((forD > minDist && forD < mi1Dist) && (camD > minDist && camD < mi1Dist)) {
        Serial.println("Min Distance -- Forward close speed");
        move_command(move_fwd_close);
        // break;
    } else if ((forD < minDist) && (camD < minDist)) {
        Serial.println("Stopping");
        move_command(all_stop);
    }


}

void check_aft_distance() {
    Serial.println("check aft");
    float aftD = get_aft_distance();
    if (aftD < minDist) {
        turn_choice();
    } else {
        move_command(reverse);
    }
}

bool okToMoveFwd() {
    float forD = get_fwd_distance();
    if (forD < minDist) {
      return false;  
    } else {
      return true;
    }
}

bool okToMoveBack() {
  float aftD = get_aft_distance();
  if (aftD < minDist) {
    return false;
  } else {
    return true;
  }
}

void check_fwd_distance() {
    Serial.println("check forward");
    float forD = get_fwd_distance();
    if (forD < minDist) {
        turn_choice();
    } else {
        move_command(reverse);
    }
}

void maneuver() {


    float forD = get_fwd_distance();
    float forL = get_left_fwd_distance();
    float forR = get_right_fwd_distance();
    float camD = get_cam_distance();
    float leftD = get_left_distance();
    float rightD = get_right_distance();
    
//        Serial.println(forD);
//        Serial.println(forL);
//        Serial.println(forR);
//        Serial.println(aftD);
//        Serial.println(camD);
//        Serial.println(leftD);
//        Serial.println(rightD)
  
    Serial.println("First Test");
//    Serial.println(forD);
//    Serial.println(forL);
//    Serial.println(forR);
    if (okToMoveFwd()) {
       move_forward();
    } else {
       turn_choice();
    }

   
}


    
    
