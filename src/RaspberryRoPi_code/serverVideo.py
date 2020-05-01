# -*- coding: utf-8 -*-

import cv2
import socket
import pickle
import struct
import imutils
import base64
import time


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
                                start = time.time()
                                rval, frame = vs.read()
                                frame = imutils.resize(frame, width=200)
                                frame =cv2.resize(frame, (300, 225))
                                #cv2.imshow("FrameServer", frame)
                                #key = cv2.waitKey(1) & 0xFF
                                #frame = pickle.dumps(frame)
                                encoded, frame_byte = cv2.imencode('.JPEG', frame)
                                frame = base64.b64encode(frame_byte)
                                size = len(frame)
                                p = struct.pack('I', size)
                                frame = p + frame
                                print (time.time()-start)
                                clientsocket.sendall(frame)
                except Exception as err:
                        print (str(err))
        server_socket.close()
        vs.stop()                
                
if __name__=='__main__':
        sendVideo()
