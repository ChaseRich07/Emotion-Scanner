from deepface import DeepFace
import cv2
import os.path
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image as im
from app import upload_file, UPLOAD_FOLDER

directory = os.path.dirname(os.path.abspath(__file__))
imgs = []
face = UPLOAD_FOLDER
path = os.path.join(directory, face)
valid_file_types = [".jpg", ".png", ".jpeg"]

for file in os.listdir(path):
    print(file)
    ext = os.path.splitext(file)[1]
    if ext.lower() not in valid_file_types:
        print ("not valid")
        continue
    print (ext)
    img = cv2.imread(os.path.join(path, file))
    image_face = DeepFace.detectFace(img)
    plt.imshow(image_face, interpolation='nearest')
    for image_face in img:
        plt.show()
