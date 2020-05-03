from sensorData import *
from byteData import *
import socket

def sendCommand():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('169.254.239.11', 4000))
    server_socket.listen(5)
    while True:        
        (clientsocket,address)=server_socket.accept()
        #print ('Connected')
        command = clientsocket.recv(2048).decode('utf-8')
        print (command)
        try:
            send_command(command)
        except Exception as ex:
            print (ex)
       
                
    
if __name__=='__main__':
    sendCommand()
