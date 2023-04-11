import cv2
import numpy as np
import utils
import config

webcam = False
image_path = './assets/samples/straight_no_shadow.jpg'
# Webcam capture settings
capture = cv2.VideoCapture(0)
# brightness
capture.set(10, 160)
# width
capture.set(3, config.frame_w)
# height
capture.set(4, config.frame_h)
# background size
scale_factor = config.scale # factor in which we scale up the image
letter_paper_length = config.background_w
letter_paper_width = config.background_h
bg_width = letter_paper_length * scale_factor
bg_height = letter_paper_width * scale_factor



torun = True;
while torun:
    if webcam:
        success, image = capture.read()
    else:
        image = cv2.imread(image_path)
    # get the outline of the background
    bg_contours = utils.getContours(image, minArea=10, filter=4, draw=True)
    # if we found an object
    if len(bg_contours) != 0:
        bg_biggest_corners = bg_contours[0][2] # get the largest contour
        cv2.drawContours(image, bg_biggest_corners, 0,(0,0,255),2)
        # shift perspective to top-down view
        perspectiveShift = utils.warpImage(image, bg_biggest_corners, bg_width, bg_height, pad=20)
        # Find objects on the background
        obj_contours = utils.getContours(perspectiveShift, showResult=True, minArea=0.1, maxArea= 95, cannyThreshold=[40, 40])
        # if we found an object
        if len(obj_contours) != 0:
            for n_corners, area, cornerPoints, boundingBox, contour in obj_contours:
                #get measurements from building boxq
                points = cv2.boxPoints(boundingBox)
                points = np.int0(points)
                (cx, cy), (w, h), angle = boundingBox
                # get width and height in cm
                width = round(w / config.scale / 10, 1)
                height = round(h / config.scale / 10, 1)
                utils.drawMeasurements(perspectiveShift, points, width, height)
                #draw on original image
                orig_points = utils.convertCoordinates(points, bg_biggest_corners, bg_width, bg_height, pad=20)
                utils.drawMeasurements(image, orig_points, width, height)
        # show the final result
        cv2.imshow('Background focus', perspectiveShift)

    # show the original image
        # TODO: draw lines on original image here
    image = cv2.resize(image, (1008, 756), interpolation=cv2.INTER_AREA)
    cv2.imshow('Webcam Source', image)

    key = cv2.waitKey(1)
    # Press Q on keyboard to exit
    if key & 0xFF == ord('q'):
        break
