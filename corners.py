import cv2
import numpy as np
import json
import matplotlib.pyplot as plt


def read_params_from_file(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        mtx = np.array(data['mtx'])
        dist = np.array(data['dist'])
        newcameramtx = np.array(data['newcameramtx'])
    return mtx, dist, newcameramtx

'''
example is (1, 640, 480, back.json, (4, 3))
'''
def find_corners(device, width, height, filename, boardsize):
    mtx, dist, newcameramtx = read_params_from_file(filename)
    cap = cv2.VideoCapture(device)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    while True:
        ret, frame = cap.read()
        undistorted_image = cv2.undistort(frame, mtx, dist, None, newcameramtx)
        ## find cornors
        gray = cv2.cvtColor(undistorted_image, cv2.COLOR_BGR2GRAY)
        find, corners = cv2.findChessboardCorners(gray, boardsize)
        '''
        (x_max, y_max), ..., (x_min, y_max),
        (x_max, ...), ..., (x_min, ...),
        (x_max, y_min), ..., (x_min, y_min)
        '''
        if find:
            print corners.shape
            for [point] in corners:
                print point
                cv2.circle(gray, ((int)(point[0]), (int)(point[1])), 5, (0, 255, 0), 1)
            cv2.imshow('ori', frame)
            cv2.imshow('birdview', gray)

            cv2.imwrite('undistorted.png', undistorted_image)
            cv2.imwrite('corners.png', gray)

            return corners[0][0], corners[boardsize[0] - 1][0], corners[-boardsize[0]][0], corners[-1][0]
        else:
            cv2.imshow('ori', gray)
            cv2.waitKey(1)



def cal_target_coor(direction, chessboard_size):
    car_width = 20.
    car_height = 27.
    offset_back_y = 6.
    grid_size = 2.5
    chessboard_size = (4., 3.)
    grid_num_x = chessboard_size[0]
    grid_num_y = chessboard_size[1]

    target_w_pixel = 600.
    target_h_pixel = 810.

    target_w_cm = 60.
    target_y_cm = 81.

    unit = target_w_pixel / target_w_cm

    midx = target_w_cm / 2
    midy = target_y_cm / 2

    back_target_coors = np.float32([
        [midx - grid_num_x / 2, midy + car_height / 2 + offset_back_y + grid_size],
        [midx - grid_num_x / 2, midy + car_height / 2 + offset_back_y + grid_size * grid_num_y],
        [midx + grid_num_x / 2, midy + car_height / 2 + offset_back_y + grid_size * grid_num_y],
        [midx + grid_num_x / 2, midy + car_height / 2 + offset_back_y + grid_size],
    ]) * unit
    print back_target_coors
    return back_target_coors

def save_transform_matrix(M, filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        data['transformmtx'] = M.tolist()
    with open(filename + '_final', 'w') as json_file:
        json_file.write(json.dumps(data))


if __name__ == '__main__':
    corners = find_corners(1, 640, 480, 'back.json', (4, 3))
    reordered_corners = np.array(corners)[[0, 2, 3, 1]]
    print corners
    target_corners = cal_target_coor('back', (4, 3))
    # must be same order
    M = cv2.getPerspectiveTransform(reordered_corners, target_corners)
    print M
    save_transform_matrix(M, 'back.json')


