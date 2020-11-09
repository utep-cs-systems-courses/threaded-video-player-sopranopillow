#!/usr/bin/env python3

import cv2, os, sys, time
import numpy as np
from threading import Thread, Semaphore, Lock

class ProducerConsumerQueue():
    def __init__(self, limit):
        self.limit = limit
        # Producer setup
        self.producerQ = []
        self.producerS = Semaphore(limit)
        self.producerL = Lock()
        # Consumer setup
        self.consumerQ = []
        self.consumerS = Semaphore(limit)
        self.consumerL = Lock()

    def producerEmpty(self):
        return not len(self.producerQ) > 0

    def consumerEmpty(self):
        return not len(self.consumerQ) > 0
        
    def pushProducer(self, value):
        self.pushQ(value)

    def pushConsumer(self, value):
        self.pushQ(value, False)

    def popProducer(self):
        return self.popQ()

    def popConsumer(self):
        return self.popQ(False)
        
    # Using value as general name since the producer/consumer Queue data structure can be reused
    # This is an "internal" method, it's just to make the code a little simpler
    def pushQ(self, value, producer = True): 
        # Acquiring from semaphore
        if producer: self.producerS.acquire()
        else: self.consumerS.acquire()
        # Acquiring lock
        if producer: self.producerL.acquire()
        else: self.consumerL.acquire()
        # Pushing value into queue
        if producer: self.producerQ.insert(0, value)
        else: self.consumerQ.insert(0, value)
        # Releasing lock
        if producer: self.producerL.release()
        else: self.consumerL.release()

    # This is an "internal" method, it's just to make the code a little simpler
    def popQ(self, producer = True):
        # Releasing from semaphore
        if producer: self.producerS.release()
        else: self.consumerS.release()
        # Acquring lock
        if producer: self.producerL.acquire()
        else: self.consumerL.acquire()
        # poping last element but not returning right away since lock needs to be released
        if producer:
            value = self.producerQ.pop()
        else:    
            value = self.consumerQ.pop()
        # Releasing lock
        if producer: self.producerL.release()
        else: self.consumerL.release()
        return value
    
class FrameReader(Thread): # Producer
    def __init__(self, fl, debug):
        Thread.__init__(self)
        self.vidcap = cv2.VideoCapture(fl) # Creating video capture object to read frames
        self.frames = int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))-1 # Getting number of frames but subtracting one since we start from 0
        self.count = 0
        self.debug = debug

    def run(self):
        if self.debug: print("Frame Reader: Thread running")

        # Getting producer consumer queue
        global pcQ
        success, img = self.vidcap.read()

        if debug: print(f'Frame Reader: Reading frame {self.count} {success}')

        while success and self.count < self.frames:
            # Pushing into producer queue
            pcQ.pushProducer(img)
            success, img = self.vidcap.read() # getting frame from video clip
            self.count += 1
            if self.debug: print(f'Frame Reader: Reading frame {self.count} {success}')
        pcQ.pushProducer(True) # Letting converter know that we're done getting the frames
            

class FrameConverter(Thread): # Producer and Consumer
    def __init__(self, debug):
        Thread.__init__(self)
        self.debug = debug
        self.count = 0

    def run(self):
        if self.debug: print("Frame Converter: Thread running")

        # Getting producer consumer queue
        global pcQ

        while True:
            if not pcQ.producerEmpty():
                if self.debug: print(f'Processing frame {self.count}')
                img = pcQ.popProducer() # Getting image from producer queue to convert to gray scale
                if type(img) == bool and img: # Checking type looks ugly but it works to know when we're done
                    break
                gs_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converting image to grayscale
                pcQ.pushConsumer(gs_img) # Pushing new grayscale image into the consumer queue
                self.count += 1
        pcQ.pushConsumer(True) # Letting displayer know that we're done processing frames

class FrameDisplay(Thread): # Consumer 
    def __init__(self, delay, debug):
        Thread.__init__(self)
        self.debug = debug
        self.delay = delay
        self.count = 0
        
    def run(self):
        if debug: print("Frame Display: Thread running")
        
        # Getting producer consumer queue
        global pcQ

        while True:
            if not pcQ.consumerEmpty():
                if self.debug: print(f'Displaying frame {self.count}') 
                img = pcQ.popConsumer() # Getting frame
                if type(img) == bool and img: # Checking if we are done displaying frames, checking the type look ugly but works good
                    break
                if cv2.waitKey(self.delay) and 0xFF == ord("q"): # Checking for delay or quit
                    break
                cv2.imshow('Video', img) # Displaying frame
                self.count += 1 
        cv2.destroyAllWindows() # Closing all windows

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error executing command, usage: ./threaded-video-player.py <clipFilName>.mp4 <debug; y : n : \"\">")
        sys.exit(1)

    if len(sys.argv) == 3 and sys.argv[2] == "y":
        debug = True
    else:
        debug = False

    fl = sys.argv[1] # File that will be processed
    delay = 30 # Delay when displaying frames
    limit = 30 # Limits the amount of items per queue
        
    pcQ =  ProducerConsumerQueue(limit) # Creating producer consumer queue

    # Creating reader, converter, and displayer
    frameReader = FrameReader(fl, debug)
    frameConverter = FrameConverter(debug)
    frameDisplay = FrameDisplay(delay, debug)

    # Starting processes
    frameReader.start()
    frameConverter.start()
    frameDisplay.start()
