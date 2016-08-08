# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui


class Splash(QtWidgets.QSplashScreen):

    def __init__(self, main):
        super(Splash, self).__init__()
        self.setPixmap(QtGui.QPixmap(main.resolveResource("splash.png")))
        self.show()
