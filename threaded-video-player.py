#!/usr/bin/env python3

import cv2, os, sys, time

if len(sys.argv) < 3:
    print("Error executing command, usage: ./threaded-video-player.py <clipFilName>.mp4 <outputDirName>")

#globals
outputDir = sys.argv[2]
clipFileName = sys.argv[1]
frameDelay = 42

#frame count
count = 0

#open video clip
vidcap = cv2.VideoCapture(clipFileName)
numberOfFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

#create the output directory if it doesn't exist
if not os.path.exists(outputDir):
    print(f"Output directory {outputDir} didn't exist, creating")
    os.makedirs(outputDir)

#read one frame
success, frame = vidcap.read()

print(f'Reading frame {count} {success}')

while success and count < numberOfFrames:
    #convert to grayscale
    grayscaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    
    #write the current frame out as a jpeg image
    cv2.imwrite(f"{outputDir}/frame_{count:04d}.bmp", grayscaleFrame)

    success, frame = vidcap.read()
    print(f'Reading frame {count}')
    count += 1


count = 0
frameFileName = f'{outputDir}/grayscale_{count:04d}.bmp'
frame = cv2.imread(frameFileName)

while frame is not None:
    print(f'Displaying frame {count}')

    cv2.imshow('Video', frame)

    if cv2.waitKey(frameDelay) and 0xFF == ord("q"):
        break

    count+=1
    frameFileName = f'{outputDir}/grayscale_{count:04d}.bmp'

    frame = cv2.imread(frameFileName)

cv2.destroyAllWindows()
