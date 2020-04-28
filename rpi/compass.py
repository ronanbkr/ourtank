###############################################################
# by Johannes Kinzig                                          #
# PyCompass                                                   #
# reads in data from Arduino with Compass Module and          #
# displays the data graphical via tkinter and turtle         #
#                                                             #
# Version: 1.0                                                #
###############################################################

from turtle import *
import serial
from gyro import *

width = 300
height = 300
screen = Screen()
screen.setup(width, height)

###############################################################
#       Functions for the turtle graphics                    #
###############################################################

def Compass():
    
    hideturtle()
    tracer(0, 0) # switch off animation to build up compass fast!
    global compasspointer
    penup()
    right(90)
    forward(100)
    left(90)
    pendown()
    circle(100)
    penup()
    home()
    goto(105, -25)
    write("E", font=('Arial', 30, 'normal'), align="left")
    home()
    goto(0, 95)
    write("N", font = ('Arial', 30, 'normal'), align="center")
    home()
    goto(0, -140)
    write("S", font = ('Arial', 30, 'normal'), align="center")
    home()
    goto(-100, -25)
    write("W", font = ('Arial', 30, 'normal'), align="right")
    home()
    bgcolor("grey")
    compasspointer = Turtle()
    compasspointer.degrees(360) #make sure to use angle in degree, a circle has 360 degrees
    compasspointer.home()
    compasspointer.settiltangle(0)
    compasspointer.shape("triangle")
    compasspointer.color("Green")
    compasspointer.turtlesize(0.5, 7, 0)
    tracer(1, 1) # switch on animation, because compasspointer should turn
    compasspointer.speed(0)

###############################################################
#          Main programm Code                                 #
###############################################################

#Arduino = serial.Serial("/dev/ttyACM0)", baudrate = 9600) # serial device
Compass()

def main():
    
    
    while True:
        angle = getGyroData()
        angleA = angle[1][0]
        #print("A: ", angleA)

        angle = getGyroData()
        angleB = angle[1][0]
        #print("B: ", angleB)
        if angleB != angleA:
            angleA = angleB
        try:
            angle = Arduino.readline()
            angle = angle.strip()
            angle = int(angle)
            print(angle)
            compasspointer.settiltangle(angleA-90) #turtles' zero position is not North, its East. But 0 degree equals N. (+90)
      
        except:
            pass

if __name__ == '__main__':
    main()










