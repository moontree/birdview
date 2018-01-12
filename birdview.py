import cv2
import numpy as np
import matplotlib.pyplot as plt
import json

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

def read_params_from_file(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        mtx = np.array(data['mtx'])
        dist = np.array(data['dist'])
        newcameramtx = np.array(data['newcameramtx'])
        transformmtx = np.array(data['transformmtx'])
    return mtx, dist, newcameramtx, transformmtx

mtx, dist, newcameramtx, transformmtx = read_params_from_file('back.json_final')

while True:
    ret, frame = cap.read()
    target = np.zeros([810, 600, 3], dtype=np.uint8)
    ### undistort
    dst = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    ### undistort

    ### transpose
    bird = np.zeros([810, 600, 3], dtype=np.uint8)
    bird_view = cv2.warpPerspective(dst, transformmtx, (600, 810))
    print bird_view.shape
    print bird_view[540:].shape
    print bird_view[540:].shape
    target[540:] = cv2.bitwise_or(target[540:], bird_view[540:])
    # dst = cv2.resize(dst, (400, 540))
    cv2.imshow('ori', frame)
    cv2.imshow('undisorted', dst)
    cv2.imshow('birdview', target)
    cv2.waitKey(1)

