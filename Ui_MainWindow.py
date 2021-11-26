import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json
import os.path as osp
import numpy as np
import cv2
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
class SecondUI(QWidget):
    # 通过窗口获得用户输入的值
    def __init__(self):
        super(SecondUI, self).__init__()
        self.resize(400, 300)
        self.setWindowTitle("请输入像素信息")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(100, 80, 181, 91))
        # 静态标签
        self.hint = QLabel(self)
        self.hint.setText("请输入value值")
        self.hint.move(60, 40)
        self.value_input = QLineEdit(self)  # 单行编辑框
        self.value_input.move(60, 100)

        # 保存输入的信息
        self.Btnsave = QtWidgets.QPushButton(self)
        self.Btnsave.setGeometry(QtCore.QRect(100, 150, 100, 50))
        self.Btnsave.setObjectName("Btnsave")
        self.Btnsave.setText("save")
        self.Btnsave.clicked.connect(self.save_information)
        self.BtnClose = QtWidgets.QPushButton(self)
        self.BtnClose.setGeometry(QtCore.QRect(250, 150, 100, 50))
        self.BtnClose.setObjectName("BtnClose")
        self.BtnClose.setText("cancel")
        self.BtnClose.clicked.connect(self.close)


    def save_information(self):
        # 获得输入的内容
        value_out = int(self.value_input.text())
        self.close()

class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 900)
        self.MainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 图片名展示
        self.tabWidget = QtWidgets.QListWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 504, 712.8))
        self.tabWidget.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.points = []
        self.value_list = []

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1140, 590, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(1130, 480, 141, 22))
        self.toolButton.setObjectName("toolButton")
        # 获取图片文件夹地址
        self.toolButton.clicked.connect(self.msg)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 22))
        self.menubar.setObjectName("menubar")
        self.menuUi_MainWindow = QtWidgets.QMenu(self.menubar)
        self.menuUi_MainWindow.setObjectName("menuUi_MainWindow")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuUi_MainWindow.menuAction())
        self.BtnClose = QtWidgets.QPushButton(self.centralwidget)
        self.BtnClose.setGeometry(QtCore.QRect(1130, 300, 141, 22))
        self.BtnClose.setObjectName("BtnClose")
        self.BtnClose.clicked.connect(MainWindow.close)  # 将BtnClose的clicked信号和MainWindow的close槽连接
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.tabWidget2 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget2.setGeometry(QtCore.QRect(600, 0, 504, 712.8))
        self.tabWidget2.setObjectName("tabWidget")


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.BtnClose.setText(_translate("MainWindow", "Close"))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "ok"))
        self.toolButton.setText(_translate("MainWindow", "select folders"))
        self.menuUi_MainWindow.setTitle(_translate("MainWindow", "Ui_MainWindow"))
        self.BtnClose.setText(_translate("MainWindow","close"))

    def msg(self, Filepath):
        # 点击按钮出现文件夹位置
        pic_path = QtWidgets.QFileDialog.getOpenFileName()
        # 在这里定义一个函数展示图片getExistingDirectory(None, "选取文件夹", "C:/")  # 起始路径
        self.pic_path = pic_path[0]
        self.show_image()

    def show_image(self):
        # 点击listWidget组建中的item响应事件
        pic_path = self.pic_path

        pix = QPixmap(pic_path)
        self.img_path = pic_path
        lab1 = QLabel()
        lab1.setPixmap(pix)
        # 将图片搞成和组件一样的大小
        lab1.resize(504, 712.8)
        lab1.setScaledContents(True)  # 设置图片自适应窗口大小
        vbox = QVBoxLayout()
        vbox.addWidget(lab1)
        tabWidget = self.tabWidget
        tabWidget.setLayout(vbox)
        # 点击图片获得鼠标点击坐标
        lab1.mousePressEvent = self.getPixel


    def getPixel(self,event):
        # 点击图片得到坐标
        x = int(event.pos().x())
        y = int(event.pos().y())
        # 获得鼠标点击的位置信息
        self.second_ui = SecondUI()
        # 初始化第二个窗口
        self.second_ui.show()
        points = self.points
        points.append([x,y])
        self.get_json()

    def get_json(self):
        # 通过points，values_list生成每一个sample的json文件
        points = self.points
        end_str = self.pic_path.split('/')[-1]
        directory_path = self.pic_path.rstrip(end_str)
        folder_path = directory_path + '/json_foldee'
        if os.path.exists(folder_path):
            img_path = self.img_path
            img_name = os.path.basename(img_path)
            img_json_path = os.path.join(folder_path,img_name[:-4]+'.json')
            get_json_dict(img_json_path, points, img_name)
        else:
            os.makedirs(folder_path)
            img_path = self.img_path
            img_name = os.path.basename(img_path)
            img_json_path = os.path.join(folder_path, img_name[:-4])
            print(img_json_path)

    def get_value_data_from_SecondUI(self,value_out):
        # 接受SecondUI传过来的value_out，保存到自己的变量里面。
        self.value_out = value_out




def get_json_dict(img_json_path,points,img_name):
    index = 0
    json_list = []
    for sample in points:
        new_sample = {
            'index': index,
            'x': sample[0],
            'y':sample[1]
        }
        json_list.append(new_sample)
    json_data = {
        'img_name': img_name,
        'data': json_list
    }
    with open(img_json_path, 'w') as f:
        json.dump(json_data, f, indent=4)
    # values的值传递错误，目前还没改过来


    def create_priority(self,width, height, points, values,img_path):
        """"
        width, height mean the width, height of picture
        points means the piexl of picture
        values means the weight of the picture
        """
        grid_x, grid_y = np.mgrid[0:width, 0:height]
        points = np.array(points)
        values = np.array(values)
        grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
        # 如果是subplot （2 ，2 ，1），那么这个figure就是个2*2的矩阵图，也就是总共有4个图，1就代表了第一幅图
        mask = grid_z1.T.astype(np.uint8)
        directory_path = self.directory_path
        folder_path = os.path.join(directory_path, 'priority_field_map_img_folder')
        if os.path.exists(folder_path):
            cv2.imwrite(img_path, mask)
        else:
            os.mkdir(folder_path)
            cv2.imwrite(img_path, mask)
        return mask
