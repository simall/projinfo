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
	def CycleVie(self):
		"""
		L'animal vieilit. Les réserves en eau et nourriture de l'animal diminuent.
		"""
		self._vie -= 1
		self._soif -= 1
		self._faim -= 1

	def boire(self):
		"""
		L'animal boit.
		"""
        self_soif = self._max
        # Il boit jusqu'à remplir ses réserves.

		

    def eau_trouvee(self):
    	"""
		l'animal se trouve dans la zone de la carte où se situe l'eau.
    	"""
        self.x <= -16 and abs(self.y) <= 20


	def manger(self):
		"""
		L'animal mange.
		"""
		self._faim = self._max


	@abstractmethod
	def nourriture_trouvee(self):
		"""
		Méthode abstraite : doit être redéfinie dans les sous-classes.
		"""
		pass


	@abstractmethod
	def action(self, animal):
		"""
		Méthode abstraite : doit être redéfinie dans les sous-classes.
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
### Est ce que ces propriétés ne pourraient pas être définie de façon générale pour tous les animaux ?
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
		pass

	def a_faim(self):
		self._faim <= 0

    def a_soif(self):
    	self._soif <= 0

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
		pass



class Fuite(Animal):
	"""
	Comportement d'un animal effrayé.
	"""
	def action(self,herbivore):
		# L'herbivore va tenter de s'enfuir.
		s_echapper = self.bouger(herbivore)
		if s_echapper :
			# Si l'herbivore réussit à s'échapper : retour à son comportement normal.
			herbivore.change_comportement(Normal_Herbivore())

	def bouger(self,herbivore):
		# 50% de chances de s'échapper.
		return np.random.rand() < 0.5

class Faim(Animal):
	"""
	Comportement d'un herbivore affamé.
	"""
	def action(self, herbivore):
		# L'herbivore cherche de la nourriture.
		trouve = self.nourriture_trouvee()
		# L'herbivore a trouvé de la nourriture.
		if herbivore.detecte_predateur:
			# Si l'herbivore détecte un prédateur : tentative de fuite
			herbivore.change_comportement(Fuite())
		elif trouve:
			# Sinon l'herbivore mange.
			herbivore.manger()
			# Une fois qu'il est rassasié : retour à son comportement normal.
			herbivore.change_comportement(Normal_Herbivore())

	def nourriture_trouvee(self):
		"""
		Spécifique aux herbivores : l'animal se trouve dans la zone de la carte où se situe la nourriture.
		"""
		abs(self.x) <= -4 and abs(self.y) <= 4



class Soif(Animal):
	"""
	Comportement d'un herbivore assoiffé.
	"""
	def action(self,herbivore):
		# L'herbivore cherche de l'eau.
		trouve = herbivore.eau_trouvee()
		# L'herbivore a trouvé de l'eau.
		if herbivore.detecte_predateur:
			# Si l'herbivore détecte un prédateur : tentative de fuite
			herbivore.change_comportement(Fuite())
		elif trouve:
			# Sinon l'herbivore boit.
			herbivore.boire()
			# L'herbivore a suffisament mangé : retour à son comportement normal.
			herbivore.change_comportement(Normal_Herbivore())



#les carnivores
class Carnivore(Animal):
	def __init__(self):
		self._vie = 100

class Predateur1(Carnivore):
	def __init__(self):
		super().__init__()


