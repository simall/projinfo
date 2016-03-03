#!/usr/bin/python3.4
# -*- coding: Utf-8 -*-

from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QBrush, QColor, QPainter, QPolygonF
from PyQt5.QtCore import Qt, QPointF

import sys

sys.path.append('../classes_eco/')
sys.path.append('../backward/')
sys.path.append('../res/')

from ressources import *
from carto import *
from ecosys import *
import constantes

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.initGui()

    def initGui(self):

        self.eco = Ecosys()

        self.resize(constantes.nb_carres_largeur*constantes.carre_res[0], constantes.nb_carres_hauteur*constantes.carre_res[1])
        self.center()
        self.setWindowTitle('Simulateur Ecosys')
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def paintEvent(self, event): #Override de la méthode QWidget
        qp = QPainter()
        qp.begin(self)
        self.drawPol(qp)
        qp.end()


    def drawPol(self, qp):
        for i in range(constantes.nb_carres_largeur):
            for j in range(constantes.nb_carres_hauteur):
                case = self.eco.carto[i][j]
                if case.id_res == 2:
                    #eau
                    qp.setPen(QColor(64, 178, 243))
                    qp.setBrush(QColor(64, 178, 243))
                    qp.drawRect(case.rect)

                elif case.id_res == 1:
                    #herbe
                    qp.setPen(QColor(21, 186, 52))
                    qp.setBrush(QColor(21, 186, 52))
                    qp.drawRect(case.rect)

                elif case.id_res == 0:
                    #terre
                    qp.setPen(QColor(179, 131, 62))
                    qp.setBrush(QColor(179, 131, 62))
                    qp.drawRect(case.rect)

        self.update()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())