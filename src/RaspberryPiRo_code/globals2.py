# from multiprocessing import Value
# import multiprocessing
# lock = multiprocessing.Lock()

# global auto_mode
# #auto_mode = False
# auto_mode = Value('b', False)
# def initialize():
   # lock.acquire()
   # global auto_mode
   # #auto_mode = False
   # print("Auto mode is " + str(auto_mode))
   # lock.release()

# def set_auto_mode():
   # lock.acquire()
   # global auto_mode
   # auto_mode = True
   # lock.release()


# def set_manual_mode():
   # lock.acquire()
   # global auto_mode
   # auto_mode = False
   # lock.release()
   
# def auto_mode_value():
   # lock.acquire()
   # global auto_mode
   # x = auto_mode
   # lock.release()
   # return x
   
   
