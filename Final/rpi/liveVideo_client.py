import socket
import time
import picamera
import io
import subprocess
from PIL import Image, ImageFile

def client():

    client_socket = socket.socket()
    client_socket.connect(('0.0.0.0', 5000))

    # Make a file-like object out of the connection
    connection = client_socket.makefile('wb')
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 24
            # Start a preview and let the camera warm up for 2 seconds
            camera.start_preview()
            time.sleep(2)
            # Start recording, sending the output to the connection for 60
            # seconds, then stop
            camera.start_recording(connection, format='h264')
            camera.wait_recording(60)
            camera.stop_recording()
    finally:
        connection.close()
        client_socket.close()

def client2():
    client_socket = socket.socket()
    client_socket.connect(('0.0.0.0', 5000))
    
    # Accept a single connection and make a file-like object out of it
    connection = client_socket.makefile('rb')
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
        client_socket.close()
        player.terminate()
    
def client3():
    
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('0.0.0.0', 8000))
    
    # Accept a single connection and make a file-like object out of it
    #connection = client_socket.makefile('rb')
    string_value = b''
    try:
        while True:
        #for i in range(1):
            msg= client_socket.recv(4096)
            string_value+=msg
            byte_value = bytearray(string_value)
            stream = io.BytesIO(byte_value)
            print (stream.getvalue())
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + stream.getvalue() + b'\r\n')
            #image = Image.open(stream).convert("RGBA")
            stream.close()
            #image.save('testing_image.png')
    finally:
        client_socket.close()
    
def client4():
    import base64
    import cv2
    import zmq

    context = zmq.Context()
    footage_socket = context.socket(zmq.PUB)
    footage_socket.connect(('0.0.0.0', 5000))

    camera = cv2.VideoCapture(0)  # init the camera

    while True:
        try:
            grabbed, frame = camera.read()  # grab the current frame
            frame = cv2.resize(frame, (640, 480))  # resize the frame
            encoded, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer)
            footage_socket.send(jpg_as_text)

        except KeyboardInterrupt:
            camera.release()
            cv2.destroyAllWindows()
            break    
    
    
    
if __name__=='__main__':
    client3()
