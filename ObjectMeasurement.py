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
scale_factor = 3 # factor in which we scale up the image
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
    # if we found an object
    if len(contours) != 0:
        biggest = contours[0][2] # get the largest contour
        # shift perspective to top-down view
        perspectiveShift = utils.warpImage(image, biggest, bg_width, bg_height, pad=20)
        # Find objects on the background
        detectedImages, detectedContours = utils.getCountours(perspectiveShift, minArea=2000, maxArea= 160000, filter=4,
                                                              cannyThreshold=[40, 40])
        # if we found an object
        if len(detectedContours) != 0:
            for obj in detectedContours:
                # draw solid lines around detected images
                cv2.polylines(detectedImages, [obj[2]], True, (0, 165, 255), 2)
                # obj is currently not in the correct order, reorder the points
                obj_points = utils.reorder(obj[2])
                # calculate the distance using the scale factor
                length = round(utils.getDistance(obj_points[0][0]//scale_factor, obj_points[1][0]//scale_factor)/10, 1)
                height = round(utils.getDistance(obj_points[0][0]//scale_factor, obj_points[2][0]//scale_factor)/10, 1)
                # draw the lines
                lengthStart = (obj_points[2][0][0], obj_points[2][0][1])
                lengthEnd = (obj_points[3][0][0], obj_points[3][0][1])
                cv2.arrowedLine(perspectiveShift, lengthStart, lengthEnd, (0, 255, 0), 3, 8, 0, 0.05)
                heightStart = (obj_points[2][0][0], obj_points[2][0][1])
                heightEnd = (obj_points[0][0][0], obj_points[0][0][1])
                cv2.arrowedLine(perspectiveShift, heightStart, heightEnd, (0, 255, 0), 3, 8, 0, 0.05)
                # write the length and height to the screen
                x, y, l, h = obj[3]
                cv2.putText(perspectiveShift, '{}cm'.format(length), (x + l // 2, y + h + 15),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(perspectiveShift, '{}cm'.format(height), (x - 70, y + h // 2),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2, cv2.LINE_AA)
        # show the final result
        cv2.imshow('Background focus', perspectiveShift)


    # show the original image
        # TODO: draw lines on original image here
    image = cv2.resize(image, (1920, 1080), interpolation=cv2.INTER_AREA)
    cv2.imshow('Webcam Source', image)

    key = cv2.waitKey(1)
    # Press Q on keyboard to exit
    if key & 0xFF == ord('q'):
        break
