#!/usr/bin/env python3

import cv2, os, sys, time
import numpy as np
from threading import Thread, Semaphore, Lock

class FrameReader(Thread): # Producer
    def __init__(self, fl, debug):
        Thread.__init__(self)
        self.vidcap = cv2.VideoCapture(fl)
        self.frames = int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))-1
        self.count = 0
        self.debug = debug

    def run(self):
        if debug: print("Frame Reader: Thread running")

        global producerQueue, producerLock
        success, img = self.vidcap.read()

        if debug: print(f'Frame Reader: Reading frame {self.count} {success}')
        while success and self.count < self.frames:
            producerLock.acquire()
            producerQueue.insert(0, img)
            producerLock.release()
            success, img = self.vidcap.read()
            self.count += 1
            if debug: print(f'Frame Reader: Reading frame {self.count} {success}')
        producerLock.acquire()
        producerQueue.insert(0, True)
        producerLock.release()
            

class FrameConverter(Thread): # Producer and Consumer
    def __init__(self, debug):
        Thread.__init__(self)
        self.debug = debug
        self.count = 0

    def run(self):
        if debug: print("Frame Converter: Thread running")
        global consumerQueue, producerQueue

        while True:
            if len(producerQueue) > 0:
                producerLock.acquire()
                img = producerQueue.pop()
                producerLock.release()
                if type(img) == bool and img:
                    break
                gs_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                consumerLock.acquire()
                consumerQueue.insert(0, gs_img)
                consumerLock.release()
        consumerLock.acquire()
        consumerQueue.insert(0, True)
        consumerLock.release()

class FrameDisplay(Thread): # Consumer 
    def __init__(self, delay, debug):
        Thread.__init__(self)
        self.debug = debug
        self.delay = delay
        
    def run(self):
        if debug: print("Frame Display: Thread running")
        # Globals
        global consumerQueue

        while True:
            if len(consumerQueue) > 0:
                consumerLock.acquire()
                img = consumerQueue.pop()
                consumerLock.release()
                if type(img) == bool and img:
                    break
                if cv2.waitKey(self.delay) and 0xFF == ord("q"):
                    break
                cv2.imshow('Video', img)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error executing command, usage: ./threaded-video-player.py <clipFilName>.mp4 <debug; y : n : \"\">")
        sys.exit(1)

    fl = sys.argv[1]
    if len(sys.argv) == 3 and sys.argv[2] == "y":
        debug = True
    else:
        debug = False

    delay = 30
        
    producerQueue = []
    consumerQueue = []

    producerLock = Lock()
    consumerLock = Lock()

    frameReader = FrameReader(fl, debug)
    frameConverter = FrameConverter(debug)
    frameDisplay = FrameDisplay(delay, debug)
    frameReader.start()
    frameConverter.start()
    frameDisplay.start()
