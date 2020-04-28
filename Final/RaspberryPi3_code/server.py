import flask
import os
from flask import Flask, Response,session,redirect, request, render_template,jsonify,make_response

# Testing camera
from picamera import PiCamera
import cv2
import socket 
import io 
import threading
from sensorData import *
from byteData import *

from camera_pi import Camera

from liveVideo_client import *

from client3_video_r4 import *

app = Flask(__name__)

######################## We get raw data
def gen1():
    camera=Camera()
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen2():
    threading.currentThread().setName('LIVE_VIDEO')
    t = threading.currentThread()
    
    vc = cv2.VideoCapture(0) 
    
    #while (getattr(t,'do_run',True)): 
    while (vc.isOpened()): 
        rval, frame = vc.read() 
        
        if  (rval==True):
           cv2.imwrite('pic.jpg', frame) 
           if cv2.waitKey(1) & getattr(t,'do_run',False):
               break
           yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n')
        else:
            break
        #time.sleep(.5)
    vc.release()

def gen3():
    framerate = 90
    quality = 100
    res = (1280, 720)
    with PiCamera(framerate=framerate, resolution=res) as camera:
        time.sleep(2)  # camera warm-up time
        while True:
            try:
                image = io.BytesIO()
                camera.capture(image, 'jpeg', quality=quality, use_video_port=True)
                print (image.getvalue())
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + image.getvalue() + b'\r\n')
            except:
                time.sleep(3) 

@app.route('/video',methods=['GET'])
def video():
    try:
        return Response(client3(),mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as ex:
        return str(ex)
    
@app.route('/video_cancel',methods=['GET'])
def cancel_video():
    try:
        alive_video = [t for t in threading.enumerate() if t.getName() == 'LIVE_VIDEO']
        alive_video.do_run = False
        alive_video.join()
        return "Stopped"
    except Exception as ex:
        return str(ex)

@app.route('/command',methods=['GET'])
def do_command():
    if 'command' in request.args:
        command = request.args['command']
        try:
            if (command == 'Auto'):
                send_command('006')
            elif (command == 'Manual'):
                send_command('007')
            print (command)
            return command
        except Exception as ex:
            print (ex)
            return (str(ex))
    
@app.route('/get_data',methods = ['GET'])
def get_data():
    data = main()
    return jsonify(data)


@app.route('/stop',methods = ['GET'])
def stop_running():
    send_command('007')
    return "Stop"

@app.route('/control',methods = ['GET'])
def control():
    try:
        if ('direction' in request.args):
            print (request.args['direction'])
            if (request.args['direction'] == 'up' or request.args['direction'] =='ArrowUp'):
                send_command('002')
            elif (request.args['direction'] == 'down' or request.args['direction'] == 'ArrowDown'):
                send_command('003')
            elif (request.args['direction'] == 'left' or request.args['direction'] == 'ArrowLeft'):
                send_command('004')            
            elif (request.args['direction'] == 'right' or request.args['direction'] == 'ArrowRight'):
                send_command('005')
            elif (request.args['direction'] == 'stop' or request.args['direction'] == '007'):
                send_command('007')
            
            return request.args['direction']
        else:
            print ("Need direction key")
            return "Need direction key"
    except Exception as e:
        print (str(e))
            
        
######################### We put data on the web        

@app.route('/video_page',methods = ['GET'])
def video_page():
    data = main()
    return render_template('index.html',message = jsonify(data))

@app.route('/',methods = ['GET'])
def home_page():
    return "RAMP DATA PAGE" #+ "/n" + 

if __name__ == '__main__':
    app.run(host = '0.0.0.0',threaded = True,debug = True)
