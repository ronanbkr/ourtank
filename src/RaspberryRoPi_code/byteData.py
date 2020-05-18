# -*- coding: utf-8 -*-

import smbus
import time

bus = smbus.SMBus(1)
 
send_count = 0
max_send = 8
command_list = ['002', '003', '004', '005', '008', '009', '010', '011', '012', '013', '014', '015', '016', '017', '018', '019', "021", "022", "023", "024"]

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
    global command_list
    if command[0:3] == '007':
        print("Manual")
        print("byteData command: ", command)
        writeData(command)
        time.sleep(.1)
        command = ""
    
    if command[0:3] == '006':
        print("AUTO")
        print("byteData command: ", command)
        writeData(command)
        time.sleep(.1)
        command = ""
        
    if command[0:3] == '020':
        print("Sending investigate Command", command)            
        writeData(command)
        time.sleep(.1)
        command = ""
        
    elif command[0:3] in command_list:
        print("Sending manual command", command)        
        writeData(command)
        command = ""
        time.sleep(.1)

if __name__ == '__main__':
    main()
    
    
    

    
    
        
        
        
