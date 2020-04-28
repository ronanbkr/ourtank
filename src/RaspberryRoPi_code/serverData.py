from sensorData import *
from byteData import *
import socket,errno
import json

def sendData():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 7000))
    server_socket.listen(0)
    while True:        
        data = main()
        data_bytes= json.dumps(data).encode('utf-8')
        (clientsocket,address)=server_socket.accept()
        clientsocket.sendall(data_bytes)
        
                
    
if __name__=='__main__':
    sendData()