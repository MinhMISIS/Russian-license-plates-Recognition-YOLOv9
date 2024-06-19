import cv2
import numpy as np
import torch
import time
from localization.localization import detect,load_model_local

from classicfication.classicfication import load_model_clas, character_recog_CNN
from preprocess_segment import crop_n_rotate_LP_new, clear_noise, get_color_LP

Min_char = 0.01
Max_char = 0.09
def load_models():
    model_char = load_model_clas()
    model_LP = load_model_local()
    return model_LP, model_char
def process(source_img, model_LP,model_char):
    #source_img = cv2.resize(source_img,(640,352))
    pred, LP_detected_img = detect(source_img,model_LP)
    cv2.imshow('input', cv2.resize(source_img, dsize=None, fx=0.5, fy=0.5))
    cv2.imshow('LP_detected_img', cv2.resize(LP_detected_img, dsize=None, fx=0.5, fy=0.5))

    c = 0
    result_LP = []
    result_xy_LP= []
    result_color_LP = []
    # kẹt tại đây / update: đã giải quyết xong loõi không nhận lọc được ký tự - tuỳ chỉnh tham số min-maxchar và ratiochar
    # có lỗi xoay biển số

    for *xyxy, conf, cls in reversed(pred):
        x1, y1, x2, y2 = int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])
        #angle, rotate_thresh, LP_rotated = crop_n_rotate_LP(source_img, x1, y1, x2, y2)
        rotate_thresh, LP_rotated = crop_n_rotate_LP_new(LP_detected_img, x1, y1, x2, y2)
        if (rotate_thresh is None) or (LP_rotated is None):
            continue
        cv2.imshow('LP_rotated_new', LP_rotated)
        cv2.imshow('rotate_thresh_new', rotate_thresh)
        result_color_LP.append( get_color_LP(LP_rotated))
        #################### Prepocessing and Character segmentation ####################
        LP_rotated_copy = LP_rotated.copy()

        rotate_thresh = clear_noise(rotate_thresh)

        cont, hier = cv2.findContours(rotate_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cont = sorted(cont, key=cv2.contourArea, reverse=True)[:17]


        cv2.drawContours(LP_rotated_copy, cont, -1, (0, 0, 255), 1)  # Draw contours of characters in a LP


        ##################### Filter out characters #################
        char_x_ind = {}
        char_x = []
        height, width, _ = LP_rotated_copy.shape
        roiarea = height * width

        for ind, cnt in enumerate(cont):
            #lấy toạ độ ký tự
            (x, y, w, h) = cv2.boundingRect(cont[ind])
            ratiochar = w / h
            char_area = w * h
            if (Min_char * roiarea < char_area < Max_char * roiarea ) and (0.11 < ratiochar < 1.1):# < Max_char * roiarea): and (0.25 < ratiochar < 1):
                char_x.append([x, y, w, h])
                cv2.rectangle(LP_rotated_copy, (x,y), (x+w,y+h), (0,255,255), 1)


        if not char_x:
            continue

        char_x = np.array(char_x)
        cv2.imshow('LP_rotated_copy', LP_rotated_copy)
        ############ Character recognition ##########################
        starttime = time.time()
        threshold_12line = char_x[:, 1].min() + (char_x[:, 3].mean() / 2)
        char_x = sorted(char_x, key=lambda x: x[0], reverse=False)
        strFinalString = ""


        for i, char in enumerate(char_x):
            x, y, w, h = char
            cv2.rectangle(LP_rotated, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #cv2.rectangle(rotate_thresh, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cắt hình kí tự từ toạ độ / hình đang cắt từ ảnh threshold (trắng đen)
            imgROI = rotate_thresh[y:y + h, x:x + w]
            cv2.imshow('imgROI', 255-imgROI)
            text = character_recog_CNN(model_char, imgROI)
            strFinalString += text

        #cv2.putText(LP_detected_img, strFinalString, (x1, y1 - 20), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255, 0), 2)

        #cv2.imshow('charac', LP_rotated_copy)
        #cv2.imshow('LP_rotated_{}'.format(c), LP_rotated)
        #print('License Plate_{}:'.format(c), strFinalString)
        result_LP.append(strFinalString)
        result_xy_LP.append([x1, y1])
        #c += 1
        endtime = time.time()-starttime
        #cv2.imshow('final_result', cv2.resize(LP_detected_img, dsize=None, fx=0.5, fy=0.5))
    print('Finally Done!')
    #cv2.imshow('this is last', final_img)
    #cv2.waitKey(0)
    return LP_detected_img,result_LP, result_xy_LP, result_color_LP
def main():
    LP,char = load_models()
    #vid = cv2.VideoCapture(0)
    #_,source_img = vid.read()hw
    image_path = 'img_28.png'
    source_img = cv2.imread(image_path)
    cv2.imshow("last", process(source_img,LP,char)[0])
    print(process(source_img,LP,char)[1])
    cv2.waitKey(0)
if __name__ == '__main__':
    main()

#%%
