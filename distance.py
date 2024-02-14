import cv2
import imutils

def find_marker(image, known_width, known_height):
    # convert the image to grayscale, blur it, and detect edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # adjust the parameters of cv2.Canny according to your image
    edged = cv2.Canny(blurred, 50, 150)

    cv2.imshow('Preto e Branco', edged)
    
    # find the contours in the edged image and filter based on aspect ratio
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Filter contours based on aspect ratio
    filtered_cnts = [cnt for cnt in cnts if is_contour_valid(cnt, known_width, known_height)]
    
    # Assume the largest contour is our piece of paper in the image
    c = max(filtered_cnts, key=cv2.contourArea, default=None)
    
    if c is not None:
        # compute the bounding box of the paper region and return it
        return cv2.minAreaRect(c)
    else:
        return None

def is_contour_valid(cnt, known_width, known_height, aspect_ratio_threshold=0.2):
    # Compute aspect ratio of the contour
    (x, y, w, h) = cv2.boundingRect(cnt)
    aspect_ratio = float(w) / h

    # Compare aspect ratio with the threshold
    return abs(aspect_ratio - (known_width / known_height)) < aspect_ratio_threshold

def distance_to_camera(known_width, focal_length, per_width):
    return (known_width * focal_length) / per_width

def existsInList(item):
    global qrcode_items_reads
    global qrcode_location_reads

    for code in qrcode_items_reads:
        if (item == code):
            return True
    
    for code in qrcode_location_reads:
        if (item == code):
            return True
    return False

def isCorrectPosition(id, name):
    global correct_items

    for item in correct_items:
        if item[0] == id and item[1] == name:
            return True
    return False

KNOWN_DISTANCE = 950.0
KNOWN_HEIGHT = 210.0
KNOWN_WIDTH = 297.0

image = cv2.imread("C:/tello/Webcam/95.jpg")
marker = find_marker(image, KNOWN_WIDTH, KNOWN_HEIGHT)
focal_length = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH