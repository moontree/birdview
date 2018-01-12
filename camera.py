import cv2
import numpy as np
camera = cv2.VideoCapture(1)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,640)  
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,480)  

if camera.isOpened():
    pass
else:  
    print "can not open camera"
    

objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)
obj_points = [] 
img_points = []
img_names_undistort = []
criteria = (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001)   


timeF = 20 
pic_num=0
c=1
firstFrame = None
while True:
    rval, frame = camera.read()
    print frame.shape
    cv2.imshow("S", frame)  
    if(c%timeF == 0):
	pic_num=pic_num+1
	cv2.imwrite("frame" + str(c) + ".bmp", frame)
        size=frame.shape[:2]
        gray = cv2.cvtColor( frame, cv2.COLOR_BGR2GRAY)
        ima=cv2.GaussianBlur(gray,(7,7),8)
        ret, corners = cv2.findChessboardCorners(ima, (7,7), None)
        if ret:
            obj_points.append(objp)               
            corners2 = cv2.cornerSubPix(gray, corners, (7,7), (-1,-1), criteria)  
            img_points.append(corners2) 
    c = c + 1  
    cv2.waitKey(1) 
    if pic_num>16:
        break

camera.release()
cv2.destroyAllWindows()
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points,size, None, None) 
print mtx
print dist
'''
[[ 688.2231363     0.          340.34796698]
 [   0.          686.17383699  231.11217397]
 [   0.            0.            1.        ]]

'''
