import socket
import json

def getData():
    try:
        # Create an INET, STREAMing socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the address
        client_socket.connect(('169.254.239.11', 7000))
        while  True:
            # Receive data from the socket and decode the data
            data = client_socket.recv(4096)
            data_json = json.loads(data.decode('utf-8'))
            return data_json
    except Exception as ex:
        pass
        
if __name__=='__main__':
    data=getData()
    print (data)
