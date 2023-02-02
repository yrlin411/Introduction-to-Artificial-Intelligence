import os
import cv2

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first
    element is the numpy array of shape (m, n) representing the image.
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    # raise NotImplementedError("To be implemented")

    """
    1) In the directory of parameter dataPath, check further directories, there should be
    one storing images with faces and the other with non-faces.
    2) For every file in the face folder, load it with gray-scale mode, and store its 
    information with classification 1 (which stands for being a face).
    3) Do the same thing as the previous step for the non-face folder.
    4) Return a tuple list "dataset" whose elements are a numpy array representing the image and 
    and the classification of it, indicating if it is a face or not.
    """
    # load all images in folder and make list of tuples
    dataset = []
    for file in os.listdir(dataPath):
        if file == 'face':
            face_path = os.path.join(dataPath, file)
            for face in os.listdir(face_path):
                img = cv2.imread(os.path.join(face_path, face), cv2.IMREAD_GRAYSCALE)
                t = img, 1
                dataset.append(t)
        if file == 'non-face':
            n_face_path = os.path.join(dataPath, file)
            for n_face in os.listdir(n_face_path):
                img = cv2.imread(os.path.join(n_face_path, n_face), cv2.IMREAD_GRAYSCALE)
                t = img, 0
                dataset.append(t)

    return dataset
