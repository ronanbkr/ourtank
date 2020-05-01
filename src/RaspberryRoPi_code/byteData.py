# -*- coding: utf-8 -*-

import smbus
import time

bus = smbus.SMBus(1)

previous_command = "000"

# This is the I2C address setup in the Arduino Program
address = 0x18

def writeData(value):
    global previous_command
    byteValue = StringToBytes(value) 
    new_command = value[0:3]
    bus.write_i2c_block_data(address,0x00,byteValue) # First byte is 0 = command byte
    #if new_command != previous_command:
        # look at last command if the same delay and send
        # if different send   
    #    bus.write_i2c_block_data(address,0x00,byteValue) # First byte is 0 = command byte
    #    previous_command = new_command
    #else:
    #    time.sleep(1)
    #    previous_command = "000"
    time.sleep(.1)
    return -1

def StringToBytes(val):
    retVal = []
    
    for c in val:
        retVal.append(ord(c))
    return retVal


auto_mode = ''
def send_command(command):
    global auto_mode
    if command[:3]=='007':
        auto_mode = False 
    elif command[:3] =='006':
        auto_mode = True 
    if command[:3]=='020' and auto_mode==True:
        startTime = time.time()
        #time.sleep(.1)
        print("Sendind Command", command)
        
        writeData(command)
        time.sleep(.1)
    elif command[:3] != '020':
        startTime = time.time()
        #time.sleep(.1)
        print("Sending Command", command)
        
        writeData(command)
        time.sleep(.1)
        
    print("Auto mode is ",auto_mode)

if __name__ == '__main__':
    main()
    
    
    

    
    
        
        
        
