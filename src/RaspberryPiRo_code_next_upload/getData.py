import socket
import json

def getData():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('169.254.239.11', 7000))
        while  True:
            data = client_socket.recv(4096)
            data_json = json.loads(data.decode('utf-8'))
            return data_json
    except Exception as ex:
        pass
        
if __name__=='__main__':
    getData()
