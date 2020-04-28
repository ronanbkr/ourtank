# School of Computing &mdash; Year 4 Project Proposal Form


## SECTION A

|                     |                     |
|---------------------|---------------------|
|Project Title:       | RAMP                |
|Student 1 Name:      | Ronan Barker        |
|Student 1 ID:        | 16733535            |
|Student 2 Name:      | Alanna Carton       |
|Student 2 ID:        | 16304366            |
|Project Supervisor:  | Alistair Sutherland |


## SECTION B


### Introduction

 Our project is based on Arduino and Raspberry PI. We Plan use an arduino as a data collection device by fitting it with multiple sensors such as GPS, barometric, ultrasonic distance and temperature sensors.
  
 We plan to connect 4 cameras to a Raspberry PI, Two day and two night. We will then use the images taken from these cameras and process it in conjunction with the sensor data to produce accurate mapping of the area.

 It is our aim to then mount these devices to a remote controlled vehicle which will send data back to the controller of the unit.


### Outline

  We are planning on building an arduino and raspberry pi based data collection vehicle with mounted sensors. We plan on using image processing and information from sensors such as distance sensors to firstly map the area then use this data if time allows to make the remote controlled vehicle autonomous so it can decide itself the best navigation route to take.

### Background

 We decided we wanted to create something to physically interact with the real world. The Arduino and Raspberry PI are ideal ways to learn about and create these things. We decided upon a moving platform with sensors and cameras as we thought that would prove to be a good balance between opportunities to learn about new technologies such as the Neural compute stick and Arduino and also to have fun with these technologies as this will keep us engaged with the project long term.

### Achievements

 The function of our project is to produce a small sensor fitted vehicle to gather location based data from which it can map a given area and relay that information back to a control unit which will process the data and then decide on the next course of action.
 
 The users of the project would be anyone who finds themselves either with a difficult to access area or where this area could be hazardous to their health and safety. 

 The applications are limitless from search and rescue (SAR) for earthquake and disaster searches, to mine mapping, archaeology exploration or dependant on the vehicle fitted to for example a drone can be used to carry out maintenance inspections on wind farms solar farms or oil rigs.


### Justification

 In hostile environments or where there is a danger to individuals responsible to maintain structures such as wind turbines, oil rigs, mines or even in the case of natural disasters the ability to remotely inspect these items/areas is crucial. Our project will provide the basic platform to carry out many of these tasks. 

### Programming language(s)

 Our project will involve the following computing languages: 
 * Python - Raspberry Pi 
 * C++     - Arduino 
 

### Programming tools / Tech stack

 We will be using Intellij as our development IDE.
 The Arduino IDE for C++

 OpenVINO is the toolkit for the Intel neural compute stick to process the image data.

 AWS server to store the collected data to be used for processing. TBC



### Hardware

 Non-standard components used will be:
 * Raspberry PI and attached cameras.
 * Arduino and attached sensors.
 * Intel Neural Compute stick 2 to deploy our neural network for the Raspberry Pi.



### Learning Challenges

 C++ will be one of the new languages we will be required to learn to interact with the Arduino. We will need to learn how to control the Arduino from a Raspberry PI. 
 
 We will have to learn how to use the neural compute stick to build our neural network for image processing and how to use this data in conjunction with al the other sensors which will be available on the unit.
 
 We may be required to learn how to deploy an AWS server to carry out our main processing if the computing power of the Raspberry Pi is not powerful enough. 



### Breakdown of work

#### Student 1

 *Ronan Barker 16733535*
 
 Will take ownership of the Raspberry Pi connectivity to the Arduino.
 
 The initial task will be to get all sensors correctly connected to the Arduino so that the data can be relayed and processed. Also the mobile unit will need to be built and coded before the autonomous system can be introduced.


#### Student 2

 *Alanna Carton 16304366*
 
 Will take ownership of the Raspberry Pi connectivity to the Camera bank and the Neural compute stick for the neural network.The initial task here will be to connect the camera to the Raspberry Pi and be able to send the data to the neural compute stick where it can then be processed by the neural network.

#### Student 1 & Student 2

 Once these two tasks have been completed satisfactorily the two seperate systems will be brought together to be mounted to the remote controlled vehicle. We will then work on the integration of these systems and the server side together to complete the project. 


