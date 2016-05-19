#!/usr/bin/python3.4
# -*- coding: Utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QSpinBox, QApplication, QDesktopWidget, QPushButton, QLineEdit
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtCore import Qt, QPointF, QRect
from PyQt5.QtCore import QObject, pyqtSignal, QEvent

rows = 0
cols = 0
name = ''


class Start(QWidget):

    signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.initGui()
        
        
    def initGui(self):

        qlb0 = QLabel(self)
        qlb0.setText('nom: ')
        qlb0.move(50, 20)

        self.qle = QLineEdit(self)
        self.qle.setText("test")
        self.qle.move(100, 15)

        qlb1 = QLabel(self)
        qlb1.setText('nombre de lignes: ')
        qlb1.move(50, 55)     

        self.qsp1 = QSpinBox(self)
        self.qsp1.setMaximum(1000)
        self.qsp1.move(180, 50)

        qlb1 = QLabel(self)
        qlb1.setText('nombre de colonnes: ')
        qlb1.move(50, 85)   

        self.qsp2 = QSpinBox(self)
        self.qsp2.setMaximum(1000)
        self.qsp2.move(180, 80)

        qb = QPushButton("Créer", self)
        qb.move(190, 130)

        qb.clicked.connect(self.buttonClicked)
        
        self.resize(280, 170)
        self.setWindowTitle('Editeur')
        self.center()

    def buttonClicked(self):
        global rows, cols, name

        (rows, cols, name) = (self.qsp1.value(), self.qsp2.value(), self.qle.text())
        self.close()
        self.signal.emit()

    def center(self):
        '''
        Détermine le centre de la fenêtre
        '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initGui()
        
    def initGui(self):
        self.accueil = Start()
        self.accueil.show()

        self.accueil.signal.connect(self.closeDial)

        self.rows = 0
        self.cols = 0
        self.name = ''
        self.size = 0

    def closeDial(self):
        global rows, cols, name

        self.rows = rows
        self.cols = cols
        self.name = name
        self.size = 10

        self.tab = [[] for i in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                (self.tab[i]).append(0)

        self.texture = 1

        self.width = cols*self.size
        self.height = rows*self.size

        self.resize(self.width, self.height)
        self.setWindowTitle('Editeur')
        self.center()
        self.show()

    def mouseMoveEvent(self, event):
        pos = event.pos()

        if pos.x() >= 0 and pos.x() <= self.width and pos.y() >= 0 and pos.y() <= self.height:
            i = pos.y() // self.size
            j = pos.x() // self.size

            if event.buttons() == Qt.LeftButton:
                self.tab[i][j] = self.texture
            elif event.buttons() == Qt.RightButton:
                self.tab[i][j] = 0

    def mousePressEvent(self, event):
        pos = event.pos()

        if pos.x() >= 0 and pos.x() <= self.width and pos.y() >= 0 and pos.y() <= self.height:
            i = pos.y() // self.size
            j = pos.x() // self.size

            if event.buttons() == Qt.LeftButton:
                self.tab[i][j] = self.texture
            elif event.buttons() == Qt.RightButton:
                self.tab[i][j] = 0

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_E:
            self.texture = 2
        elif event.key() == Qt.Key_H:
            self.texture = 1
        elif event.key() == Qt.Key_S:
            f = open(self.name, 'w')

            for i in range(self.rows):
                for j in range(self.cols):
                    f.write(str(self.tab[i][j]))
                f.write('\n')

            f.close()

    def paintEvent(self, event): #Override de la méthode QWidget
        '''
        Initialise la fonction d'affichage
        '''
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()
        self.update()

    def draw(self, qp):
        for i in range(self.rows):
            for j in range(self.cols):
                case = self.tab[i][j]

                if case == 1:
                    qp.setPen(QColor(21, 186, 52))
                    qp.setBrush(QColor(21, 186, 52))

                    qp.drawRect(QRect(j*self.size, i*self.size, self.size, self.size))
                elif case == 2:
                    qp.setPen(QColor(64, 178, 243))
                    qp.setBrush(QColor(64, 178, 243))

                    qp.drawRect(QRect(j*self.size, i*self.size, self.size, self.size))
                elif case == 0:
                    qp.setPen(QColor(179, 131, 62))
                    qp.setBrush(QColor(179, 131, 62))

                    qp.drawRect(QRect(j*self.size, i*self.size, self.size, self.size))

        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(0, 0, 0))

        for i in range(self.rows):
            qp.drawLine(QPointF(0, i*self.size), QPointF(self.cols*self.size, i*self.size))

        for i in range(self.cols):
            qp.drawLine(QPointF(i*self.size, 0), QPointF(i*self.size, self.rows*self.size))

    def center(self):
        '''
        Détermine le centre de la fenêtre
        '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2) 
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    w = Window()
    sys.exit(app.exec_())