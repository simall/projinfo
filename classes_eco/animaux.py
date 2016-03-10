#!/usr/local/bin/python3.4
# -*- coding: Utf-8 -*-

import sys
from abc import abstractmethod, ABCMeta
from PyQt5.QtCore import Qt, QPointF
import numpy as np
from objects import *


#classe abstraite mère
class Animal(metaclass=ABCMeta):
	"""
	Classe abstraite pour les caractéristiques communes.
	"""
	vie = 0
	rapidite = 0

	poly = None
	vision = None
	pas = 0

	sexe = 0

	quota_nourriture = 0
	quota_eau = 0

	eau = 0
	nourriture = 0

	# Création des caractéristiques communes :
	@abstractmethod
	def calcVie(self):
		"""
		L'animal vieilit. Les réserves en eau et nourriture de l'animal diminuent.
		"""
		pass	

	def manger(self, ressource):
		self.nourriture += ressource.reduction()

	def boire(self, ressource):
		self.eau += ressource.reduction()

	def tryTrans(self, sens):
		nbp = self.poly.nbp
		virtual_fig = self.poly

		(x1,y1) = (self.poly.head().x(), self.poly.head().y())

		center = self.poly.get_center()
		(x0, y0) = (center.x(), center.y())

		norme = np.sqrt((x1-x0)**2 + (y1-y0)**2)
		v_t = (sens*(x1-x0)*self.pas/norme, sens*(y1-y0)*self.pas/norme)
		Trans = np.array([[1,0,v_t[0]],[0,1,v_t[1]]])#matrice de translation

		for i in range(nbp):
			point = self.poly.shape.at(i)
			pt = np.array([[point.x()],[point.y()],[1]])
			new_point = np.dot(Trans, pt)

			virtual_fig.shape.replace(i, QPointF(new_point[0], new_point[1]))

		virtual_fig.shape.swap(self.poly.shape)

	def tryRotate(self, theta):
		nbp = self.poly.nbp
		virtual_fig = self.poly

		#recuperer les coord du centre de rotation
		center = self.poly.get_center()
		(x0, y0) = (center.x(), center.y())

		#definir la matrice de rotation
		Rot = np.array([[np.cos(theta),-np.sin(theta)], [np.sin(theta), np.cos(theta)]])

		#appliquer la rotation a l'ensemble des points
		for i in range(nbp):
			point = self.poly.shape.at(i)
			pt = np.array([[point.x()-x0],[point.y()-y0]])
			new_point = np.dot(Rot, pt)

			#mettre a jour les points
			virtual_fig.shape.replace(i, QPointF(new_point[0]+x0, new_point[1]+y0))

		virtual_fig.shape.swap(self.poly.shape)
		self.poly.heading = np.mod(self.poly.heading - theta*180/np.pi,360)
		

class Herbivore(Animal):
	def __init__(self):
		self.vie = 80
		self.rapidite = 2

		self.pas = 3
		self.poly = Triangle(50, 50, 8, 15, 90)
		self.vision = Champ_Vison(40, np.pi/8, self.poly.heading)

	def calcVie(self):
		self.vie -= 1
