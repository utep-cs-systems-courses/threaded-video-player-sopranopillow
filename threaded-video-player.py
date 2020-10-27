#!/usr/bin/env python3

import cv2, os, sys, time
from threading import Thread, Semaphore

class FrameReader(Thread):
    def __init__(self, fl):
        Thread.__init__(self)
        pass
    def run(self):
        print("Frame Reader: Thread running")

class FrameConverter(Thread):
    def __init__(self, fl):
        Thread.__init__(self)
        pass
    def run(self):
        print("Frame Converter: Thread running")

class Consumer(Thread):
    def __init__(self, fl):
        Thread.__init__(self)
        pass
    def run(self):
        print("Consumer: Thread running")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error executing command, usage: ./threaded-video-player.py <clipFilName>.mp4 <outputDirName>")
        sys.exit(1)

    producerQueue = []
    consumerQueue = []
    producerLock
    
    frameReader = FrameReader(fl)
    frameConverter = FrameConverter(fl)
    consumer = Consumer(fl)
    frameReader.start()
    frameConverter.start()
    consumer.start()
