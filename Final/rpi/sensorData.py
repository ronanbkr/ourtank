from altitude import *
from gps import *
from gyro import *

def main():
    altitudeData = getAltitude()
    #print("Altitude Data: ", altitudeData)
    #print("")
    gyroData = getGyroData()
    #print("Gyro Data", gyroData)
    #print("")
    #gpsData = getGPSdata()
    #print("GPS Data: ", gpsData)
    dic ={
        "Altitude Data: ": str(altitudeData),
        "GyroData:": str(gyroData),
        #"GPSData:":str(gpsData)
    }
    
    return dic
              
    
if __name__ == '__main__':
    main()
    
    
    

    
    
        
        
        
