from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QBrush, QColor, QPainter, QPolygonF
from PyQt5.QtCore import Qt, QPointF

from abc import abstractmethod, ABCMeta
import numpy as np

class Shape(metaclass=ABCMeta):
	'''
	Classe abstraite qui permet de définir un polygone
	'''
	def __init__(self, nbp, list_of_points = None, heading = 0):
		'''
		Constructeur
		Prend comme paramêtres:
		- un nombre de points nbp
		- une liste de coordonnées list_of_points (optionnel)
		- un cap heading (optionnel)
		'''
		self.shape = QPolygonF(nbp)
		for i in range(nbp):
			if list_of_points is not None:
				pt = list_of_points[i]
			else:
				pt = (0,0)
			self.shape.replace(i, QPointF(pt[0], pt[1]))
		self.nbp = nbp
		self.heading = heading

	@abstractmethod
	def get_center(self):
		'''
		Méthode abstraite.
		Retourne les coordonnées du centre de gravité du polygone
		'''
		pass

class Triangle(Shape):
	'''
	Classe qui hérite de Shape
	Créé un triangle
	'''
	def __init__(self, x_h, y_h, base, hauteur, heading = 0):
		'''
		Constructeur
		Prend en paramêtres:
		- des coordonnées (x_h,y_h) du sommet représentant la tête de l'animal
		- la taille de la base
		- la taille de la hauteur
		- le cap de la figure (optionnel)
		'''
		
		#(x_h,y_h) le point en "haut" du triangle (fâce à la base)
		#on détermine le point au milieu de la base du triangle
		x1 = x_h - np.cos(-heading*np.pi/180)
		y1 = y_h - np.sin(-heading*np.pi/180)

		norme = np.sqrt((x1 - x_h) ** 2 + (y1 - y_h) ** 2)

		vect_trans = ((x1 - x_h)*hauteur / norme,
		              (y1 - y_h)*hauteur / norme)


		Trans = np.array([[1, 0, vect_trans[0]],
		                  [0, 1, vect_trans[1]]])

		base_point = np.dot(Trans, np.array([[x_h],[y_h],[1]]))

		#on détermine le 2ème sommet
		x1 = base_point[0] - np.cos((heading-90)*np.pi/180)
		y1 = base_point[1] + np.sin((heading-90)*np.pi/180)

		norme = np.sqrt((x1 - base_point[0]) ** 2 + (y1 - base_point[1]) ** 2)

		vect_trans = ((x1 - base_point[0])*base / (2*norme),
		              (y1 - base_point[1])*base / (2*norme))


		Trans = np.array([[1, 0, vect_trans[0]],
		                  [0, 1, vect_trans[1]]])

		p1 = np.dot(Trans, np.array([[base_point[0]], [base_point[1]], [1]]))

		#on détermine le 3ème sommet
		x1 = base_point[0] - np.cos((heading+90)*np.pi/180)
		y1 = base_point[1] + np.sin((heading+90)*np.pi/180)

		norme = np.sqrt((x1 - base_point[0]) ** 2 + (y1 - base_point[1]) ** 2)

		vect_trans = ((x1 - base_point[0])*base / (2*norme),
		              (y1 - base_point[1])*base / (2*norme))


		Trans = np.array([[1, 0, vect_trans[0]],
		                  [0, 1, vect_trans[1]]])

		p2 = np.dot(Trans, np.array([[base_point[0]], [base_point[1]], [1]]))

		list_of_points = [(x_h,y_h), (p1[0], p1[1]), (p2[0], p2[1])]

		super().__init__(3, list_of_points, heading)

		self.head_num = 0

	def head(self):
		'''
		Renvoie le sommet du triangle représentant la tête de l'animal
		'''
		return self.shape.at(self.head_num)

	def get_center(self):
		'''
		Renvoie les coordonnées du centre de gravité du polygone
		'''
		p0 = self.shape.at(0)
		p1 = self.shape.at(1)
		p2 = self.shape.at(2)

		return QPointF((p0.x()+p1.x()+p2.x())/3, (p0.y()+p1.y()+p2.y())/3)

class Champ_Vison():
	'''
	Créé un champ de vision
	'''
	def __init__(self, R, angle, heading):
		'''
		Constructeur
		Prend en paramêtres:
		- un rayon R
		- un angle pour définir l'arc de cercle
		- un cap
		'''
		self.rayon = R
		self.angle = angle

		self.poly = Triangle(1, 1, 1, 1, heading)

	def update(self, anchorPoint, heading):
		'''
		Met à jour la position du champ de vision
		Prends en paramêtres:
		- les coordonnées du point d'ancrage du champ de vision
		- le cap heading
		'''
		(x_h, y_h) = (anchorPoint.x(), anchorPoint.y())

		self.poly.shape.replace(0, QPointF(x_h,y_h))


		x1 = x_h - np.cos((heading+180)*np.pi/180)
		y1 = y_h + np.sin((heading+180)*np.pi/180)

		norme = np.sqrt((x1 - x_h) ** 2 + (y1 - y_h) ** 2)

		vect_trans = ((x1 - x_h)*self.rayon / norme,
		              (y1 - y_h)*self.rayon / norme)


		Trans = np.array([[1, 0, vect_trans[0]],
		                  [0, 1, vect_trans[1]]])  # matrice de translation
		
		#Dessin de la nouvelle figure et suppression de l'autre
		for i in range(1, self.poly.nbp):
			point = self.poly.head()
			pt = np.array([[point.x()], [point.y()], [1]])
			new_point = np.dot(Trans, pt)
			self.poly.shape.replace(i, QPointF(new_point[0], new_point[1]))

		x0 = x_h
		y0 = y_h

		signe = 1

		for i in range(1,self.poly.nbp):
			# definir la matrice de rotation
			theta = signe*self.angle
			Rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

			point = self.poly.shape.at(i)
			pt = np.array([[point.x() - x0], [point.y() - y0]])
			new_point = np.dot(Rot, pt)
			self.poly.shape.replace(i, QPointF(new_point[0] + x0, new_point[1] + y0))
			signe = -1