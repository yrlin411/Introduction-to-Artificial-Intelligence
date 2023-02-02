import os
import cv2
import matplotlib.pyplot as plt

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    """
    1) Read the txt file, and load the image
    2) By the given number, store the left-up coordinate and the width and the height
    3) Crop the image by the coordinates and convert it into a gray-scale image
    4) Use the "classify" function to test the cropped image, if the function returns 1,
    it shall be a face therefore box it with a green rectangle, otherwise red.  
    5) Check the image with imshow
    """
    # read the txt file
    file = open(dataPath, 'r')
    for line in file:
        img = cv2.imread(os.path.join('data/detect', line.split()[0]))
        for i in range(int(line.split()[1])):
            data = file.readline().split()
            x = int(data[0])
            y = int(data[1])
            w = int(data[2])
            h = int(data[3])
            # crop the faces
            crop = img[y:y+h, x:x+w]
            crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            crop = cv2.resize(crop, (19, 19), interpolation=cv2.INTER_AREA)
            if clf.classify(crop) == 1:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            else:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.imshow('With Box', img)
        cv2.waitKey(0)
    # raise NotImplementedError("To be implemented")
    # End your code (Part 4)
