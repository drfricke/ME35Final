
from PIL import Image, ImageOps
import numpy as np
import binascii, json, requests, time, tensorflow.keras, cv2

import binascii as ubinascii
import json as ujason
import requests as urequests
import time


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the qshape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

#start up variables
frame, image, = None, None

#get password
##def get_key():
##    fin = open('Practice.txt')
##    for element in fin:
##        return element

Key = 'bvd8X9LweQY9o2eP1NYL-p8mLL9wMAk6YYOnYSiIo0'

#System link setup, gets, and puts

def SL_setup():
     Key = 'bvd8X9LweQY9o2eP1NYL-p8mLL9wMAk6YYOnYSiIo0'
     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     headers = {"Accept":"application/json","x-ni-api-key":Key}
     return urlBase, headers

def Get_SL(Tag):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     try:
          value = requests.get(urlValue,headers=headers).text
          data = json.loads(value)
          result = data.get("value").get("value")
     except Exception as e:
          print(e)
          result = 'failed'
     return result

def Put_SL(Tag, Type, Value):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     propValue = {"value":{"type":Type,"value":Value}}
     try:
          reply = requests.put(urlValue,headers=headers,json=propValue).text
     except Exception as e:
          print(e)         
          reply = 'failed'
     return reply

#funtion that handles predition model

def prediction(frame):
    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    #Need to change cv2 image accordingly
    frame = Image.fromarray(frame)
    image = ImageOps.fit(frame, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)

    # display the resized image
    #image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference and give predition
    prediction = model.predict(data)
    print(prediction)
    #print(np.argmax(prediction))
    shape_index = np.argmax(prediction)
    return np.argmax(prediction)

#Turns camera on
image = cv2.VideoCapture(0)


##while True:
##    if Get_SL('Start08') == 'false':
##        ret, frame = image.read()
##        frame = frame[380:600,520:780]
##        cv2.imshow('frame',frame)  
##        print('waiting')
##        time.sleep(0.5)
##    if Get_SL('Start08') == 'true':
##        print('go!')
##        break

while(True):
    # Capture frame-by-frame
    ret, frame = image.read()
    # crop! Very important improves predictions!
    frame = frame[380:600,520:780]
    # Display the resulting frame
    cv2.imshow('frame',frame)
    
    #Allows user to excute commands and quit
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
         ball = prediction(frame)
         if ball == 0:
              print('Package Recieved')
              #image.release()
              #cv2.destroyAllWindows()
              #Put_SL('Start09', 'BOOLEAN', 'true')
         if ball == 1:
              print('Target Missed')
              
    if key == ord('p'):
        image.release()
        cv2.destroyAllWindows()
        print('Good Bye!')
        break
    #Allows EV3 to interact and get predictions via sys link
##    if Get_SL('Start08') == 'false':
##       time.sleep(1)
##       ball = prediction(frame)

           



