import tensorflow as tf
from keras import optimizers
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten, BatchNormalization
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint
from keras.models import Sequential




ALPHA_DICT = {0:"0",1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",
              10:"A",11:"B",12:"C",13:"E",14:"H",15:"K",16:"M",17:"O",18:"P",
              19:"T",20:"X",21:"Y"}



class Alex_Model(object):

    def __init__(self, trainable=True):
        # Building model
        self._build_model()

    def _build_model(self):
        # CNN model
        self.model = Sequential()
        self.model.add(Conv2D(filters=128, kernel_size=(11,11), strides=(4,4), activation='relu', input_shape=(32,32,1)))
        self.model.add(BatchNormalization())
        self.model.add(MaxPooling2D(pool_size=(2,2), padding="same"))
        self.model.add(Conv2D(filters=256, kernel_size=(5,5), strides=(1,1), activation='relu', padding="same"))
        self.model.add(BatchNormalization())
        self.model.add(MaxPooling2D(pool_size=(3,3), padding="same"))
        self.model.add(Conv2D(filters=256, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same"))
        self.model.add(BatchNormalization())
        self.model.add(Conv2D(filters=256, kernel_size=(1,1), strides=(1,1), activation='relu', padding="same"))
        self.model.add(BatchNormalization())
        self.model.add(Conv2D(filters=256, kernel_size=(1,1), strides=(1,1), activation='relu', padding="same"))
        self.model.add(BatchNormalization())
        self.model.add(MaxPooling2D(pool_size=(2,2), padding="same"))
        self.model.add(Flatten())
        self.model.add(Dense(1024,activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(1024,activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(22, activation='softmax'))