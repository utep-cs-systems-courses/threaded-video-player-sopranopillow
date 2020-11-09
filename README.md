# Producer Consumer Lab

## Use
To use the threaded video player, these are the following commands:

`$ ./threaded-video-player.py <clip>.mp4 <y : n : "">`

The first parameter is the name of the video clip to use and the second parameter is if you want to show debug messages. The third parameter can be omitted and will default to not show any messages.

#### Note: the amount of delay was changed to 30 and the limit per queue as well, this is mainly to be able to look at a smooth video. These settings can be changed by going in the code and changing the values in the main.

---

For this lab you will implement a trivial producer-consumer system using
python threads where all coordination is managed by counting and binary
semaphores for a system of two producers and two consumers. The producers and
consumers will form a simple rendering pipeline using multiple threads. One
thread will read frames from a file, a second thread will take those frames
and convert them to grayscale, and the third thread will display those
frames. The threads will run concurrently.

In order to run this lab opencv will need to be installed. To install opencv
use the follwing commands (note that ordering is important):

    sudo zypper -n install python3-devel
    sudo zypper -n install ffmpeg ffmpeg-3
    sudo zypper -n install gstreamer gstreamer-devel
    sudo zypper -n install python3-numpy
    sudo pip install --upgrade pip
    sudo pip install opencv-python

## Allowed libraries
The purpose of this lab is to implement and use a producer-consumer system.
Python already has several synchronized bounded buffers and queues available 
as libraries. You *may not* use any of these as they would prevent you from 
demonstrating the knowledge you've gained. The only threading/synchronization
objects or methods you may use are mutexes and semaphores (we suggest using
the threads api).

## File List
### ExtractFrames.py
Extracts a series of frames from the video contained in 'clip.mp4' and saves 
them as jpeg images in sequentially numbered files with the pattern
'frame_xxxx.jpg'.

### ConvertToGrayscale.py
Loads a series for frams from sequentially numbered files with the pattern
'frame_xxxx.jpg', converts the grames to grayscale, and saves them as jpeg
images with the file names 'grayscale_xxxx.jpg'

### DisplayFrames.py
Loads a series of frames sequently from files with the names
'grayscale_xxxx.jpg' and displays them with a 42ms delay.

### ExtractAndDisplay.py
Loads a series of framss from a video contained in 'clip.mp4' and displays 
them with a 42ms delay

## Requirements
* Extract frames from a video file, convert them to grayscale, and display
them in sequence
* You must have three functions
  * One function to extract the frames
  * One function to convert the frames to grayscale
  * One function to display the frames at the original framerate (24fps)
* The functions must each execute within their own python thread
  * The threads will execute concurrently
  * The order threads execute in may not be the same from run to run
* Threads will need to signal that they have completed their task
* Threads must process all frames of the video exactly once
* Frames will be communicated between threads using producer/consumer idioms
  * Producer/consumer qeueus must be bounded at ten frames

Note: You may have ancillary objects and method in order to make you're code easer to understand and implement.



