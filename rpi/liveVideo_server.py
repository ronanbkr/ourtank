import socket
import subprocess
import picamera
import time
import io
import pickle
import struct
#import cv2
#import numpy as np
#import zmq
#import base64

def server():
    # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
    # all interfaces)
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('rb')
    try:
        # Run a viewer with an appropriate command line. Uncomment the mplayer
        # version if you would prefer to use mplayer instead of VLC
        cmdline = ['vlc', '--demux', 'h264', '-']
        #cmdline = ['mplayer', '-fps', '25', '-cache', '1024', '-']
        player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
        while True:
            # Repeatedly read 1k of data from the connection and write it to
            # the media player's stdin
            data = connection.read(1024)
            if not data:
                break
            player.stdin.write(data)
    finally:
        connection.close()
        server_socket.close()
        player.terminate()

def server2():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 24

        server_socket = socket.socket()
        server_socket.bind(('0.0.0.0', 5000))
        server_socket.listen(0)

        # Accept a single connection and make a file-like object out of it
        connection = server_socket.accept()[0].makefile('wb')
        try:
            camera.start_recording(connection, format='h264')
            camera.wait_recording(10)
            camera.stop_recording()
        finally:
            connection.close()
            server_socket.close()

def server3():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 24
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 8000))
        server_socket.listen(0)
        (clientsocket,address)=server_socket.accept()
        print ('Video is live')
        
        try:
            while (True):
                stream = io.BytesIO()
                camera.capture(stream, 'jpeg', use_video_port=True)
                clientsocket.sendall(stream.getvalue())
            
        #    stream = io.BytesIO()
            
        #    for frame in camera.capture_continuous(stream, 'jpeg',use_video_port=True):
                # return current frame
        #        stream.seek(0)
                #frame = stream.read() 
                 
                # print (stream)
         #       data = stream.read()
                
          #      clientsocket.sendall(data)
                
                #yield stream.read()

                # reset stream for next frame
           #     stream.seek(0)
           #     stream.truncate() 
        finally:
            server_socket.close()
            clientsocket.close()
            

def server4():

    context = zmq.Context()
    footage_socket = context.socket(zmq.SUB)
    footage_socket.bind(('0.0.0.0', 5000))
    footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

    while True:
        try:
            frame = footage_socket.recv_string()
            img = base64.b64decode(frame)
            npimg = np.fromstring(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)
            cv2.imshow("Stream", source)
            cv2.waitKey(1)

        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            break

def test_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print (socket.gethostname())
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(0)
    while True:
        (clientsocket,address)=server_socket.accept()
        clientsocket.send("Hello")
    

if __name__=='__main__':
    
   server3()
