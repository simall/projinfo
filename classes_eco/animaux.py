#!/usr/bin/python3.4
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
from fsm import *


#classe abstraite mère
class Animal(metaclass=ABCMeta):
	'''
	Classe abstraite pour les caractéristiques communes.
	'''
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

	comportement = None

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
		'''
		La méthode gère la perte de vie de l'animal.
		Deux facteurs sont pris en compte:
		- Le vieillissement (1 point de vie en moins chaque jour)
		- La soif/faim. Si l'animal n'a pas son quota d'eau ou de nourriture 
		  par jour, l'animal perd un nombre de points de vie proportionnel
		  au manque.

		La méthode prend en paramètre un booleen jour_ecoule qui indique que l'animal
		doit vieillir.
		'''

		if jour_ecoule:
			#le vieillissement
			self.vie -= 1

			#les quotas
			self.vie -= (self.quota_eau - self.eau)
			self.vie -= (self.quota_nourriture - self.nourriture)

	def manger(self, ressource):
		'''
		Nourrit l'animal avec la ressource passée en paramètre
		'''
		self.nourriture += ressource.reduction()

	def boire(self, ressource):
		'''
		Hydrate l'animal avec la ressource passée en paramètre
		'''
		self.eau += ressource.reduction()

	def tourner(self, ressources, eco, angle):
		'''
		Fait tourner l'animal
		Prend en paramètres:
		- la carte des ressources
		- l'ensemble des animaux de l'écosystème
		- un angle de rotation
		'''
		(collisionedObjects, collBorders) = self.tryRotate(ressources, eco, angle)
		self.vision.update(self.poly.head(), self.poly.heading)

		return (collisionedObjects, collBorders)

	def translater(self, ressources, eco, sens):
		'''
		Fait avancer/tourner l'animal
		Prend en paramètres:
		- la carte des ressources
		- l'ensemble des animaux de l'écosystème
		- un sens de translation
		'''
		for i in range(self.rapidite):
			(collisionedObjects, collBorders) = self.tryTrans(ressources, eco, sens)
			self.vision.update(self.poly.head(), self.poly.heading)

		return (collisionedObjects, collBorders)


	def tryTrans(self, ressources, eco, sens):
		'''
		Créé une figure virtuelle et vérifie que l'animal peut bouger
		Prend en paramètres:
		- la carte des ressources
		- l'ensemble des animaux de l'écosystème
		- un angle de sens de translation
		'''
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
		'''
		Créé une figure virtuelle et vérifie que l'animal peut bouger
		Prend en paramètres:
		- la carte des ressources
		- l'ensemble des animaux de l'écosystème
		- un angle de rotation
		'''
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
	def next_state(self, current_case, list_vision_cases, list_vision_eco):
		'''
		Méthode abstraite
		Détermine le comportement de l'animal
		'''
		pass
		

class Herbivore(Animal):
	'''
	Créé un herbivore
	'''
	def __init__(self):
		'''
		Constructeur
		'''
		self.vie = 80
		self.rapidite = 4

		self.pas = 1
		self.poly = Triangle(random.randint(10,300), random.randint(10,300), 4, 6, 90)
		self.vision = Champ_Vison(60, np.pi/8, self.poly.heading)

		self.quota_eau = 50
		self.quota_nourriture = 100

		self.eau = 50
		self.nourriture = 100

		self.comportement = FSM()

		#définition du comportement
		self.comportement.add_state("suivre")
		self.comportement.add_state("chercher_nourriture")
		self.comportement.add_state("manger")
		self.comportement.add_state("chercher_eau")
		self.comportement.add_state("boire")
		self.comportement.add_state("fuir")

		self.comportement.add_event("faim")
		self.comportement.add_event("nourriture_trouvee")
		self.comportement.add_event("retour_normal")
		self.comportement.add_event("soif")
		self.comportement.add_event("eau_trouvee")
		self.comportement.add_event("danger")

		self.comportement.add_transition("suivre", "retour_normal", "suivre", doFollow)
		self.comportement.add_transition("suivre", "faim", "chercher_nourriture", doLookFood)
		self.comportement.add_transition("suivre", "soif", "chercher_eau", doLookWater)
		self.comportement.add_transition("suivre", "danger", "fuir", doEscape)

		self.comportement.add_transition("chercher_nourriture", "faim", "chercher_nourriture", doLookFood)
		self.comportement.add_transition("chercher_nourriture", "nourriture_trouvee", "manger", doEat)
		self.comportement.add_transition("chercher_nourriture", "danger", "fuir", doEscape)

		self.comportement.add_transition("manger", "nourriture_trouvee", "manger", doEat)
		self.comportement.add_transition("manger", "retour_normal", "suivre", doFollow)
		self.comportement.add_transition("manger", "danger", "fuir", doEscape)
		self.comportement.add_transition("manger", "faim", "chercher_nourriture", doLookFood)

		self.comportement.add_transition("chercher_eau", "soif", "chercher_eau", doLookWater)
		self.comportement.add_transition("chercher_eau", "eau_trouvee", "boire", doDrink)
		self.comportement.add_transition("chercher_eau", "danger", "fuir", doEscape)

		self.comportement.add_transition("boire", "eau_trouvee", "boire", doDrink)
		self.comportement.add_transition("boire", "retour_normal", "suivre", doFollow)
		self.comportement.add_transition("boire", "danger", "fuir", doEscape)

		self.comportement.add_transition("fuir", "danger", "fuir", doEscape)
		self.comportement.add_transition("fuir", "retour_normal", "suivre", doFollow)

		self.comportement.currentState = "suivre"
		self.comportement.currentEvent = "retour_normal"

	def next_state(self, ressources, eco, current_case, list_vision_cases, list_vision_eco, list_touch_cases):
		event = (self.comportement.run())(self, ressources, eco, current_case, list_vision_cases, list_vision_eco, list_touch_cases)
		self.comportement.currentEvent = event


class Pretadeur(Animal):

	def __init__(self):
		'''
		Constructeur
		'''
		self.vie = 40
		self.rapidite = 6

		self.pas = 1
		self.poly = Triangle(random.randint(10,300), random.randint(10,300), 4, 6, 90)
		self.vision = Champ_Vison(80, np.pi/12, self.poly.heading)

		self.quota_eau = 50
		self.quota_nourriture = 100

		self.eau = 50
		self.nourriture = 100

		self.comportement = FSM()

		# Définition du comportement
		self.comportement.add_state("se_balader")
		self.comportement.add_state("chercher_nourriture")
		self.comportement.add_state("manger")
		self.comportement.add_state("chercher_eau")
		self.comportement.add_state("boire")

		self.comportement.add_event("faim")
		self.comportement.add_event("proie_tuee")
		self.comportement.add_event("retour_normal")
		self.comportement.add_event("soif")
		self.comportement.add_event("eau_trouvee")

		self.comportement.add_transition("se_balader", "retour_normal", "se_ballader", doMove)
		self.comportement.add_transition("se_balader", " faim", "chercher_nourriture", doLookPrey)
		self.comportement.add_transition("se_balader", "soif", "chercher_eau", doLookWater)

		self.comportement.add_transition("chercher_nourriture", "faim", "chercher_nourriture", doLookPrey)
		self.comportement.add_transition("chercher_nourriture", "proie_tuee", "manger", doEatPrey)

		self.comportement.add_transition("manger", "proie_tuee", "manger", doEatPrey)
		self.comportement.add_transition("manger", "retour_normal", "se_balader", doMove)

		self.comportement.add_transition("chercher_eau", "soif", "chercher_eau", doLookWater)
		self.comportement.add_transition("chercher_eau", "eau_trouvee", "boire", doDrink)

		self.comportement.add_transition("boire", "eau_trouvee", "boire", doDrink)
		self.comportement.add_transition("boire", "retour_normal", "se_balader", doMove)

	def next_state(self, ressources, eco, current_case, list_vision_cases, list_vision_eco, list_touch_cases):
		event = (self.comportement.run())(self, ressources, eco, current_case, list_vision_cases, list_vision_eco, list_touch_cases)
		self.comportement.currentEvent = event
