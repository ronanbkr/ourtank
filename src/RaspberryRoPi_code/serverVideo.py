# -*- coding: utf-8 -*-

import cv2
import socket
import pickle
import struct
import imutils
import base64
import time


def sendVideo():
    # Create an INET, STREAMing socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the address
    server_socket.bind(('169.254.239.11', 8000))
    # Enable the server to listen to number of connections
    server_socket.listen(0)
    print ('Video Server is live')
    # Start recording
    vs = cv2.VideoCapture(0)
    while True:
        try:
            # Accept a connection
            (clientsocket,address)=server_socket.accept()
            print ("Connected")
            while True:
                start = time.time()
                # Get the frame
                rval, frame = vs.read()
                # Resize the frame
                frame = imutils.resize(frame, width=200)
                frame =cv2.resize(frame, (300, 225))
                #frame = pickle.dumps(frame)
                # Encode the frame to the picture of JPEG format
                encoded, frame_byte = cv2.imencode('.JPEG', frame)
                # Convert the picture to printable base64 encoding.
                frame = base64.b64encode(frame_byte)
                size = len(frame)
                # Use struct to package the data to send through sockets
                p = struct.pack('I', size)
                frame = p + frame
                #print (time.time()-start)
                # Send the data via socket
                clientsocket.sendall(frame)
        except Exception as err:
                print (str(err))
    server_socket.close()
    vs.stop()                
                
if __name__=='__main__':
    sendVideo()
