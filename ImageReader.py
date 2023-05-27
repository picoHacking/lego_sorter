import cv2
import numpy as np
import time
import configparser
import os
from datetime import date

#Image average calibration
def ImageAverageCalibration():
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    avg_color_list = []

    timeout_start = time.time()

    while time.time() < 10 + timeout_start:
        ret, frame = cap.read()
        if not ret:
            print("Can not read camera stream! Go to line 10 in ImageReader.py and change 1 to 0.  If fail then \n stream corrupt!")
            exit()
        avg_color_per_row = np.average(frame, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        avg_color_list.append(avg_color)
        cv2.waitKey(1)
    colorAverage = np.average(avg_color_list)
    #print(avg_color_list)
    #print(colorAverage)
    cap.release()
    return(colorAverage)

def GetTestImage():
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    avg_color_per_row = np.average(frame, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    cv2.waitKey(1)
    colorAverage = np.average(avg_color)
    cap.release()
    return(colorAverage)

def SaveImage(frame):
    counter = 1

    if not os.path.isdir('images/' + str(date.today())):
        os.mkdir('images/' + str(date.today()))
    savepath = 'images/' + str(date.today()) + '/'
    TryPath = savepath + 'image' + str(counter) + '.jpg'
    while os.path.isfile(TryPath):
        counter += 1
        TryPath = savepath + 'image' + str(counter) + '.jpg'
    cv2.imwrite(TryPath, frame)

def Run():
    #open the config file and store the value for MinimumTolerance as a variable.
    config = configparser.ConfigParser()
    config.read('config.ini')
    MinimumTolerance = config.getfloat('Calibration', 'Minimum Tolerance')
    EmptyAverage = config.getfloat('Calibration', 'Color Average')
    LagTime = config.getfloat('Settings', 'Lag Time')
    CameraSource = config.getint('Settings', 'Camera Source')

    cap = cv2.VideoCapture(CameraSource)
    i = 1
    LastImage = 0
    IsSearching = True
    while True:
        #Get video stream and wait for a frame to exceed tolerance.
        while IsSearching:
            ret, frame = cap.read()
            if not ret:
                print("""Error: Video stream is corrupt or camera is not on. \n If this problem persists
                change 'video_source' in config.ini to 0 or 1, whatever it currently is not, or reinstall ffmpeg""")
                print("Press enter to exit.")
                input()
                exit()
            #Determine if the current image exceeds the minimum tolerance
            avg_color_per_row = np.average(frame, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            colorAverage = np.average(avg_color)
            if colorAverage > abs(MinimumTolerance) + EmptyAverage or colorAverage < EmptyAverage - abs(MinimumTolerance):
                #print("Found Object!")
                #print(str(colorAverage))
                IsSearching = False
    


        #Once a frame has exceeded tolerance, wait for the lag time to pass so that the object is centered
        #print("Moving to save.")
        time.sleep(LagTime)
        ret, frame = cap.read()
        if not ret:
                print("""Error: Video stream is corrupt or camera is not on. \n If this problem persists
                change 'video_source' in config.ini to 0 or 1, whatever it currently is not, or reinstall ffmpeg""")
                print("Press enter to exit.")
                input()
                exit()
        cv2.imwrite("image" + str(i) + ".jpg", frame)
        cv2.waitKey(1)
        i + 1
        SaveImage(frame)
        #print("Saved image.  Remove object NOW!")
        #Wait for object to exit frame.
        time.sleep(LagTime + 2) #Edit the modifier if you keep getting duplicates.
        IsSearching = True