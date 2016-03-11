#!/usr/local/bin/python3.4
# -*- coding: Utf-8 -*-

import sys

sys.path.append('../classes_eco/')
sys.path.append('../backward/')
sys.path.append('../res/')
sys.path.append('../interface/')

from abc import abstractmethod, ABCMeta
from PyQt5.QtCore import Qt, QPointF
import random
import numpy as np
from objects import *
from collisions import *


#classe abstraite mère
class Animal(metaclass=ABCMeta):
	"""
	Classe abstraite pour les caractéristiques communes.
	"""
	__vie = 0
	rapidite = 0

	espece = ""
	index = 0

	poly = None
	vision = None
	pas = 0

	sexe = 0

	quota_nourriture = 0
	quota_eau = 0

	eau = 0
	nourriture = 0

	current_state = 0#comportement de l'animal

	@property
	def vie(self):
	    return self.__vie

	@vie.setter
	def vie(self, v):
		if v < 0:
			self.__vie = 0
		else:
			self.__vie = v

	# Création des caractéristiques communes :
	def calcVie(self, jour_ecoule):
		"""
		La méthode gère la perte de vie de l'animal.
		Deux facteurs sont pris en compte:
		- Le vieillissement (1 point de vie en moins chaque jour)
		- La soif/faim. Si l'animal n'a pas son quota d'eau ou de nourriture 
		  par jour, l'animal perd un nombre de points de vie proportionnel
		  au manque.

		La méthode prend en paramètre un booleen jour_ecoule qui indique que l'animal
		doit vieillir.
		"""

		if jour_ecoule:
			#le vieillissement
			self.vie -= 1

			#les quotas
			self.vie -= (self.quota_eau - self.eau)
			self.vie -= (self.quota_nourriture - self.nourriture)

	def manger(self, ressource):
		self.nourriture += ressource.reduction()

	def boire(self, ressource):
		self.eau += ressource.reduction()

	def tourner(self, ressources, eco, angle):
		(collisionedObjects, collBorders) = self.tryRotate(ressources, eco, angle)
		self.vision.update(self.poly.head(), self.poly.heading)

		return (collisionedObjects, collBorders)

	def translater(self, ressources, eco, sens):
		for i in range(self.rapidite):
			(collisionedObjects, collBorders) = self.tryTrans(ressources, eco, sens)
			self.vision.update(self.poly.head(), self.poly.heading)

		return (collisionedObjects, collBorders)


	def tryTrans(self, ressources, eco, sens):
		nbp = self.poly.nbp
		virtual_fig = Triangle(1,1,1,1)

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

		(height, width) = (constantes.nb_carres_hauteur*constantes.carre_res[0], constantes.nb_carres_largeur*constantes.carre_res[1])
		center = virtual_fig.get_center()
		(row, col) = current_case(center.x(), center.y())
		curr_case = ressources[row][col]

		(collisionedObjects, collBorders) = check_collisions(virtual_fig, self.espece, self.index, eco, (height, width))

		if(collBorders and len(collisionedObjects) == 0 and curr_case.passable):
			virtual_fig.shape.swap(self.poly.shape)

		return (collisionedObjects, collBorders)

	def tryRotate(self, ressources, eco, theta):
		nbp = self.poly.nbp
		virtual_fig = Triangle(1,1,1,1)

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

		(height, width) = (constantes.nb_carres_hauteur*constantes.carre_res[0], constantes.nb_carres_largeur*constantes.carre_res[1])
		center = virtual_fig.get_center()
		(row, col) = current_case(center.x(), center.y())
		curr_case = ressources[row][col]

		(collisionedObjects, collBorders) = check_collisions(virtual_fig, self.espece, self.index, eco, (height, width))

		if(collBorders and len(collisionedObjects) == 0 and curr_case.passable):
			virtual_fig.shape.swap(self.poly.shape)
			self.poly.heading = np.mod(self.poly.heading - theta*180/np.pi,360)

		return (collisionedObjects, collBorders)

	@abstractmethod
	def next_state(self, current_case, list_vision, list_touch):
		pass
		

class Herbivore(Animal):
	def __init__(self):
		self.vie = 80
		self.rapidite = 4

		self.pas = 1
		self.poly = Triangle(random.randint(10,300), random.randint(10,300), 8, 15, 90)
		self.vision = Champ_Vison(40, np.pi/8, self.poly.heading)

		self.current_state = 0

	def next_state(self, current_case, list_vision, list_touch):
		'''
		Comportement de Herbivore
		0: suivre les autres
		1: fuire
		2: chercher à manger
		3: manger
		4: chercher à boire
		5: boire
		'''
