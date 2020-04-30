# -*- coding: utf-8 -*-

import cv2
import socket
import pickle
import struct
import imutils

def sendVideo():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('169.254.239.11', 8000))
        server_socket.listen(0)
        print ('Video Server is live')
        vs = cv2.VideoCapture(0)
        while True:
                try:
                        (clientsocket,address)=server_socket.accept()
                        print ("Connected")
                        while True:
                                rval, frame = vs.read()
                                frame = imutils.resize(frame, width=400)
                                frame =cv2.resize(frame, (300, 300))
                                #cv2.imshow("FrameServer", frame)
                                #key = cv2.waitKey(1) & 0xFF
                                frame = pickle.dumps(frame)
                                size = len(frame)
                                p = struct.pack('I', size)
                                frame = p + frame
                                clientsocket.sendall(frame)
                except Exception as err:
                        print (str(err))
        server_socket.close()
        vs.stop()                
                
if __name__=='__main__':
        sendVideo()
