import cv2
import PIL.Image
from io import BytesIO
import IPython.display
from matplotlib import pyplot as plt
import os #need for directory


from IPython.display import clear_output

import imutils
import numpy as np #useful math/array stuff
import time


#Function that converts array data to image
def array_to_image(a, fmt='jpeg'):
    #Create binary stream object
    f = BytesIO()
    
    #Convert array to binary stream object
    PIL.Image.fromarray(a).save(f, fmt)
    
    return IPython.display.Image(data=f.getvalue())

def save_image(frame):
    cv2.imwrite('test.jpeg', frame)
    return print('Saved')

def get_frame(cam):
    # Capture frame-by-frame
    ret, frame = cam.read()
    crop = frame[1:250,150:400] #used! [y1(top):y2(bottom),x1(left):x2(right)]
    return crop

# Display the image
d1 = IPython.display.display("Your image displayed here!", display_id=1)

# Start video capture 
cam = cv2.VideoCapture(0)
frame = get_frame(cam)
# Change the color to RGB
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# Resize the image to 200px
frame = imutils.resize(frame, width=200, inter=cv2.INTER_LINEAR)

save_image(frame)

cam.release()
#Call the function to convert array data to image
frame = array_to_image(frame)

d1.update(frame)



#####################


img = cv2.imread("target.jpeg")


# Start video capture 
cam = cv2.VideoCapture(0)
frame = get_frame(cam)
# Change the color to RGB
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# Resize the image to 200px
frame = imutils.resize(frame, width=200, inter=cv2.INTER_LINEAR)
#save_image(frame)

cam.release()

def mse(imageA, imageB):
    err = np.sum((imageA - imageB) ** 2)
    err = err/((float(imageA.shape[1] * imageA.shape[0]))**2)
    
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

#print(type(frame),type(img))
err = mse(frame, img)

if err < 0.0050:
    print('Target Aquired!')
    print(err)
    
if err >= 0.0050:
    print('No Target')
    print(err)
    
frame = array_to_image(frame)
img = array_to_image(img)

d2 = IPython.display.display("Your image displayed here!", display_id=2)
d3 = IPython.display.display("Your image displayed here!", display_id=3)
d2.update(frame)
d3.update(img)
