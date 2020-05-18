from sensorData import *
from byteData import *
import socket,errno
import json

def sendData():
    # Create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the address
    server_socket.bind(('169.254.239.11', 7000))
    # Enable the server to listen to number of connections
    server_socket.listen(5)
    while True:
        # Get GPS from Arduino
        data = main()
        # Encode the data to send via socket
        data_bytes= json.dumps(data).encode('utf-8')
        # Accept a connection
        (clientsocket,address)=server_socket.accept()
        print ('Connected')
        # Send the data via socket
        clientsocket.sendall(data_bytes)
        
                
    
if __name__=='__main__':
    sendData()
