#goal: extract a brick image of set size from video feed

#background subtract/video processing done in 2021

#importing modules
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys
from matplotlib.animation import FuncAnimation

#global variables
paths = []

ksize = (3, 3)
erode_ksize = np.ones((7,7))
filenames = []
img_scale = 300
delay = 500
init_frame_count = 5
ars = []
brick_areas = []
is_brick = False
brick_type = 2 # 1x, 2x, 3x 4x, etc.
hue_tolerance = 200
sat_tolerance = 200
light_tolerance = 200

#functions
def idk(x):
    pass

def getBrick(img, hue, sat, light, bg_img, counts):
    if counts == 0:
        aspect_ratio = 0
        area = 0

    #PREPARE IMAGES
    bg_img = scaleImage(bg_img, img_scale)
    img = scaleImage(img, img_scale)

    #BACKGROUND SUBTRACTION
    background_subtract = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
    #background_image = cv2.convertScaleAbs(background_image, contrast, brightness)
    background_subtract.apply(bg_img)
    sub = background_subtract.apply(img)
    sub = cv2.erode(sub, erode_ksize)

    #CROP TO PART
    #Logic required to deal with the case in which there is no brick in sight
    #print(np.sum(sub))

    if np.sum(sub) > 0:
        (x, y, w, h) = cv2.boundingRect(sub)
        #MAKE ALL IMAGES SQUARE
        if w>h:
            h=w
        elif w<h:
            w=h
        crop = img[y:y + h, x:x + w]
        crop = scaleImage(crop, 300)

        #cv2.rectangle(img, pt1=(x,y), pt2=(x+w, y+h), color=(0, 255, 0), thickness=2)

        #LOCATE CENTER & DETERMINE COLOR OF BRICK

        crop_grey = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        crop_hls = cv2.cvtColor(crop, cv2.COLOR_BGR2HLS)

        cen_x = int(crop_grey.shape[1]/2)
        cen_y = int(crop_grey.shape[0]/2)
        center_color = np.array(crop_hls[cen_y, cen_x]) # value of colored center

        low_hls  = np.array([center_color[0] - hue, center_color[1] - light, center_color[2] - sat])
        hi_hls = np.array([center_color [0]+ hue, center_color[1] + light, center_color[2] + sat])

        #print("center point color value", center_color)

        cv2.circle(crop, (cen_x, cen_y), 2, (255, 0, 0), 5)
        center_value = crop_grey[cen_y, cen_x] # value of grey center

        #COLOR THRESHOLD
        #blur = cv2.blur(crop_grey, ksize)
        thresh = cv2.inRange(crop_hls, low_hls, hi_hls)
        thresh = cv2.erode(thresh, erode_ksize)
        thresh2 = thresh.copy()
        crop2 = crop.copy()

        try:
            contours, hcy = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                #print("area", area)
                if area > 5000:
                    #cv2.drawContours(crop2, [cnt], -1, (255, 0, 0), 4)
                    perimeter = cv2.arcLength(cnt, True)
                    # print('perimeter: ',perimeter)
                    #approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
                    rect = cv2.minAreaRect(cnt)
                    box_points = np.int0(cv2.boxPoints(rect))
                    cv2.drawContours(crop2, [box_points], 0, (255, 0, 0), 4)
                    (x,y),(brick_height, brick_width),angle = rect
                    brick_length = max(brick_width, brick_height)
                    aspect_ratio = round((min(brick_height, brick_width) / max(brick_height, brick_width)), 3)
                    #print("aspect ratio", aspect_ratio)

                    return thresh2, crop2, sub, aspect_ratio, area
        except cv2.error:
            print("Contour detection error")
            aspect_ratio = 0
            area = 0

            return thresh, crop, sub, aspect_ratio, area

    else:

        area = 0

        return None, None, np.zeros((480, 640)), aspect_ratio, area


    # cv2.waitKey(0)


def cropImage(img):
    img_cropped = img[0:1000, 0:1230]
    return img_cropped


def scaleImage(img, width):

    new_width = width / img.shape[1]
    new_size = (width, int(img.shape[0] * new_width)) #size refers to width, height
    img_resize = cv2.resize(img, new_size, interpolation=cv2.INTER_LINEAR)
    return img_resize


def processImages():

    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("The camera isn't open")
        sys.exit()

    #This code created track bars for the various tolerances
    #cv2.namedWindow("window")
    #cv2.createTrackbar("Hue Tolerance", "window", 56, 400, idk)
    #cv2.createTrackbar("Sat Tolerance", "window",100, 400, idk)
    #cv2.createTrackbar("Light Tolerance", "window", 40, 400, idk)

    foreground_old = 0
    frames = 0
    frames_with_brick = 0

    bg = np.zeros((480, 640))
    global is_brick
    while True:

        #Video capture
        ret, frame = cap.read()
        frame = frame[:,:610]
        if not ret:
            print("Cannot obtain frame from camera")
            break

        #Trackbars
        #hue = cv2.getTrackbarPos("Hue Tolerance", "window")
        #light = cv2.getTrackbarPos("Light Tolerance", "window")
        #sat = cv2.getTrackbarPos("Sat Tolerance", "window")

        hue=hue_tolerance
        sat=sat_tolerance
        light=light_tolerance

        if frames >= init_frame_count:
            try:
                thresh, crop, sub, a_ratio, area = getBrick(frame, hue, sat, light, bg, frames_with_brick)

                foreground = np.sum(sub)

                if foreground != 0:
                    #print("brick found")
                    #cv2.imshow("threshold", thresh)
                    #cv2.imshow("cropped", crop)
                    #cv2.imshow("sub", sub)
                    ars.append(a_ratio)
                    brick_areas.append(area)
                    frames_with_brick += 1
                    is_brick = True

                if foreground >= 18000000 or foreground == 0:
                    #print("no brick")
                    bg = frame
                    frames_with_brick = init_frame_count
                    is_brick = False

                #print(foreground)
                cv2.imshow("background", bg)

                foreground_old = foreground
            except TypeError:
                # print("no brick")
                #bg = frame
                frames_with_brick = init_frame_count
                is_brick = False

        if cv2.waitKey(10) == ord('s'):
            cv2.imwrite()

        if cv2.waitKey(1) == 32:
            cv2.destroyAllWindows()
            cap.release()
            break
        #print(frames)
        frames += 1

        cv2.waitKey(delay)


#function call

processImages()




