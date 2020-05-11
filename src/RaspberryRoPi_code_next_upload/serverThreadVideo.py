import cv2, Queue, threading, time
import socket
import struct
import imutils
import base64

# bufferless VideoCapture
class VideoCapture:

  def __init__(self, name):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('169.254.239.11', 8000))
    server_socket.listen(0)
    print ('Video Server is live')
    self.cap = cv2.VideoCapture(name)
    #self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
    self.q = Queue.Queue()
    t = threading.Thread(target=self._reader,args=(server_socket,))
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self,server_socket):
    (clientsocket,address)=server_socket.accept()
    print ("Connected")
    while True:
      start = time.time()
      ret, frame = self.cap.read()
      frame = imutils.resize(frame, width=200)
      frame =cv2.resize(frame, (300, 225))
      encoded, frame_byte = cv2.imencode('.JPEG', frame)
      frame = base64.b64encode(frame_byte)
      size = len(frame)
      p = struct.pack('I', size)
      frame = p + frame
      clientsocket.sendall(frame)
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except Queue.Empty:
          pass
      self.q.put(frame)
      print (time.time()-start)
      
  def read(self):
    return self.q.get()

def sendVideo():
    cap = VideoCapture(0)
    while True:
        try:
            frame = cap.read()

        except Exception as err:
                print (str(err))
    
if __name__=='__main__':
    sendVideo()
