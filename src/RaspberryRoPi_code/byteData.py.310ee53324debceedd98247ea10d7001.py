# -*- coding: utf-8 -*-

import smbus
import time

bus = smbus.SMBus(1)

# This is the I2C address setup in the Arduino Program
address = 0x18

def writeData(value):
    byteValue = StringToBytes(value)    
    bus.write_i2c_block_data(address,0x00,byteValue) # First byte is 0 = command byte
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

if __name__ == '__main__':
    main()
    
    

    
    
    

    
    
        
        
        

    
    
        
        
        
