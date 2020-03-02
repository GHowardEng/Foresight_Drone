
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import math
from ult_sense import *
#from OpticalFlowShowcase import *

webcam = cv2.VideoCapture(0, cv2.CAP_V4L)
#Minimum Image Size 160x120
height = 120
width = 160
webcam.set(3, width)
webcam.set(4, height)
imArea = width * height

class IOpticalFlow:
    '''Interface of OpticalFlow classes'''
    def set1stFrame(self, frame):
        '''Set the starting frame'''
        self.prev = frame
        cv2.imshow("preview", frame)

    def apply(self, frame):
        '''Apply and return result display image (expected to be new object)'''
        result = frame.copy()
        self.prev = frame
        return result

class DenseOpticalFlow(IOpticalFlow):
    '''Abstract class for DenseOpticalFlow expressions'''
    def set1stFrame(self, frame):
        self.prev = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.hsv = np.zeros_like(frame)
        self.hsv[..., 1] = 255

    def apply(self, frame):
        next = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # These are important parameters that determine the function of the algorithm
        flow = cv2.calcOpticalFlowFarneback(self.prev, next, None,
                                            0.5, 3, 10, 3, 5, 1.2, 0)

        result = self.makeResult(frame, flow)
        self.prev = next
        return result

    def makeResult(self, grayFrame, flow):
        '''Replace this for each expression'''
        return frame.copy()


class DenseOpticalFlowByLines(DenseOpticalFlow):
    flowAverage = []
        
    def __init__(self):
        self.step = 16 # configure this if you need other steps...

    def makeResult(self, frame, flow):

       flowSum = cv2.sumElems(flow)
       flowAverage = (flowSum[0] / imArea, flowSum[1] / imArea)

       self.flowAverage = flowAverage

       #vis = cv2.cvtColor(grayFrame, cv2.COLOR_GRAY2BGR)
       cv2.circle(frame, (int(width/2), int(height/2)), 2, (0, 255, 0))
       cv2.arrowedLine(frame, (int(width/2), int(height/2)), (int(width/2 + math.ceil(flowAverage[0]*3)),
                        int(height/2 + math.ceil(flowAverage[1]*3))), (0, 255, 0))
       return frame

def CreateOpticalFlow(type):
    def dense_by_lines():
            
        return DenseOpticalFlowByLines()
    return {
        'dense_lines': dense_by_lines,
    }.get(type, dense_by_lines)()

check, frame = webcam.read()  
of = CreateOpticalFlow('dense_lines')
of.set1stFrame(frame)
ult = ult_sensor()
scale_h = 0.22
scale_w = 0.29

try:
        t_old = time.time()
        while(1):
                check, frame = webcam.read()
                t_new = time.time()
                img = of.apply(frame)
                cv2.imshow("preview", img)
                ult_height = ult.getVert()
                #ult_dist = ult.getHorz()
                vel_x = scale_h * of.flowAverage[0] #* ult_height
                vel_y = scale_w * of.flowAverage[1] #* ult_height
                print("\nX Vel: " + str(vel_x) + " m/frame")
                print("Y Vel: " + str(vel_y) + " m/frame")
                print("Height: " + str(ult_height))
                #print("Distance: " + str(ult_dist))
                t_dif = t_new - t_old
                fps = 1/t_dif
                print("FPS: " + str(fps))
                t_old = t_new
                
                key = cv2.waitKey(1)
                if key == 27:         # exit on ESC
                        print 'Closing...'
                        break


finally:
        webcam.release()
        ult.close()
        print("Closed Safely")
        cv2.destroyAllWindows()

#1m screen height view @456cm drone height - scale = 0.22
#3x4 screen so width = 1.33m @456cm drone height - scale = 0.29
