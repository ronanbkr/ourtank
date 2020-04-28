# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MPL3115A2
# This code is designed to work with the MPL3115A2_I2CS I2C Mini Module available from ControlEverything.com.
# https://shop.controleverything.com/products/precision-altimeter-500-to-1100-mbar#tabs-0-product_tabset-2

#from MPL3115A2 import MPL3115A2
#mpl3115a2 = MPL3115A2()

import smbus
import time
 
# Get I2C bus
bus = smbus.SMBus(1)

#sensor.sealevel_pressure = 103800
 
# I2C address of the device
DEFAULT_ADDRESS         = 0x60
 
# MPL3115A2 Regster Map
REG_STATUS              = 0x00 # Sensor status Register
REG_PRESSURE_MSB        = 0x01 # Pressure data out MSB
REG_PRESSURE_CSB        = 0x02 # Pressure data out CSB
REG_PRESSURE_LSB        = 0x03 # Pressure data out LSB
REG_TEMP_MSB            = 0x04 # Temperature data out MSB
REG_TEMP_LSB            = 0x05 # Temperature data out LSB
REG_DR_STATUS           = 0x06 # Data Ready status registe
OUT_P_DELTA_MSB         = 0x07 # Pressure data out delta MSB
OUT_P_DELTA_CSB         = 0x08 # Pressure data out delta CSB
OUT_P_DELTA_LSB         = 0x09 # Pressure data out delta LSB
OUT_T_DELTA_MSB         = 0x0A # Temperature data out delta MSB
OUT_T_DELTA_LSB         = 0x0B # Temperature data out delta LSB
REG_WHO_AM_I            = 0x0C # Device Identification Register
PT_DATA_CFG             = 0x13 # PT Data Configuration Register
CTRL_REG1               = 0x26 # Control Register-1
CTRL_REG2               = 0x27 # Control Register-2
CTRL_REG3               = 0x28 # Control Register-3
CTRL_REG4               = 0x29 # Control Register-4
CTRL_REG5               = 0x2A # Control Register-5
 
# MPL3115A2 PT Data Configuration Register
PT_DATA_CFG_TDEFE       = 0x01 # Raise event flag on new temperature data
PT_DATA_CFG_PDEFE       = 0x02 # Raise event flag on new pressure/altitude data
PT_DATA_CFG_DREM        = 0x04 # Generate data ready event flag on new pressure/altitude or temperature data
 
# MPL3115A2 Control Register-1 Configuration
CTRL_REG1_SBYB          = 0x01 # Part is ACTIVE
CTRL_REG1_OST           = 0x02 # OST Bit ACTIVE
CTRL_REG1_RST           = 0x04 # Device reset enabled
CTRL_REG1_OS1           = 0x00 # Oversample ratio = 1
CTRL_REG1_OS2           = 0x08 # Oversample ratio = 2
CTRL_REG1_OS4           = 0x10 # Oversample ratio = 4
CTRL_REG1_OS8           = 0x18 # Oversample ratio = 8
CTRL_REG1_OS16          = 0x20 # Oversample ratio = 16
CTRL_REG1_OS32          = 0x28 # Oversample ratio = 32
CTRL_REG1_OS64          = 0x30 # Oversample ratio = 64
CTRL_REG1_OS128         = 0x38 # Oversample ratio = 128
CTRL_REG1_RAW           = 0x40 # RAW output mode
CTRL_REG1_ALT           = 0x80 # Part is in altimeter mod
CTRL_REG1_BAR           = 0x00 # Part is in barometer mode
 
#class MPL3115A2():
def control_alt_config():
    """Select the Control Register-1 Configuration from the given provided value"""
    CONTROL_CONFIG = (CTRL_REG1_SBYB | CTRL_REG1_OS128 | CTRL_REG1_ALT)
    bus.write_byte_data(DEFAULT_ADDRESS, CTRL_REG1, CONTROL_CONFIG)
    #return

def data_config():
    """Select the PT Data Configuration Register from the given provided value"""
    DATA_CONFIG = (PT_DATA_CFG_TDEFE | PT_DATA_CFG_PDEFE | PT_DATA_CFG_DREM)
    bus.write_byte_data(DEFAULT_ADDRESS, PT_DATA_CFG, DATA_CONFIG)
    #return

def read_alt_temp():
    """Read data back from MPL3115A2_REG_STATUS(0x00), 6 bytes
    status, tHeight MSB, tHeight CSB, tHeight LSB, temp MSB, temp LSB"""
    data = bus.read_i2c_block_data(DEFAULT_ADDRESS, REG_STATUS, 6)

    # Convert the data to 20-bits
    #tHeight = ((data[1] * 24) + (data[2] * 16) + (data[3] & 0xF0)) / 8
    tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
    temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16

    altitude = tHeight / 7.5
    cTemp = temp / 16.0
    fTemp = cTemp * 1.8 + 32

    return {'a' : altitude, 'c' : cTemp, 'f' : fTemp}

def control_pres_config():
    """Select the Control Register-1 Configuration from the given provided value"""
    CONTROL_CONFIG = (CTRL_REG1_SBYB | CTRL_REG1_OS128)
    bus.write_byte_data(DEFAULT_ADDRESS, CTRL_REG1, CONTROL_CONFIG)
    #return

def read_pres():
    """Read data back from MPL3115A2_REG_STATUS(0x00), 4 bytes
    status, pres MSB, pres CSB, pres LSB"""
    data = bus.read_i2c_block_data(DEFAULT_ADDRESS, REG_STATUS, 4)

    # Convert the data to 20-bits
        
    pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
    #print(pres)
    pressure = pres / 1000.0

    return {'p' : pressure}
 
def startUp():
    control_alt_config()
    #print("Alt Config")
    data_config()
    #print("Data Config")
    time.sleep(1)
    alt = read_alt_temp()
    #print("Read Alt")
    control_pres_config()
    #print("Press Alt")
    time.sleep(.1)
    pres = read_pres()
    #print("Read Press")
    
    return alt, pres

def getAltitude(): 
    while True: 
        alt, pres = startUp()
        
        if alt['a'] > 1000 or pres['p'] < 1000:
            #print(alt, pres)
            alt, pres = startUp()
        #else:
            print("Altitude : {:.2f} m".format(alt['a']))
          #  print("Temperature in Celsius : {:.2f} C".format(alt['c']))
           # print("Temperature in Fahrenheit : {:.2f} F".format(alt['f']))
            #print("Pressure : {:.2f} hPa".format(pres['p']))
            
        alt_data = [alt['a'], alt['c'], alt['f'], pres['p']]
            
        return alt_data

if __name__ == "__main__":
    getAltitude()
