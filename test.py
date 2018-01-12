import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

matrix = np.array(
    [[ 348.74833497, 0., 325.37653412],
     [0., 336.2491519, 256.36903539],
     [0., 0., 1.]])

dist = np.array([[-0.33826572,  0.17477173,  0.00039001,  0.0094751 , -0.05144266]])

'''

    |----|
    |    |
    |    |
    |----| 


  1 4
  2 3
'''


def cal_map():
    w = 20.
    h = 27.
    offset_back_y = 6.
    grid_size = 2.5
    chessboard_size = (4., 3.)
    grid_num_x = chessboard_size[0]
    grid_num_y = chessboard_size[1]
    back_points = np.float32([[223.4, 341.4], [206.6, 313.7], [140.3, 314.6], [121, 341.4]])

    target_w_pixel = 600.
    target_h_pixel = 810.

    target_w_cm = 60.
    target_y_cm = 81.

    unit = target_w_pixel / target_w_cm

    midx = target_w_cm / 2
    midy = target_y_cm / 2

    back_target_coors = np.float32([
        [midx - grid_num_x / 2, midy + h / 2 + offset_back_y + grid_size],
        [midx - grid_num_x / 2, midy + h / 2 + offset_back_y + grid_size * grid_num_y],
        [midx + grid_num_x / 2, midy + h / 2 + offset_back_y + grid_size * grid_num_y],
        [midx + grid_num_x / 2, midy + h / 2 + offset_back_y + grid_size],
    ]) * unit
    print back_target_coors
    M = cv2.getPerspectiveTransform(back_points, back_target_coors)
    print M
    return M

w = 640
h = 480
newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(matrix, dist, (w, h), 1, (w, h))
mapx, mapy = cv2.initUndistortRectifyMap(matrix, dist, None, newCameraMatrix, (w,h), 5)
print roi
x, y, w, h = roi
#
# pts1 = np.float32([[0, 0], [0, 360], [640, 360], [640, 0]])
# '''
# 0 3
# 1 2
# '''
#
# car_points = [[250, 250], [250, 350], [350, 350], [350, 250]]
# '''
# 0 3
# 1 2
# '''
# targets_width = 600
# targets_height = 600
#
# front = np.float32([[0, 0], car_points[0], car_points[3], [targets_width, 0]])
# left = np.float32([[0, targets_height], car_points[1], car_points[0], [0, 0]])
# back_corners = np.float32([[178.48, 254.04], [234.03, 201.53], [432.40, 208.64], [476.86, 265.54]])
# back = np.float32([[224, 660], [224, 764], [400, 764], [400, 660]])
# right = np.float32([[targets_width, 0], car_points[3], car_points[2], [targets_width, targets_height]])
#
# directions = [front, right, left, back]
# M = cv2.getPerspectiveTransform(back_corners, back)
M = cal_map()

while True:
    # target = np.zeros([600, 600, 3], dtype=np.uint8)
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    ### undistort
    # dst = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
    dst = cv2.undistort(frame, matrix, dist, None, newCameraMatrix)
    ### undistort

    # dst = dst[y : y + h, x : x + w]
    ### transpose
    bird = cv2.warpPerspective(dst, M, (600, 810))
    # dst = cv2.resize(dst, (400, 540))
    cv2.imshow('ori', frame)
    cv2.imshow('undisorted', dst)
    cv2.imshow('birdview', bird)
    cv2.waitKey(1)
    ### find cornors
    # gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    # # TermCriteria(CV_TERMCRIT_EPS + CV_TERMCRIT_ITER, 30, 0.1)
    #
    # find, corners = cv2.findChessboardCorners(gray, (4, 3))
    # if find:
    #     print corners
    #     for [point] in corners:
    #         print point
    #         cv2.circle(gray, ((int)(point[0]), (int)(point[1])), 3, (0, 255, 0), 1)
    #
    #         cv2.imshow('ori', frame)
    #         cv2.imshow('birdview', gray)
    #     break
    # else:
    #     cv2.imshow('ori', gray)
    #     cv2.waitKey(1)
    ###

#
#
# # dst = cv2.warpPerspective(frame, M, (600, 600))
# # target = cv2.bitwise_or(target, dst)
#
# #
# # plt.subplot(121)
# # plt.imshow(frame)
# # plt.title('front')
# #
# # plt.subplot(122)
# # plt.imshow(target)
# # plt.title('birdview')
# #
# # plt.show()
# # cv2.imshow('test', target)
#
# cv2.waitKey(0)


