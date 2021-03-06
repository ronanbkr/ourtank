import cv2
import pickle
import socket
import struct
import base64
import numpy as np
import time
from image_processing2 import image_processing_pi3
 
def client3(night_mode):
    # Create an INET, STREAMing socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the address
    client_socket.connect(('169.254.239.11', 8000))
    # Calculate the size of the sent package
    payload_size = struct.calcsize("I")
    data=b''
    while True:
        start = time.time()
        # Get all data via network
        while len(data) < payload_size:
            data += client_socket.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        # Unpack the sent package
        msg_size = struct.unpack("I", packed_msg_size)[0]
        # Get all data via network
        while len(data) < msg_size:
            data += client_socket.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        if frame_data=='':
            break
        # Convert byte format back to frame
        #frame=pickle.loads(frame_data,encoding='latin1')
        img = base64.b64decode(frame_data)
        npimg = np.fromstring(img, dtype=np.uint8)
        frame = cv2.imdecode(npimg, 1)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        if (night_mode=='True'):
            # Trying to process with night mode
            processed_frame = image_processing_pi3(frame)
            print(processsed_frame)
            _,frame_bytes= cv2.imencode('.JPEG',processed_frame)
        else:            
            _,frame_bytes= cv2.imencode('.JPEG',frame)
        #print (time.time()-start)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes.tostring()+ b'\r\n')
    client_socket.close()

def client4():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('0.0.0.0', 9000))
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
        frame=pickle.loads(frame_data)
        #img = base64.b64decode(frame_data)
        #npimg = np.fromstring(img, dtype=np.uint8)
        #frame = cv2.imdecode(npimg, 1)
        #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        _,frame_bytes= cv2.imencode('.JPEG',frame[0])
        info=frame[1]
        #print (time.time()-start)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes.tostring()+ b'\r\n')
        #yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes.tostring()+ b'\r\n',frame_numpy[1])
    client_socket.close()
    
