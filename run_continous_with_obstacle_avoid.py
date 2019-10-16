#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from AMSpi import AMSpi
import time
import RPi.GPIO as GPIO


def distance_reading():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return int(float(distance))

def run_robot():
    with AMSpi() as amspi:
        # Set PINs for controlling shift register (GPIO numbering)
        amspi.set_74HC595_pins(21, 20, 16)
        
        # Set PINs for controlling all 4 motors (GPIO numbering)
        amspi.set_L293D_pins(5, 6, 13, 19)
        while True:
            dist_sensor = distance_reading()
            if dist_sensor >= 23.4:
                print (dist_sensor)
                amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
            else:
                amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
                amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_3])
                amspi.run_dc_motors([amspi.DC_Motor_2, amspi.DC_Motor_4], clockwise=False)
                print ("Turning Right")

if __name__ == '__main__':
    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
     
    #set GPIO Pins
    GPIO_TRIGGER = 17
    GPIO_ECHO = 27
     
    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    
    run_robot()
