import cv2
import pickle
import socket
import struct


def client3():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('169.254.239.11', 8000))
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
        frame_numpy=pickle.loads(frame_data,encoding='latin1')
        #print (frame_numpy)
        _,frame_bytes= cv2.imencode('.JPEG',frame_numpy)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes.tostring()+ b'\r\n')
    #client_socket.close()

def client4():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('0.0.0.0', 9000))
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
        frame_numpy=pickle.loads(frame_data)
        _,frame_bytes= cv2.imencode('.JPEG',frame_numpy)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes.tostring()+ b'\r\n')
    #client_socket.close()
        
