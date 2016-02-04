#!/usr/bin/python3.4
# -*- coding: Utf-8 -*-

import sys
import numpy as np
from abc import abstractmethod, ABCMeta


#classe abstraite mère
class Animal(metaclass=ABCMeta):
	"""
	Classe abstraite pour les caractéristiques communes.
	"""

    # Création des caractéristiques communes :
	def vieillir(self):
		"""
		Méthode caractérisant la vieillesse de l'animal.
		"""
		self._vie -= 1

	@abstractmethod
	def action(self, animal):
		"""
		Méthode abstraite : doit être redéfinie dans les sous-classes
		"""
		pass


#les herbivores :
class Herbivore(Animal):
	"""
	Animal grégaire quand il n'est pas en recherche de nourriture. Il s'enfuit à l'approche d'un prédateur.
	Détection d'un prédateur : probabilité inversemement proportionnelle à la distance du prédateur.
	Animal possédant un comportement décrit par un automate.
	"""

	def __init__(self, vie, faim, soif, capacite=5,comportement, abscisse, ordonnee):
		self._vie = 80
		self._faim = 5
		self._soif = 5
		self._max = capacite
		self._comportement = Normal_Herbivore()
		self.x = abscisse
        self.y = ordonnee

#########
### Est ce que ces propriétés ne seraient pas à définir de façon générale pour tous les animaux ?
#########

   	@property
    def x(self):
        return self.__x
    @x.setter
    def x(self, abscisse):
        if abscisse > 20:
            self.__x = 20
        elif abscisse < -20:
            self.__x = -20
        else:
            self.__x = abscisse

    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self, ordonnee):
        if ordonnee > 20:
            self.__y = 20
        elif ordonnee <- 20:
            self.__y = -20
        else:
            self.__y = ordonnee
############

	def detecte_predateur(self):
		"""
		Détection d'un prédateur : probabilité inversemement proportionnelle à la distance du prédateur.
		"""
		### ?????

	def a_faim(self):
        self._faim -= 1
        if abs(self.x)<=4 and abs(self.y)<=4:
            self._faim = self._max
            print("Je mange")
        if self._faim <= 0:
            print("Je cherche toujours à manger")

    def a_soif(self):
        self._soif -= 1
        if self.x<=-16 and abs(self.y)<=20:
            self_soif = self._max
            print("Je bois")
        if self._soif <= 0:
            print("Je cherche toujours à boire")	

    def change_comportement(self, nouv_comportement):
    	self._comportement = nouv_comportement



class Normal_Herbivore(Animal):
	"""
	Sous-classe de Animal qui définit le comportement standard d'un herbivore.
	"""

	def action(self, herbivore):
		"""
		Cas où l'herbivore sera contraint de changer de comportement.
		"""
		self.bouger(herbivore)
		if herbivore.detecte_predateur():
			# Prédateur détecté : nouveau comportement : fuite.
			herbivore.change_comportement(Fuite())
		elif herbivore.a_faim():
			# Herbivore affamé : chercher de la nourriture.
			herbivore.change_comportement(Faim())
		elif herbivore.a_soif():
			# Herbivore assoiffé : chercher de l'eau.
			herbivore.change_comportement(Soif())

	def bouger(self,herbivore):
		"""
		Déplacement de l'herbivore : cherche la compagnie de ses semblables.
		"""
		### ????



class Fuite(Herbivore):

class Faim(Herbivore):

class Soif(Herbivore):


#les carnivores
class Carnivore(Animal):
	def __init__(self):
		self._vie = 100

class Predateur1(Carnivore):
	def __init__(self):
		super().__init__()
