import time
import serial
import string
import pynmea2
 
port = "/dev/ttyAMA0" # the serial port to which the pi is connected.
 
#create a serial object
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)

def getGPSdata():
        gpsData=[]
        run = True    
          
        while run:
                try:
                    data = ser.readline()
                except:
                    print("loading") 
                    break
                #print ("Running",type(data),data[0:6],data[0:6]==b'$GPGGA')  

                if (data[0:6] == b'$GPGGA'): 
                        #print (data)
                        #print ("Im in here")
                        #print (data.decode('utf-8').split(','))
                        #msg = pynmea2.parse(data)
                        msg = data.decode('utf-8').split(',')
                        #print ("Im in here now")
                        #msgTime = msg.timestamp
                        msgTime = msg[0].encode("ascii")
                        #latD = msg.latitude
                        latM = msg[2].encode("ascii")
                        latD = msg[3].encode("ascii")
                        lonM = msg[4].encode("ascii")
                        lonD = msg[5].encode("ascii")
                        satquality = msg[6].encode("ascii")
                        noSats = msg[7].encode("ascii")
                        horz = msg[8].encode("ascii")
                        alt = msg[9].encode("ascii")
                        alt_units = msg[10].encode("ascii")
                        geo_sep = msg[11].encode("ascii")
                        refSta = msg[-1].encode("ascii")
                        if (latM != '' and lonM != ''):
                                run = False
                                
                                return( ["Latitude:", latM + latD, "Longitude:", lonM + lonD, "Satalite Quality:", satquality, "Available Satalites:", noSats, "Altitude:", alt + alt_units])
                        
                        #latM = str(msg.latitude_minutes)
                        #latS = msg.latitude_seconds
                        #latDir = msg.lat_dir
                        
                        #lonD = msg.longitude
                        #lonD= msg[2]
                        #lonM = str(msg.longitude_minutes)
                        #lonS = msg.longitude_seconds
                        #lonDir = msg.lon_dir
                        #gpsQ = msg.gps_qual
                        #numSat = msg.num_sats
                        #horizontal = msg.horizontal_dil
                        #alt = msg.altitude
                        #unit = msg.altitude_units
                        #sep = msg.geo_sep
                        #sepUnits = msg.geo_sep_units
                        #msgAge = msg.age_gps_data
                        #refSta = msg.ref_station_id

                         ##Time
                        #print (msgTime)
                        
                         ##Latitude
                        #print("Latitude: {:.0f},{},{:.4f}".format(latD, latM[:2]))#, latS))

                         ##Longitude
                        #print("Lonitude: {:.0f},{},{:.4f}".format(abs(lonD), lonM[:2]))#, lonS))

                         ##GPS Quality
                        #print("GPS Quality: " + str(gpsQ))

                         ##Number of Satelites
                        #print("Number of satelites: " + str(numSat))

                         ##Horizontal
                        #print("Horizontal dil: " + str(horizontal))

                        ## Altitude
                        #print("Altitude: " + str(alt) + str(unit.lower()))

                         ##Geo Separation
                        ##print("Geo seperation: " + str(sep) + str(sepUnits.lower()))
                        
                        #gpsData = [msgTime, latD, latM, latS, latDir, lonD, lonM, lonS, lonDir, gpsQ, numSat, horizontal, alt, unit, sep, sepUnits]
                        
                        #run = False
                        #print("woohoo",gpsData)
        #if (run == False)
                        #return gpsData
                   
                #time.sleep(0.5)

if __name__ == "__main__":
        getGPSdata()
        
