from sensorData import *
from byteData import *
import socket

def sendCommand():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 4000))
    server_socket.listen(0)
    while True:        
        (clientsocket,address)=server_socket.accept()
        command = clientsocket.recv(1024).decode('utf-8')
        send_command(command)
        
                
    
if __name__=='__main__':
    sendCommand()
