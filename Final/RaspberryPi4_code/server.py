import flask
import os
from flask import Flask, Response,  send_file, request, render_template,jsonify,make_response
from picamera import PiCamera
import cv2
import socket 
import io 
from sensorData import *
from byteData import *

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
            if (request.args['direction'] == 'up' or request.args['direction'] =='ArrowUp'):
                client_socket.sendall('002'.encode('utf-8'))    
            elif (request.args['direction'] == 'down' or request.args['direction'] == 'ArrowDown'):
                client_socket.sendall('003'.encode('utf-8'))    
            elif (request.args['direction'] == 'left' or request.args['direction'] == 'ArrowLeft'):
                client_socket.sendall('004'.encode('utf-8'))            
            elif (request.args['direction'] == 'right' or request.args['direction'] == 'ArrowRight'):
                client_socket.sendall('005'.encode('utf-8'))
            elif (request.args['direction'] == 'stop' or request.args['direction'] == '007'):
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
    return render_template('index.html')


@app.route('/',methods=['GET'])
def home_page():
    return "RAMP Data Page"


if __name__=='__main__':
    app.run(host='0.0.0.0',threaded=True)
