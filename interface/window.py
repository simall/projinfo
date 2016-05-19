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
from collisions import *

from animaux import *#virer plus tard

class Window(QWidget):
    '''
    Créé une fenêtre
    '''
    def __init__(self):
        '''
        Constructeur
        '''
        super().__init__()

        self.initGui()

    def initGui(self):
        '''
        Initialise l'environnement graphique
        '''

        self.ecosys = Ecosys()
        self.ecosys.signal.connect(self.repaint)

        # self.ecosys.add_animal(Herbivore(), 'h')#pour les tests (temporaire)
        # self.ecosys.eco['h'][0].vision.update(self.ecosys.eco['h'][0].poly.head(), self.ecosys.eco['h'][0].poly.heading)

        # self.ecosys.add_animal(Herbivore(), 'h')
        # self.ecosys.eco['h'][1].vision.update(self.ecosys.eco['h'][1].poly.head(), self.ecosys.eco['h'][1].poly.heading)

        for i in range(20):
            self.ecosys.add_animal(Herbivore(), 'h')
            self.ecosys.eco['h'][i].vision.update(self.ecosys.eco['h'][i].poly.head(), self.ecosys.eco['h'][i].poly.heading)


        self.resize(constantes.nb_carres_largeur*constantes.carre_res[0], constantes.nb_carres_hauteur*constantes.carre_res[1])
        self.center()
        self.setWindowTitle('Simulateur Ecosys')

    def center(self):
        '''
        Détermine le centre de la fenêtre
        '''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def paintEvent(self, event): #Override de la méthode QWidget
        '''
        Initialise la fonction d'affichage
        '''
        qp = QPainter()
        qp.begin(self)
        self.drawPol(qp)
        qp.end()
        self.update()


    def keyPressEvent(self, e):
        '''
        Gère les évènements clavier
        '''
        if e.key() == Qt.Key_Up:
            self.ecosys.eco['h'][0].translater(self.ecosys.carto.carte, self.ecosys.eco, 1)
        elif e.key() == Qt.Key_Down:
            self.ecosys.eco['h'][0].translater(self.ecosys.carto.carte, self.ecosys.eco, -1)
        elif e.key() == Qt.Key_Left:
            self.ecosys.eco['h'][0].tourner(self.ecosys.carto.carte, self.ecosys.eco, -np.pi/8)
        elif e.key() == Qt.Key_Right:
            self.ecosys.eco['h'][0].tourner(self.ecosys.carto.carte, self.ecosys.eco, np.pi/8)
        elif e.key() == Qt.Key_Space:
            for i in range(300):
                self.ecosys.next_cycle()
                #print(self.ecosys.eco['h'][0].comportement.currentState)
                #print('--------------------------------\n\n')
                self.ecosys.signal.emit()


    def drawPol(self, qp):
        '''
        Affiche les éléments à l'écran
        '''
        for i in range(constantes.nb_carres_largeur):
            for j in range(constantes.nb_carres_hauteur):
                case = self.ecosys.carto.carte[i][j]
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

                elif case.id_res == -1:
                    #herbe épuisée
                    qp.setPen(QColor(3, 104, 25))
                    qp.setBrush(QColor(3, 104, 25))
                    qp.drawRect(case.rect)

                elif case.id_res == 0:
                    #terre
                    qp.setPen(QColor(179, 131, 62))
                    qp.setBrush(QColor(179, 131, 62))
                    qp.drawRect(case.rect)

        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(0, 0, 0))
        for key_espece in self.ecosys.eco:
            for animal in self.ecosys.eco[key_espece]:
                qp.drawConvexPolygon(animal.poly.shape)

        qp.setPen(QColor(255, 0, 0))
        qp.setBrush(QColor(255, 0, 0))
        qp.drawConvexPolygon(self.ecosys.eco['h'][0].vision.poly.shape)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()

    sys.exit(app.exec_())