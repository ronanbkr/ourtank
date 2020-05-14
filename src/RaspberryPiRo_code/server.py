import flask
import os
from flask import Flask, Response,  send_file, request, render_template,jsonify,make_response
from picamera import PiCamera
import cv2
import socket 
import io 
from flask_cors import CORS
from itertools import chain
import meinheld
import multiprocessing
import datetime
from video_socket import *
from getData import *
import pickle

app = Flask(__name__)
CORS(app)
######################## Raw Data #######################

log_ls=[]
command_dict={
    "002":" Manual Drive Forward. ",
    "003":" Manual Drive Reverse. ",
    "004":" Manual Turn Left. ",
    "005":" Manual Turn Right. ",
    "006":" Set To Autonomous Mode. ",
    "007":" Set To Manual Mode. ",
    "008":" Manual Tilt Camera Down. ",
    "009":" Manual Tilt Camera Up. ",
    "010":" Manual Pan Left. ",
    "011":" Manual Pan Right. ",
    "012":" Pan Cameras to center. ",
    "013":" Laser activated On/Off. ", 
    "015":" Screenshot taken. ",
    "016":" Free 1. ",
    "017":" Free 2. ",
    "018":" Free 3. ",
    "019":" Free 4. ",
    "020":" Investigation Activated . ",
    "021":" Toggle Neural Network Feed Night Mode Pi 3 Camera. ",
    "022":" Toggle Neural Network Feed Day Mode Pi 4 Camera. ",
}
max_command = 20
def write_log():
    with open('log.txt','a') as f:
        for command in log_ls:
            f.write(command+"\n")

@app.route('/video4',methods=['GET'])
def video4():
    try:
        with open('night_mode.pickle','rb') as night_file:
            night_mode=pickle.load(night_file)
            if night_mode=='True':
                print('nighton')
                result = client3("True")
                return Response(result,mimetype='multipart/x-mixed-replace; boundary=frame')
            else:
                print('nightoff')
                result = client4()
                return Response(result,mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as ex:
        return str(ex)    
        
@app.route('/video3',methods=['GET'])
def video3():
    try:
        return Response(client3("False"),mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as ex:
        return str(ex)

@app.route('/get_gps',methods=['GET'])
def get_data():
    data=getData()
    return (jsonify(data))

@app.route('/get_data', methods=['GET'])
def info():
    data = ""
    return jsonify(str(data))

@app.route('/get_screenshot', methods=['GET'])
def get_picture():
    with open('take_screenshot.pickle','wb') as f:
        pickle.dump('True',f)
    return 'Taken screenshot'


@app.route('/control',methods=['GET'])
def control():
    global log_ls
    global command_dict
    s = ""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('169.254.239.11', 4000))
        if ('direction' in request.args):
            if (request.args["direction"] in ["up", "ArrowUp"]):
                s = "002"
                client_socket.sendall(s.encode('utf-8'))    
            elif (request.args["direction"] in ["down", "ArrowDown"]):
                s = "003"
                client_socket.sendall(s.encode('utf-8'))    
            elif (request.args["direction"] in ["left", "ArrowLeft"]):
                s = "004"
                client_socket.sendall(s.encode('utf-8'))            
            elif (request.args["direction"] in ["right", "ArrowRight"]):
                s = "005"
                client_socket.sendall(s.encode('utf-8'))
            elif (request.args['direction'] in ["w"]):
                s = "008"
                client_socket.sendall(s.encode('utf-8'))
            elif (request.args['direction'] in ["s"]):
                s = "009"
                client_socket.sendall(s.encode('utf-8'))
            elif (request.args['direction'] in ["a"]):
                s = "010"
                client_socket.sendall(s.encode('utf-8'))
            elif (request.args['direction'] in ["d"]):
                s = "011"
                client_socket.sendall(s.encode('utf-8'))
            elif (request.args['direction'] in ["c"]):
                s = "012"
                client_socket.sendall(s.encode('utf-8'))
            # elif (request.args['direction'] in ["l"]):
            #    s = "013"
            # elif (request.args['direction'] in ["p"]):
            #    s = "015"
            log_ls.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Sending direction: " + command_dict[s])
            
            if len(log_ls)==max_command:
                print("logging")
                write_log()
                log_ls=[]
            return request.args['direction']
            
        elif ('command' in request.args):
            command = request.args['command']

            try:
                # Tank Manual/Auto
                if (command == 'auto'):
                    with open('auto_mode.pickle','wb') as variable:
                        pickle.dump('True',variable)
                    s = "006"
                    client_socket.sendall(s.encode('utf-8'))
                    
                elif (command == 'manual'):
                    with open('auto_mode.pickle','wb') as variable:
                        pickle.dump('False',variable)
                    s = "007"
                    client_socket.sendall(s.encode('utf-8'))
                                                
#                # Lazer on/off
                elif (command == 'lazeron'):
                    s = "013"
                    client_socket.sendall(s.encode('utf-8'))
                elif (command == 'lazeroff'):
                    s = "014"
                    client_socket.sendall(s.encode('utf-8'))
                    
#                # Night mode on/off  
                elif (command == 'nighton'):
                    with open('night_mode.pickle','wb') as variable:
                        pickle.dump('True',variable)
                    s = "021"
                    client_socket.sendall(s.encode('utf-8'))
                    
                elif (command == 'nightoff'):
                    with open('night_mode.pickle','wb') as variable:
                        pickle.dump('False',variable)
                    s = "022"
                    client_socket.sendall(s.encode('utf-8'))
                elif (command == 'take_photo'):
                    s = "015"
                    print (s)
                    with open('take_screenshot.pickle','wb') as f:
                        pickle.dump('True',f)
                #client_socket.sendall(s.encode('utf-8'))
                print(command)
                log_ls.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' Sending Command: '+command_dict[s])                
                if len(log_ls)==max_command:
                    print("logging")
                    write_log()
                    log_ls=[]
                return command
            except Exception as ex:
                print (ex)
                return (str(ex))
        else:
            print ("Need direction key")
            return "Need direction key"
    except Exception as e:
        print (str(e))
        
######################### We put data on the web ###################################      

@app.route('/video_page',methods = ['GET'])
def video_page():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('169.254.239.11', 4000))
        client_socket.sendall('007'.encode('utf-8'))
        #data = getData()
    except Exception as e:
        print(str(e))
    #return render_template('index.html',message=jsonify(data))
    return render_template('index.html')

@app.route('/',methods=['GET'])
def home_page():
    return "RAMP Data Page"

if __name__=='__main__':        
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('169.254.239.11', 4000))
    with open('night_mode.pickle','wb') as variable:
        pickle.dump('False',variable)
        client_socket.sendall('022'.encode('utf-8'))
    app.run(host='0.0.0.0',threaded=True)
    #meinheld.listen(("0.0.0.0", 5000))
    #meinheld.run(app)
