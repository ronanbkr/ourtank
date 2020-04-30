import cv2
import pickle
import socket
import struct
import base64
import numpy as np
import time

def client3():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('169.254.239.11', 8000))
    payload_size = struct.calcsize("I")
    data=b''
    while True:
        start = time.time()
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
        #frame=pickle.loads(frame_data,encoding='latin1')
        img = base64.b64decode(frame_data)
        npimg = np.fromstring(img, dtype=np.uint8)
        frame = cv2.imdecode(npimg, 1)

        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        _,frame_bytes= cv2.imencode('.JPEG',frame)
        print (time.time()-start)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes.tostring()+ b'\r\n')
    #client_socket.close()

info ={}
def client4():
    global info
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
        _,frame_bytes= cv2.imencode('.JPEG',frame_numpy[0])
        info=frame_numpy[1]
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes.tostring()+ b'\r\n')
        #yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes.tostring()+ b'\r\n',frame_numpy[1])
    #client_socket.close()
    
def get_info():
    return info
