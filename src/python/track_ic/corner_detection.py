import cv2
import numpy as np

#filename = 'chessboard2.jpg'
#img = cv2.imread(filename)
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def corner_detect(gray_input, img_input, row, col):
    height, width = gray_input.shape
    #print(height, width)
    gray = gray_input
    img = img_input
    #crop_img = img[y:y+h, x:x+w]
    #gray = gray_input[col+col:h, row+row:w]
    #img = img_input[col:col+70, row:row+70]
    # find Harris corners
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.004) #0.04
    dst = cv2.dilate(dst,None)
    ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0) #0.01*dst.max() was original value
    dst = np.uint8(dst)    

    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)  

    # define the criteria to stop and refine the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)  

    # Now draw them
    res = np.hstack((centroids,corners))
    res = np.int0(res)
    img[res[:,1],res[:,0]]=[0,0,255]
    img[res[:,3],res[:,2]] = [0,255,0]
    print(corners)
    corners = np.array(corners).astype(int)
    centroids = np.array(centroids).astype(int)
    for corner in corners:
        row = corner[0]
        col = corner[1]

        cv2.rectangle(img,(col, row),(col + 2,row + 2),(0,0,255),2)

    for corner in centroids:
        row = corner[0]
        col = corner[1]

        cv2.rectangle(img,(col, row),(col + 2,row + 2),(0,255,0),2)
   
    cv2.imwrite('subpixel5.png',img)

    return img