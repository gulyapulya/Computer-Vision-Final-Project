import cv2
import numpy as np


def getContours(img, cannyThreshold=[100, 250], showResult=False, minArea = 0, maxArea = 100, filter = 0, draw=False):
    '''
    Takes an image and returns an array of all contours found within that image sorted by size of the contour
    :param img: source image
    :param cannyThreshold: canny threshold
    :param showResult: Bool - displays the result of the function as an image
    :param minArea: int (out of 100) - minimum percent of image area to accept as a contour
    :param maxArea: int (out of 100) - maximum percent of image area to accept as a contour
    :param filter: int - number of corners
    :param draw: Bool - draw the contours identified on the source image
    :return: the sorted array of contours
    '''

    # convert to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur the image
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    # apply canny edge detector
    imgCanny = cv2.Canny(imgBlur, cannyThreshold[0], cannyThreshold[1])
    kernel = np.ones((5, 5))
    # smoothen the lines detected
    imgDial = cv2.dilate(imgCanny, kernel, iterations=3)
    imgThreshold = cv2.erode(imgDial, kernel, iterations=2)

    # display the result of the function
    if showResult:
        cv2.imshow('Edges image', imgThreshold)

    # get the contours and process
    contours, _ = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ret = []
    for contour in contours:
        img_w, img_h, _ = img.shape
        area = cv2.contourArea(contour) / (img_w * img_h) * 100
        #check if it is big enough and does not cover more than needed
        if minArea < area < maxArea:
            perimeter = cv2.arcLength(contour, True)
            cornerPoints = cv2.approxPolyDP(contour, 0.02*perimeter, True)
            #check number of corners
            if filter > 0 and len(cornerPoints) != filter:
                continue
            boundingBox = cv2.minAreaRect(cornerPoints)
            ret.append([len(cornerPoints), area, cornerPoints, boundingBox, contour])
    
    # sort the return values based on the area of the contour found
    ret = sorted(ret, key=lambda x: x[1], reverse=True)
    if draw:
        for contour in ret:
            # draw the contour outline in red with a line thickness of 3
            cv2.drawContours(img, contour[4], -1, (0,0,255), 3)
    return ret


def reorder(points):
    '''
    Reorder the points such that they are in the form
    1....2
    .    .
    .    .
    3....4
    :param points: input points
    :return: formatted points
    '''
    # copy the structure of the input type
    returnPoints = np.zeros_like(points)
    # we only care about the elements which contain our 4 corner values and our 2 x,y co-ordinates
    points = points.reshape((4,2))
    # use the summation principle to find the first and 4th point (top left and bottom right)
    mySum = points.sum(1)
    returnPoints[0] = points[np.argmin(mySum)]
    returnPoints[3] = points[np.argmax(mySum)]
    # use the difference principle to find the 2nd and 3rd point (top right and bottom left)
    myDiff = np.diff(points, axis=1)
    returnPoints[1] = points[np.argmin(myDiff)]
    returnPoints[2] = points[np.argmax(myDiff)]
    return returnPoints

def warpImage(img, points, width, height, pad=0):
    '''
    Shifts perspective of an image to straight-on view
    :param img: source image
    :param points: corner points
    :param width: output width
    :param height: output height
    :param pad: padding to remove
    :return: warped image
    '''
    # reorder the points in the correct orientation
    points = reorder(points)
    # create the perspective
    input_points = np.float32(points)
    output_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(input_points, output_points)
    # warp based on the perspective
    imgWarp = cv2.warpPerspective(img, matrix, (width, height))
    imgWarp = imgWarp[pad:imgWarp.shape[0] - pad, pad:imgWarp.shape[1]-pad]
    return imgWarp

def drawMeasurements(img, points, width, height):
    '''
    Draws measurements around the object
    :param img: image to draw on
    :param points: rotated rectangle coordinates
    :param width: rotated rectangle width
    :param height: rotated rectangle height
    '''
    # draw the lines
    cv2.drawContours(img, [points], 0, (0, 255, 0), 2)
    #draw measurements
    #check if square
    if min(width, height) / max(width, height) > 0.95:
        avg = round(np.average([width, height]), 1)
        cv2.putText(img, '{}cm'.format(avg), (points[0][0], points[0][1]),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (189, 159, 0), 1, cv2.LINE_AA)
    else:
        cv2.putText(img, '{}cm x {}cm'.format(width, height), (points[0][0], points[0][1]),
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (189, 159, 0), 1, cv2.LINE_AA)


def convertCoordinates(coordinates, points, width, height, pad=0):
    '''
    Converts coordinates from transformed to original 
    :param coordinates: array of coordinates from transformed image
    :param points: corner points of original
    :param width: transformed width
    :param height: transformed height
    :return: array of corresponding coordinates
    '''
    # reorder the points in the correct orientation
    points = reorder(points)
    # identify the forward trasnform
    input_points = np.array(np.float32(points))
    output_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(input_points, output_points)
    # Reverse the transform
    inv_matrix = np.linalg.pinv(matrix)
    coordinates = np.float32(np.array([coordinates]) + pad)    
    converted_coordinates = cv2.perspectiveTransform(coordinates, inv_matrix)[0]
    converted_coordinates = np.int0(converted_coordinates)
    return converted_coordinates

