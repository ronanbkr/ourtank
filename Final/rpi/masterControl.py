# -*- coding: utf-8 -*-

import smbus
import time
from random import randint
from altitude import *
#from ultrasonic_threading import *
from lazer import *

bus = smbus.SMBus(1)

max_dist = 150.00
mid_dist = 100.00
min_dist = 60.00

move_fwd_full = "001-1-0-255-0-0-255-00"
move_fwd_half = "001-1-0-150-0-0-150-00"
move_fwd_close = "001-1-0-120-0-0-120-00"

all_stop = "001-1-0-000-0-0-000-00"

spin_right = "001-1-0-175-1-0-175-1000"
spin_left = "001-0-0-175-0-0-175-1000"

turn_right = "001-1-0-125-1-0-125-00"
turn_left = "001-0-0-125-0-0-125-00"

start_time = time.time()
freq = 20
time_gap = 1/freq

autonomous = True
#state = "all_stop"
#newstate = "all_stop"
#wait_count = 0

# This is the address we setup in the Arduino Program
address = 0x18

# http://www.raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
def writeData(value):
    byteValue = StringToBytes(value)    
    bus.write_i2c_block_data(address,0x00,byteValue) # first byte is 0=command byte
    return -1

def StringToBytes(val):
    retVal = []
    for c in val:
        retVal.append(ord(c))
    return retVal

def send_command(command):
    startTime = time.time()
    time.sleep(.1)
    print("Sending Command", command)
    
    writeData(command)
    time.sleep(.1)

def main():
    state = "all_stop"
    newstate = "all_stop"
    wait_count = 0
    
#    fwd_distance = UltrasonicSensors(1, "Forward Sensor", float(get_fwd_distance()))
#    fwd_left_distance = UltrasonicSensors(2, "Fwd Left Sensor", float(get_fwd_left_distance()))
#    fwd_right_distance = UltrasonicSensors(3, "Fwd Right Sensor", float(get_fwd_right_distance()))
#    aft_distance = UltrasonicSensors(4, "Aft Sensor", float(get_aft_distance()))

    
#    fwd_distance.start()
#    fwd_left_distance.start()
#    fwd_right_distance.start()
#    aft_distance.start() 
    
    while autonomous == True:
        try:                       
            if time.time() - start_time > time_gap:
                print(state)
                fwd_distance = float(get_fwd_distance())
                fwd_left_distance = float(get_fwd_left_distance())
                fwd_right_distance = float(get_fwd_right_distance())
                aft_distance = float(get_aft_distance())
                    
                #fwd_dist = float(get_fwd_distance())
                
                if fwd_distance < min_dist:
                    print("Less than ", min_dist, " All_stop")
                    print("Distance ", fwd_distance)
                    newstate = all_stop
                    
                    
                    
                    if newstate == all_stop and wait_count < 3:
                        wait_count+=1
                        print("Waiting ", wait_count)
                        
                    elif newstate == all_stop and wait_count == 3:
                
                        #fwd_distance = float(get_fwd_distance())
                        #fwd_left_dist = float(get_fwd_left_distance())
                        #fwd_right_dist = float(get_fwd_right_distance())
                
                        if fwd_distance + fwd_left_distance > fwd_distance + fwd_right_distance:
                            # Turn Left
                            print("Turn Left")
                            send_command(spin_left)
                        else:
                            # Turn Right
                            print("Turn Right")
                            send_command(spin_right)
                    
                
                elif fwd_distance < mid_dist and fwd_distance > min_dist:
                    print("Between ", min_dist, " and ", mid_dist, ": Close Speed")
                    print("Distance ", fwd_distance)
                    newstate = move_fwd_close

                elif fwd_distance > mid_dist and fwd_distance < max_dist:
                    print("Between ", mid_dist, " and ", max_dist, ": Half Speed")
                    print("Distance ", fwd_distance)
                    newstate = move_fwd_half

                
                elif fwd_distance > max_dist:
                    print("Greater than ", max_dist, ": Full Speed")
                    print("Forward Distance: ", fwd_distance)
                    newstate = move_fwd_half
                            
                if newstate != state:
                    state = newstate
                    print("Command Change")
                    wait_count = 0
                    send_command(state)
            
                                    
        except IOError:
            continue
                
    
if __name__ == '__main__':
    main()
    
    
    

    
    
        
        
        
