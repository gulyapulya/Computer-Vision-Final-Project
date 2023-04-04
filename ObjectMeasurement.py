import cv2
import numpy as np
import utils

webcam = True
image_path = './assets/image.jpg'
# Webcam capture settings
capture = cv2.VideoCapture(0)
# brightness
capture.set(10, 160)
# width
capture.set(3, 1920)
# height
capture.set(4, 1080)
# background size
scale_factor = 3
letter_paper_length = 280
letter_paper_width = 216
bg_width = letter_paper_length * scale_factor
bg_height = letter_paper_width * scale_factor



torun = True;
while torun:
    if webcam:
        success, image = capture.read()
    else:
        image = cv2.imread(image_path)
    # get the outline of the background
    image, contours = utils.getCountours(image, minArea=60000, filter=4, draw=True)
    if len(contours) != 0:
        biggest = contours[0][2] # get the largest contour
        # shift perspective to top-down view
        perspectiveShift = utils.warpImage(image, biggest, bg_width, bg_height, pad=20)

        detectedImages, detectedContours = utils.getCountours(perspectiveShift, minArea=2000, maxArea= 160000, filter=4,
                                                              cannyThreshold=[40,40])

        if len(detectedContours) != 0:
            for obj in detectedContours:
                # draw solid lines around detected images
                cv2.polylines(detectedImages, [obj[2]], True, (0, 165, 255), 2)
        cv2.imshow('Background focus', perspectiveShift)


    # show the original image
    image = cv2.resize(image, (1920, 1080), interpolation=cv2.INTER_AREA)
    cv2.imshow('Webcam Source', image)

    key = cv2.waitKey(1)
    # Press Q on keyboard to exit
    if key & 0xFF == ord('q'):
        break
