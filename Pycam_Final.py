import cv2
import PIL.Image
from io import BytesIO
import IPython.display
from matplotlib import pyplot as plt


from IPython.display import clear_output

import serial #need for ev3 talk
s=serial.Serial("/dev/serial0",9600,timeout=2)

#system link coms - this has been modified to work with Chris's verision
import binascii as ubinascii
import json as ujson
import requests as urequests


import imutils
import numpy as np #useful math/array stuff
import time

#Basic System's Check

print('Libraries Loaded')
s.write('L'.encode())


#######################


# Convert's array values to image format
def array_to_image(a, fmt='jpeg'):
    #Create binary stream object
    f = BytesIO()
    #Convert array to binary stream object
    PIL.Image.fromarray(a).save(f, fmt)
    
    return IPython.display.Image(data=f.getvalue())

# Function to read the frame from camera
def get_frame(cam):
    ret, frame = cam.read()
    crop = frame[1:250,150:400]
    #crop = vis[y1:y2,x1:x2] cropping image
    return crop

#mean square error function
def mse(imageA, imageB):
    err = np.sum((imageA - imageB) ** 2)
    err = err/(float(imageA.shape[1] * imageA.shape[0])**2)
    
    return err

#Syetem link header
def SL_setup():
    Key = #####
    urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
    headers = {"Accept":"application/json","x-ni-api-key":Key}
    return urlBase, headers

#upload info to cloud
def Put_SL(Tag, Type, Value):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     propValue = {"value":{"type":Type,"value":Value}}
     try:
          reply = urequests.put(urlValue,headers=headers,json=propValue).text
     except Exception as e:
          print(e)         
          reply = 'failed'
     return reply

#down load info from cloud
def Get_SL(Tag):
    urlBase, headers = SL_setup()
    urlValue = urlBase + Tag + "/values/current"
    print(urlValue)
    print(headers)
    try:
        value = urequests.get(urlValue,headers=headers).text
        #print(value)
        data = ujson.loads(value)
        result = data.get("value").get("value")
        #print(result)
    except Exception as e:
        print(e)
        result = 'failed'
    return result

#Displays feed, counter added incase user terminates code remotely,
#The camera is released. Avoids camera issues

def CameraOn():
    d1 = IPython.display.display("Viewing Window", display_id=1)
    cam = cv2.VideoCapture(0)
    count = 0
    while True:
        count = count + 1
        if count >= 500:
                if Get_SL('Start08') == 'false':
                    # Release the camera resource
                    cam.release()
                    print('Capture Off')
                    break
                if Get_SL('Start08') == 'true':
                    count = 0
                    print('System Check')
                    
        #cropping function,Change the color to RGB,Resize the image to 200px
        frame = get_frame(cam)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = imutils.resize(frame, width=200, inter=cv2.INTER_LINEAR)
        
        #Checks Error
        err = mse(frame, img)
        #Thersholding
        if err < 0.0050:
            s=serial.Serial("/dev/serial0",9600,timeout=2)
            s.write("y".encode()) #to yes write to EV3
            print('Target Aquired!')
            print(err)
            cam.release()
            Put_SL('Start08', 'BOOLEAN', 'false')
            #Put_SL('Start09', 'BOOLEAN', 'false')
            break
            
        else:
            s=serial.Serial("/dev/serial0",9600,timeout=2)
            s.write("n".encode()) #to no write to EV3
            #print('No Target')  #coding checks
            #print(err)          #coding checks

        #Call the function to convert array data to image
        frame = array_to_image(frame)

        #Updates live feed
        d1.update(frame)



#Target image for release
img = cv2.imread("target.jpeg")


#Main loop
while True:
    if Get_SL('Start08') == 'false':
        print('waiting')
        time.sleep(0.5)
    if Get_SL('Start08') == 'true':
        #gets image spot ready on jupyter
        CameraOn()
        break
        
