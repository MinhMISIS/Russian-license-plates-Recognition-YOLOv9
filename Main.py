

from database import select, creat_car_guest, creat_transaction\
    ,update_transaction,get_transaction,check_car_in_is_available, \
    find_element, check_element_in_list
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtGui import QImage
import imutils, os
import time

from recognize import process, load_models
import cv2
import pyshine as ps

try:
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
except Exception as e:
    print('Warning...',e)


class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1013, 606)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(730, 0, 271, 531))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.listwidget = QtWidgets.QListWidget(self.gridLayoutWidget_2)
        self.listwidget.setObjectName("listwidget")
        self.gridLayout_2.addWidget(self.listwidget, 0, 0, 1, 1)
        #self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        #self.pushButton.setObjectName("pushButton")
        #self.gridLayout_2.addWidget(self.pushButton, 3, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 2, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("IN")
        self.comboBox.addItem("OUT")
        self.gridLayout_2.addWidget(self.comboBox, 1, 0, 1, 1)
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 9, 711, 401))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(19, 419, 701, 101))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_2.setObjectName("label_2")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1013, 37))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton_2.clicked.connect(self.loadImage)
        #self.pushButton.clicked.connect(self.savePhoto)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Added code here
        self.filename = 'Snapshot '+str(time.strftime("%Y-%b-%d at %H.%M.%S %p"))+'.png' # Will hold the image address location
        self.tmp = None # Will hold the temporary image for display
        self.fps=0
        self.started = False
        self.LP = []
        self.LP_photo = None
        self.LP_color=[]
        self.status = 'NO'
        self.all_LP = select("license_plate","car")
        self.transaction = []
    def loadImage(self):
        """ This function will load the camera device, obtain the image
            and set it to label using the setPhoto function
        """
        if self.started:
            self.started=False
            self.pushButton_2.setText('Start')
        else:
            self.started=True
            self.pushButton_2.setText('Stop')

        cam = True # True for webcam
        if cam:
            vid = cv2.VideoCapture(0)
        else:
            vid = cv2.VideoCapture('video.mp4')

        cnt=0
        frames_to_count=20
        st = 0
        fps = 1


        countexp = 0

        while(vid.isOpened()):

            QtWidgets.QApplication.processEvents()
            self.all_LP = select("license_plate","car")
            img, self.image = vid.read()

            if self.status == 'YES':
                self.status = 'WAIT'

            if self.status == 'NO':
                try:
                    cache_LP= []
                    cache_xy= []
                    while len(cache_LP) < 3:
                        _, self.image = vid.read()
                        self.image, text_LP, xy_LP,  self.LP_color = process(self.image, model_detect, model_clas)
                        cache_LP.append(text_LP)
                        cache_xy.append(xy_LP)
                        self.LP_photo = self.image
                    LP = find_element(cache_LP)

                    for i in LP:
                        if len(i) < 7 or len(i) > 9:
                            break
                        else:
                            self.LP = LP
                            self.status = 'YES'
                    for i in reversed(range(len(cache_LP))):
                        if cache_LP[i] == self.LP:
                            xy_LP = cache_xy[i]
                            break
                    for j in range(len(self.LP)):
                        cv2.putText(self.image, self.LP[j], (xy_LP[j][0], xy_LP[j][1] - 20), cv2.FONT_HERSHEY_DUPLEX, 2, (25, 25, 25), 2)

                except Exception:
                    pass

            if self.status == 'WAIT':
                try:
                    self.image, text_LP, xy_LP, _ = process(self.image, model_detect, model_clas)
                    for j in range(len(self.LP)):
                        cv2.putText(self.image, self.LP[j], (xy_LP[j][0], xy_LP[j][1] - 20), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 0), 4, 3)
                    countexp = 0
                except Exception:
                    if countexp >= 6:
                        self.status = 'NO'
                        self.LP = []
                    countexp = countexp + 1
                    pass


            if self.comboBox.currentText() == "IN":
                if self.status == "YES":
                    for index, i in enumerate(self.LP):
                        if i not in self.all_LP:#select("license_plate","car","license_plate = %s"%(i))==[]:
                            photo_car = self.savePhoto(i)
                            color_LP = self.LP_color[index]
                            creat_car_guest(i, color_LP, photo_car)
                            creat_transaction(i, str(time.strftime("%Y-%m-%d %H:%M:%S")))
                        else:
                            if check_car_in_is_available(i):
                                creat_transaction(i, str(time.strftime("%Y-%m-%d %H:%M:%S")))

            elif self.comboBox.currentText() == "OUT":
                if not check_element_in_list(self.LP, self.all_LP):
                    self.status = 'NO'
                    self.LP = []
                    self.transaction = []
                else:
                    for i in self.LP:
                        if i in self.all_LP:
                            try:
                                update_transaction(i, str(time.strftime("%Y-%m-%d %H:%M:%S")))
                            except:
                                pass

            if cnt == frames_to_count:
                try: # To avoid divide by 0 we put it in try except
                    print(frames_to_count/(time.time()-st),'FPS')
                    self.fps = round(frames_to_count/(time.time()-st))
                    st = time.time()
                    cnt=0
                except:
                    pass
            cnt+=1

            self.update()
            key = cv2.waitKey(1) & 0xFF
            if self.started==False:
                break
                print('Loop break')

    def setPhoto(self,image):
        """ This function will take image input and resize it
            only for display purpose and convert it to QImage
            to set at the label.
        """
        self.tmp = image
        image = imutils.resize(image,width=710)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)

        self.label.setPixmap(QtGui.QPixmap.fromImage(image))


    def update(self):
        """ This function will update the photo according to the
            current values of blur and brightness and set it to photo label.
        """
        img = self.image
        # Here we add display text to the image
        text  =  'FPS: '+str(self.fps)
        img = ps.putBText(img,text,text_offset_x=20,text_offset_y=30,vspace=20,hspace=10, font_scale=1.0,background_RGB=(10,20,222),text_RGB=(255,255,255))
        text = str(time.strftime("%H:%M %p"))
        img = ps.putBText(img,text,text_offset_x=self.image.shape[1]-180,text_offset_y=30,vspace=20,hspace=10, font_scale=1.0,background_RGB=(228,20,222),text_RGB=(255,255,255))

        #if self.LP != ["waiting"]:
        if self.status == 'YES':
            self.label_2.setStyleSheet("background-color: lightgreen")
            self.label_2.setText("<font color='black'> OK </font>")

            for index, i in enumerate(self.LP):
                """them vao database"""
                self.listwidget.addItem(i)
                self.listwidget.addItem(self.LP_color[index])
                if self.comboBox.currentText() == "OUT":
                    self.transaction = get_transaction(i)
                    for j in self.transaction:
                        self.listwidget.addItem(j)
        elif self.status == 'WAIT':
            self.label_2.setStyleSheet("background-color: yellow")
            self.label_2.setText("<font color='black'> OK </font>")
        #if self.LP == []:
        elif self.status == 'NO':
            self.label_2.setStyleSheet("background-color: red")
            self.label_2.setText("<font color='black'> STOP </font>")
            self.listwidget.clear()

        #if len(self.LP) != 0:
        #    self.label_2.setStyleSheet("background-color: lightgreen")
        #    self.label_2.setText("<font color='black'> OK </font>")
        #else:
        #    self.label_2.setStyleSheet("background-color: red")
        #    self.label_2.setText("<font color='black'> STOP </font>")


        self.setPhoto(img)

    def savePhoto(self, LP = ""):
        """ This function will save the image"""
        path = "/Applications/XAMPP/xamppfiles/var/image-autopark/"
        self.filename = 'Car_'+LP+".jpeg"#+str(time.strftime("%Y-%b-%d at %H.%M.%S %p"))+'.png'
        cv2.imwrite(os.path.join(path, self.filename), self.LP_photo)
        print('Image saved as:',self.filename)
        return path + self.filename


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyShine video process"))
        self.pushButton_2.setText(_translate("MainWindow", "Start"))
        #self.pushButton.setText(_translate("MainWindow", "Take picture"))
        self.comboBox.setItemText(0, _translate("MainWindow", "IN"))
        self.comboBox.setItemText(1, _translate("MainWindow", "OUT"))
        self.label_2.setText(_translate("MainWindow", ""))
        self.label.setStyleSheet("background-color: black")
# Subscribe to PyShine Youtube channel for more detail!

# WEBSITE: www.pyshine.com


if __name__ == "__main__":
    import sys
    model_detect, model_clas = load_models()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


#%%
