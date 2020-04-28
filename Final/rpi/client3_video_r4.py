#import cv2
#import pickle
import pickle
import socket
import struct
import subprocess

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.0.34', 9000))
    payload_size = struct.calcsize("I")
    data=b''
    while True:
        while len(data) < payload_size:
            data += client_socket.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("I", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        if frame_data=='':
            break
        print (type(frame_data))
        frame=pickle.loads(frame_data)
        # print(frame_data)
        
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        
    client_socket.close()
    
    player.terminate()
        
        
if __name__=='__main__':
    client()
