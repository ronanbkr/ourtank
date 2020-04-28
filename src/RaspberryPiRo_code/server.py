import flask
import os
from flask import Flask, Response,  send_file, request, render_template,jsonify,make_response
from picamera import PiCamera
import cv2
import socket 
import io 

from video_socket import *
from getData import *

app = Flask(__name__)

######################## Raw Data #######################

@app.route('/video4',methods=['GET'])
def video4():
    try:
        return Response(client4(),mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as ex:
        return str(ex)    
        
@app.route('/video3',methods=['GET'])
def video3():
    try:
        return Response(client3(),mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as ex:
        return str(ex)

@app.route('/get_data',methods=['GET'])
def get_data():
    data = getData()
    return jsonify(data)

@app.route('/control',methods=['GET'])
def control():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('192.168.0.12', 4000))
        if ('direction' in request.args):
            if (request.args["direction"] in ["up", "ArrowUp", "w"]):
                client_socket.sendall('002'.encode('utf-8'))    
            elif (request.args["direction"] in ["down", "ArrowDown", "s"]):
                client_socket.sendall('003'.encode('utf-8'))    
            elif (request.args["direction"] in ["left", "ArrowLeft", "a"]):
                client_socket.sendall('004'.encode('utf-8'))            
            elif (request.args["direction"] in ["right", "ArrowRight", "d"]):
                client_socket.sendall('005'.encode('utf-8'))
            elif (request.args['direction'] in ["007", "stop", ""]):
                client_socket.sendall('007'.encode('utf-8'))
            return request.args['direction']
        elif ('command' in request.args):
            command = request.args['command']
            try:
                if (command == 'Auto'):
                    client_socket.sendall('006'.encode('utf-8'))
                elif (command == 'Manual'):
                    client_socket.sendall('007'.encode('utf-8'))
                print (command)
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
        client_socket.connect(('192.168.0.12', 4000))
        client_socket.sendall('007'.encode('utf-8'))
    except Exception as e:
        print(str(e))
    return render_template('index.html')

@app.route('/',methods=['GET'])
def home_page():
    return "RAMP Data Page"


if __name__=='__main__':
    app.run(host='0.0.0.0',threaded=True)
