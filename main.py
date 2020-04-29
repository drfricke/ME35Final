#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import ubinascii, ujson, urequests, utime

# Write your program here
ev3 = EV3Brick()
#ev3.speaker.beep()

#pycam set up
from pybricks.iodevices import AnalogSensor, UARTDevice
uart = UARTDevice(Port.S1, 9600, timeout=2000)

rightMotor = Motor(Port.A)
leftMotor = Motor(Port.D)

clawMotor = Motor(Port.B)
#tilt = GyroSensor(Port.S1) #Stops is derails??

dist = UltrasonicSensor(Port.S4)
kp = 0.21
travel = 'off'
Motor_input = -150 # pos towards kitchen, neg towards living room

def SL_setup():
    Key = 'bvd8X9LweQY9o2eP1NYL-p8mLL9wMAk6YYOnYSiIo0'
    urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
    headers = {"Accept":"application/json","x-ni-api-key":Key}
    return urlBase, headers   

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

def Get_SL(Tag):
    urlBase, headers = SL_setup()
    urlValue = urlBase + Tag + "/values/current"
    print(urlValue)
    print(headers)
    try:
        value = urequests.get(urlValue,headers=headers).text
        #print(value)
        data = ujson.loads(value)
        #print('data')
        #print(data)
        result = data.get("value").get("value")
        #print(result)
    except Exception as e:
        print(e)
        result = 'failed'
    return result 

def release():
    rightMotor.stop(stop_type=Stop.COAST)
    leftMotor.stop(stop_type=Stop.COAST)
    clawMotor.run_angle(200,-60)
    clawMotor.run_angle(200, 60)
    travel = 'off'
    return travel

def reset():
    rightMotor.reset_angle(0)
    leftMotor.reset_angle(0)
    rightMotor.run_target(200,30*360,wait=False)
    leftMotor.run_target(200,30*360)

def waiting():
    while True:
        if Get_SL('Start08') == 'true':
            travel = 'on'
            break
        if Get_SL('Start08') == 'false':
            wait(10)
            if uart.waiting() >= 1:
                data = uart.read()
                print(data.decode('utf-8'))
    return travel

def cleanUp():
    while True:
        print(dist.distance())
        error = dist.distance() - 500
        Motor_input = -kp*(error)
        rightMotor.run(Motor_input)
        leftMotor.run(Motor_input)
        if error < 10:
            print('Over!')
            reset()
            break
        

travel = waiting()

while travel == 'on':
    if dist.distance() > 150:
        Motor_input = -150
    if dist.distance() <= 150:
        Motor_input = -10
    if uart.waiting() >= 1:
        data = uart.read()
        if data.decode('utf-8') == 'y':
            print('Fire')
            wait(1000)
            release()
            break

    rightMotor.run(Motor_input)
    leftMotor.run(Motor_input)


cleanUp()

#reset to true???
#Put_SL('Start08', 'BOOLEAN', 'true')

# for i in range(10):
#     print(dist.distance())