from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15
camera.start_preview()
#camera.capture('/home/pi/Desktop/new.jpg')
time.sleep(15)
camera.stop_preview()