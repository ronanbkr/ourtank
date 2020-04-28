import flask
import os
from flask import Flask, Response,  send_file, request, render_template,jsonify,make_response
from master_controller import *

app = Flask(__name__)

######################## Raw Data #######################

def gen():
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

@app.route('/video',methods=['GET'])
def video():
    try:
        return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as ex:
        return str(ex)

@app.route('/get_data',methods=['GET'])
def get_data():
    data = main()
    return jsonify(data)

@app.route('/control',methods=['GET'])
def control():
    try:
        if ('direction' in request.args):
            print (request.args['direction'])
            return request.args['direction']
        else:
            print ("Need direction key")
            return "Need direction key"
    except Exception as e:
        print (e)
        
######################### We put data on the web ###################################      

@app.route('/video_page',methods = ['GET'])
def video_page():
    data = main()
    return render_template('index.html',message = jsonify(data))


@app.route('/',methods=['GET'])
def home_page():
    return "RAMP Data Page"



if __name__=='__main__':
    app.run(host='0.0.0.0',threaded=True)
