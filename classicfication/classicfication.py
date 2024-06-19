from classicfication.model import Alex_Model
import cv2, time
import numpy as np
import tensorflow as tf
def load_model_clas():
    CHAR_CLASSIFICATION_WEIGHTS = '/Users/tranminh/Desktop/Hoc online/Проект к ВКР/Renew Project/classicfication/weitgh_class.h5'
    model_char = Alex_Model(trainable=False).model
    model_char.load_weights(CHAR_CLASSIFICATION_WEIGHTS)
    return model_char

ALPHA_DICT = {0:"0",1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",
              10:"A",11:"B",12:"C",13:"E",14:"H",15:"K",16:"M",17:"O",18:"P",
              19:"R",20:"S",21:"T",22:"U",23:"X",24:"Y"}

def character_recog_CNN(model, img, dict=ALPHA_DICT):
    '''
    Turn character image to text
    :param model: Model character recognition
    :param img: threshold image no fixed size (white character, black background)
    :param dict: alphabet dictionary
    :return: ASCII text
    '''

    start= time.time()
    img = (255 - img)/255
    imgROI = cv2.resize(img, (32, 32), cv2.INTER_AREA)
    imgROI = imgROI.reshape((32, 32, 1))
    imgROI = np.array(imgROI)
    imgROI = np.expand_dims(imgROI, axis=0)
    result = model.predict(imgROI, verbose='2')
    result_idx = np.argmax(result, axis=1)
    print("CNN: " + str(time.time()-start))
    return ALPHA_DICT[result_idx[0]]

