from sensorData import *
from byteData import *
import socket

def sendCommand():
    # Create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the address
    server_socket.bind(('169.254.239.11', 4000))
    # Enable the server to listen to number of connections
    server_socket.listen(5)
    while True:
        # Accept a connection
        (clientsocket,address)=server_socket.accept()
        # Receive data from the socket and decode the data
        command = clientsocket.recv(2048).decode('utf-8')
        if command != "":
            try:
                # Send the data to Arduino
                send_command(command)
            except Exception as ex:
                print (ex)
       
                
    
if __name__=='__main__':
    sendCommand()
