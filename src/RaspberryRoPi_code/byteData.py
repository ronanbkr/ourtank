# -*- coding: utf-8 -*-

import smbus
import time
from globals2 import auto_mode

bus = smbus.SMBus(1)
 
send_count = 0
max_send = 10

# This is the I2C address setup in the Arduino Program
address = 0x18

def writeData(value):
    byteValue = StringToBytes(value) 
    bus.write_i2c_block_data(address,0x00,byteValue) # First byte is 0 = command byte
    time.sleep(.1)
    return -1

def StringToBytes(val):
    retVal = []
    
    for c in val:
        retVal.append(ord(c))
    return retVal

def send_command(command):
    print("byteData command: ", command)
    
    if command[0:3] == '007':
        print("STOP")
        writeData(command)

    if command[0:3] == '006':
        print("AUTO")
        writeData(command)
        
    
    if command[0:3] == '020':
        global send_count
        send_count+=1
                    
        if send_count == max_send: 
            print("Sending investigate Command", command)
            writeData(command)
            time.sleep(.1)
            send_count = 0
        
        if send_count > max_send:
            send_count = 0
        
    elif command[0:3] in ['002', '003', '004', '005', '008', '009', '010', '011', '012', '013', '014', '015', '016', '017', '018', '019']:
        print("Sending alternate Command", command)
        
        writeData(command)
        time.sleep(.1)

if __name__ == '__main__':
    main()
    
    
    

    
    
        
        
        
