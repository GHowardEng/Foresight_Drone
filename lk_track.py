#!/usr/bin/env python

'''
Lucas-Kanade tracker
====================

Lucas-Kanade sparse optical flow demo. Uses goodFeaturesToTrack
for track initialization and back-tracking for match verification
between frames.

Usage
-----
lk_track.py [<video_source>]


Keys
----
ESC - exit
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv
from ult_sense import *

#import video
#from common import anorm2, draw_str
from time import clock

lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

class App:
    def __init__(self, vid_feed):
        self.track_len = 10
        self.detect_interval = 5
        self.tracks = []
        #self.cam = video.create_capture(video_src)
        self.cam = vid_feed
        self.frame_idx = 0
        
        self.ult = ult_sensor()
        self.scale_h = 0.22
        self.scale_w = 0.29
        self.t_old = time.time()
        
    
    def run(self):
        while True:
            _ret, frame = self.cam.read()
            #Read the time
            self.t_new = time.time()
            
            height, width = frame.shape[:2]
            height = height/4
            width = width/4
            frame = cv.resize(frame, (int(width),int(height)))
            frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            vis = frame.copy()

            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, st, _err = cv.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                p0r, _st, _err = cv.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
                d = abs(p0-p0r).reshape(-1, 2).max(-1)
                good = d < 1
                new_tracks = []
                
                #Austin added - for storing difference in p1, p0
                velocity = []
                good_new = p1[st==1]
                good_old = p0[st==1]
                if len(good_new) == 0:
                    grab_points = 1
                for i, (new,old) in enumerate(zip(good_new,good_old)):
                    a,b = new.ravel()
                    c,d = old.ravel()
                    velocity.append((a-c,b-d))
                
                vel_avg = average(velocity)
                cv.circle(vis, (width/2, height/2), 2, (0, 255, 0))
                if vel_avg is not None:
                    vel_x, vel_y = vel_avg
                    
                    ult_height = self.ult.getVert()
                    realvel_x = self.scale_h * vel_x * ult_height
                    realvel_y = self.scale_w * vel_y * ult_height
                    print("\nX Vel: " + str(realvel_x) + " m/frame")
                    print("Y Vel: " + str(realvel_y) + " m/frame")
                    print("Height: " + str(ult_height))
                    cv.arrowedLine(vis, (int(width/2), int(height/2)), (int(width/2 + vel_x), int(height/2 + vel_y)), (0, 255, 0))
                
                t_dif = self.t_new - self.t_old
                fps = 1/t_dif
                print("FPS: " + str(fps))
                self.t_old = self.t_new
                ## End
                
                for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                    if not good_flag:
                        continue
                    tr.append((x, y))
                    if len(tr) > self.track_len:
                        del tr[0]
                    new_tracks.append(tr)
                    #cv.circle(vis, (x, y), 2, (0, 255, 0), -1)
                self.tracks = new_tracks
                #cv.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))
                #draw_str(vis, (20, 20), 'track count: %d' % len(self.tracks))

            if self.frame_idx % self.detect_interval == 0 or grab_points:
                mask = np.zeros_like(frame_gray)
                grab_points = 0
                mask[:] = 255
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv.circle(mask, (x, y), 5, 0, -1)
                p = cv.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x, y)])


            self.frame_idx += 1
            self.prev_gray = frame_gray
            cv.imshow('lk_track', vis)
            ch = cv.waitKey(1)
            if ch == 27:
                self.ult.close()
                break

def main():
    import sys
    try:
        #video_src = sys.argv[1]
        vf = cv.VideoCapture(0)
        print("Video Capture setup")
    except Exception as e:
        print(e)
    
    App(vf).run()
    vf.release()
    print('Done')

def average(vel):
    try:
        divisor = len(vel)
        if divisor > 0:
            x_tot = 0
            y_tot = 0

            for i in range(divisor):
                pair = vel[i]
                x = pair[0]
                y = pair[1]
                x_tot += x
                y_tot += y
            
            x_avg = x_tot/divisor
            y_avg = y_tot/divisor
            #print("X Vel: " + str(x_avg) + "  Y Vel: " + str(y_avg))
            vel_avg = (x_avg,y_avg)
            return vel_avg
        else:
            return None
            
    except Exception as e:
        print(e)

if __name__ == '__main__':
    print(__doc__)
    main()
    cv.destroyAllWindows()
