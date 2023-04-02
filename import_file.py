from GUI import GUI
from HAL import HAL
import numpy as np
import cv2
import time
# Enter sequential code!

LOW_HEIGHT = 330
UP_HEIGHT = 300

KP = -0.0018
KI = -0.002
KD = -0.005

class PID_Controller:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.last_error = 0
        self.diff = 0
        self.last_time = 0
        self.delta_t = 0
        self.current_time = 0
    
    def controll(self, error):
        self.current_time = time.time()
        if self.last_time != 0:
            self.delta_t = (self.current_time - self.last_time)
            print("delta t", self.delta_t)
        self.last_time = self.current_time
        self.integral += error*self.delta_t
        if self.delta_t != 0:
            self.diff = (error - self.last_error)/self.delta_t
        self.last_error = error
        return self.kp*error + self.ki*self.integral + self.kd*self.diff

pid_controller = PID_Controller(KP, KI, KD)

while True:
    img = HAL.getImage()
    # GUI.showImage(img)
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    
    mask = cv2.inRange(img_hsv, lower_red, upper_red)
    mask[:][:UP_HEIGHT] = np.zeros_like(mask[:][:UP_HEIGHT])
    mask[:][LOW_HEIGHT:] = np.zeros_like(mask[:][LOW_HEIGHT:])
    
    img_result = cv2.bitwise_and(img, img, mask=mask)
    GUI.showImage(img_result)
    
    up_line = mask[:][UP_HEIGHT]
    
    start_red = 0
    end_red = len(up_line)
    
    for i in range(len(up_line)):
        if up_line[i] > 10:
            start_red = i
            break
    
    for i in reversed(range(len(up_line))):
        if up_line[i] > 10:
            end_red = i
            break
    
    center_red = (start_red + end_red)//2
    
    error = center_red - len(up_line)//2
    
    W = pid_controller.controll(error)
    print("error: ",error)
    print(pid_controller.integral)
    print(pid_controller.diff)
    
    HAL.setV(3)
    HAL.setW(W)
    
    
    
    
    
    
    
