import sys
from PyQt5.QtWidgets import *
from Ui_MainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np


class MainWindow(QMainWindow):
    # 读取主图片布局
    def __init__(self):
            super(MainWindow, self).__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

from scipy.interpolate import griddata
def create_priority(width, height, points, values):
    """

    """
    points = np.array([[0,0],[128,30],[255,0],[128, 170], [0,255],[255,0],[255,255]])
    values = np.array([0, 255, 0, 200, 0, 0, 0])
    grid_x, grid_y = np.mgrid[0:width, 0:height]
    # points = np.array(points)
    # values = np.array(values)
    grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
    mask = grid_z1.T.astype(np.uint8)

    return mask


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    # points = np.array([[0, 0], [128, 30], [255, 0], [128, 170], [0, 255], [255, 0], [255, 255]])
    # values = np.array([0, 255, 0, 200, 0, 0, 0])
    # width = 6
    # height = 1
    # create_priority(width, height, points, values)
