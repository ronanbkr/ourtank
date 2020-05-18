# USAGE
# Command to run below
# python image_processing.py  

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2
import socket
import pickle
import struct
import base64
import numpy as np
import os 
import sys
import datetime
#from video_socket import client3_for4

count = 0
max_send = 10

def image_processing():
    
    ### Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9000))
    server_socket.listen(0)
    print ('Video Server is live')

    output = {}
    img_counter = 1
    object_list = ["", "background", "aeroplane", "bicycle", "bird",
        "bottle", "bus", "car", "cat", "chair", "diningtable",
        "person", "pottedplant",
        "sofa", "train", "tvmonitor"]

    # "cow", "boat", "motorbike","dog","horse","sheep",
    # initialize the list of class labels MobileNet SSD was trained to
    # detect, then generate a set of bounding box colors for each class
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # load our serialized model from disk
    embedder = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
    embedder.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

    # initialize the video stream, allow the cammera sensor to warmup,
    # and initialize the FPS counter
    print("Test: Video Stream starting")
    vs = VideoStream(src=0).start()
    time.sleep(2)
    confidence_limit = 0.6
    while True:
        try:
            (clientsocket,address)=server_socket.accept()
            print ('Connected')
            # loop over the frames from the video stream
            while True:
                start =time.time()
                # Take one frame from the video and resize it
                frame = vs.read()
                frame = imutils.resize(frame, width=400)

                # grab the frame dimensions and convert it to a blob
                (h, w) = frame.shape[:2]
                blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                    0.007843, (300, 300), 127.5)

                # pass the blob through the network and return detections and predictions
                embedder.setInput(blob)
                detections = embedder.forward()

                trigger = False 

                # loop over the detections
                for i in np.arange(0, detections.shape[2]):
                    # extract the confidence of the prediction
                    confidence = detections[0, 0, i, 2]

                    # make sure that the confidence is high enough
                    if confidence > confidence_limit:
                        # extract the index for the label
                        # compute the (x, y)-coordinates of
                        # the bounding box for the object
                        idx = int(detections[0, 0, i, 1])
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")
                        output["start x"] = startX
                        output["start y"] = startY
                        output["end x"] = endX
                        output["end y"] = endY
                        final_confidence = confidence * 100
                        output["confidence"] = "{:.2f}".format(final_confidence)
                        output["detection label"] = idx
                        trigger = True
                        if (trigger):
                            output["true/false indicator"] = 1
                        else:
                            output["true/false indicator"] = 0
                        # depending on the confidence, draw the prediction on the frame
                        if confidence < 0.75:
                            label = "{}: {:.2f}% Investigate".format(CLASSES[idx], final_confidence)
                            cv2.rectangle(frame, (startX, startY), (endX, endY),
                                COLORS[idx], 2)
                            y = startY - 15 if startY - 15 > 15 else startY + 15
                            cv2.putText(frame, label, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                            output["confidence"] = 0
                        else:
                            label = "{}: {:.2f}% Confirmed".format(CLASSES[idx], final_confidence)
                            cv2.rectangle(frame, (startX, startY), (endX, endY),
                                COLORS[idx], 2)
                            y = startY - 15 if startY - 15 > 15 else startY + 15
                            cv2.putText(frame, label, (startX, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                            output["confidence label"] = 1
                        
                # show the output frame
                #cv2.imshow("FrameServer", frame)
                #key = cv2.waitKey(1) & 0xFF
                
                auto_mode="False"
                if os.path.exists('auto_mode.pickle') and os.path.getsize('auto_mode.pickle') > 0:
                    with open('auto_mode.pickle','rb') as variable:
                        auto_mode = pickle.load(variable)
                if output != {} and output["true/false indicator"] == 1 and auto_mode == "True":                    
                    send_dict(output,'020')
                    output = {}
                 # Server sending frame in bytes format
                
                frame_data = pickle.dumps([frame,output])
                #encoded, frame_byte = cv2.imencode('.JPEG', frame)
                #frame_data = base64.b64encode(frame_byte)
                #encoded_dict = str(output).encode('utf-8')
                #output_data = base64.b64encode(encoded_dict)
                #size = len(frame_data)+len(output_data)
                size = len(frame_data)
                p = struct.pack('I', size)
                frame_data = p + frame_data
                clientsocket.sendall(frame_data)
                #clientsocket.close()

                # Takes a photo of the stream when c is pressed.
                # Used for testing
                if os.path.exists('take_screenshot.pickle') and os.path.getsize('take_screenshot.pickle') > 0:
                    with open('take_screenshot.pickle','rb') as variable:
                        screen_shot = pickle.load(variable)
                    if screen_shot == 'True':
                        found_value = "screenshot"             
                        if output != {} and (output["confidence label"] ==1):
                            found_value = CLASSES[output["detection label"]]                            
                        img_name = "current_screenshots/{}_{}.png".format(found_value,img_counter)
                        cv2.imwrite(img_name, frame)
                        img_name = "all_screenshots/{}_{}.png".format(found_value,img_counter)
                        cv2.imwrite(img_name, frame)
                        img_counter += 1
                        with open('log.txt','a') as f:
                            temp_text="Investigate"
                            if output["confidence label"] ==1:
                                temp_text ="Confirm"
                            text=" {} {} {} in {}\n".format(CLASSES[output["detection label"]],temp_text,output["confidence"],img_name)
                            f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+text)
                    with open('take_screenshot.pickle','wb') as f:
                        pickle.dump('False',f)  

                # break once q is pressed
                #if key == ord("q"):
                #    break
                # print (time.time()-start)
        except KeyboardInterrupt:
            if os.path.exists("take_screenshot.pickle"):
                os.remove("take_screenshot.pickle")
            if os.path.exists("auto_mode.pickle"):
                os.remove("auto_mode.pickle")
            server_socket.close()
            # do a bit of cleanup
            cv2.destroyAllWindows()
            vs.stop()
            return
        except Exception as e:
            print (str(e))
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            

            
    # Socket Connection closed
    server_socket.close()
     
  

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()

def send_dict(info,s):
    global count
    global max_send
    #print(max_send)
    try:
        with open('auto_mode.pickle','rb') as variable:
            auto_mode = pickle.load(variable)
        print("Auto_mode is ", auto_mode)

        if auto_mode == 'True':
            count+=1
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('169.254.239.11', 4000))
            for v in (info.values()):
                if (len(str(v)) < 3):
                    v = str(v)
                    if (len(str(v)) == 2):
                        v = "0" + v
                    else:
                        v = "00" + v
                    s+=v
                else:    
                    s+=str(v)
            if count == max_send:
                client_socket.sendall(s.encode('utf-8')) 
                count = 0      
                print(s, len(s))

    except Exception as ex:
        print (ex)
    
if __name__=='__main__':
    image_processing()
