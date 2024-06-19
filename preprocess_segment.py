import cv2
import numpy as np


# module level variables ##########################################################################
GAUSSIAN_SMOOTH_FILTER_SIZE = (3, 3)  # kích cỡ càng to thì càng mờ # tham số gốc (5,5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19 #19
ADAPTIVE_THRESH_WEIGHT = 11 #9
Min_char = 0.01
Max_char = 0.09

###################################################################################################
def preprocess(imgOriginal):
    '''
    :param imgOriginal: RGB image (cv2)
    :return: imgGrayscale, imgThresh
    '''

    imgGrayscale = cv2.cvtColor(imgOriginal,cv2.COLOR_BGR2GRAY) #nên dùng hệ màu HSV
    # Trả về giá trị cường độ sáng ==> ảnh gray
    imgMaxContrastGrayscale = apply_brightness_contrast(imgGrayscale,10,5)  # để làm nổi bật biển số hơn, dễ tách khỏi nền
    # cv2.imwrite("imgGrayscalePlusTopHatMinusBlackHat.jpg",imgMaxContrastGrayscale)
    height, width = imgGrayscale.shape

    imgBlurred = np.zeros((height, width, 1), np.uint8)
    imgBlurred = cv2.GaussianBlur(imgMaxContrastGrayscale, GAUSSIAN_SMOOTH_FILTER_SIZE, 0)
    # Làm mịn ảnh bằng bộ lọc Gauss 5x5, sigma = 0

    imgThresh = cv2.adaptiveThreshold(imgBlurred, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,
                                      ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)

    #_,imgThresh = cv2.threshold(imgBlurred, 100, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # Tạo ảnh nhị phân
    return imgGrayscale, imgThresh



def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):

    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    cv2.imshow("Aplly contract and brightness", buf)
    return buf


def crop_n_rotate_LP_new(source_img, x1, y1, x2, y2):
    #cat anh tu yolo
    w = int(x2 - x1)
    h = int(y2 - y1)
    LP = source_img[y1:y1 + h, x1:x1 + w]
    try:
        ratio = 400/w
        LP = cv2.resize(LP, (400, int(h*ratio)), cv2.INTER_AREA)
    except:
        pass

    #tim hinh chu nhat lon nhat
    gray, thresh = preprocess(LP)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    max_cnt = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            max_cnt = cnt
    x,y,w,h = cv2.boundingRect(max_cnt)
    #xoay dua tren goc cuar hinh chu nhat lon nhat va nho nhat
    rect = cv2.minAreaRect(max_cnt)
    ((cx,cy),(cw,ch),angle) = rect
    if angle > 45 :
        M = cv2.getRotationMatrix2D((cx,cy), angle -90, 1)
    else:
        M = cv2.getRotationMatrix2D((cx,cy), angle , 1)

    rotated = cv2.warpAffine(LP, M, (LP.shape[1], LP.shape[0]))

    gray, thresh = preprocess(rotated)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #tim hinh chu nhat lan nhat de cat
    max_area = 0
    max_cnt = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            max_cnt = cnt
    x,y,w,h = cv2.boundingRect(max_cnt)
    cropped_LP = rotated[y:y+h, x:x+w]
    LP_rotated = cropped_LP
    _,rotate_thresh = preprocess(LP_rotated)
    _,rotate_thresh2 = preprocess(LP)
    #rotate_thresh = cv2.bitwise_not(rotate_thresh)
    return rotate_thresh2,LP #rotate_thresh, LP_rotated

def clear_noise(imgthesh):
    _, labels = cv2.connectedComponents(imgthesh)
    mask = np.zeros(imgthesh.shape, dtype="uint8")
    total_pixels = imgthesh.shape[0] * imgthesh.shape[1]
    lower = total_pixels // 300 #90
    upper = total_pixels // 20#20
    for label in np.unique(labels):
        if label == 0:
            continue
        labelMask = np.zeros(imgthesh.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)
        if numPixels > lower and numPixels < upper:
            mask = cv2.add(mask, labelMask)
    cv2.imshow('clear noise', mask)
    return mask


def get_color_LP(img):
    img = apply_brightness_contrast(img,0,59)
    height, width, _ = np.shape(img)
    data = np.reshape(img, (height * width, 3))
    data = np.float32(data)
    number_clusters = 2
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)
    bgr=[]
    main_color = None
    for i in centers:
        bgr.append(list(i))

    if bgr[0][1] < 30 and bgr[0][1] < 30 and bgr[0][2] < 30 :
        main_color = bgr[1]
    else:
        main_color = bgr[0]

    if main_color[0] < 170:
        return "yellow"
    else:
        return "white"
def main():
    # create_yaml()
    print('haha')


if __name__ == "__main__":
    main()

#%%
