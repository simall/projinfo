#!/usr/local/bin/python3.4
# -*- coding: Utf-8 -*-

import sys
import numpy as np
from abc import abstractmethod, ABCMeta


#classe abstraite mère
class Animal(metaclass=ABCMeta):
	"""
	Classe abstraite pour les caractéristiques communes.
	"""
	vie = 0
	rapidite = 0
	vision = (0,0)
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

	@abstractmethod
	def action(self, animal):
		"""
		Méthode abstraite : doit être redéfinie dans les sous-classes.
		"""
		pass

	@abstractmethod
	def bouger(self, animal):
		pass

	@abstractmethod
	def manger(self, animal):
		pass

	
	def comportement_normal(self, animal):
		pass

	@abstractmethod
	def boire(self):
		pass

	def fuite(self, animal):
		s_echapper = np.random.rand()
		# L'animal a une chance sur deux de s'enfuir.
		if s_echapper < 0.5:
			# L'animal réussit à s'échapper.
			self.comportement_normal()

	def a_faim(self):
		if self.nourriture == 0:
			print("J'ai faim !")

		#rajouter si nourriture dans le champ de vision -> se déplacer vers elle

	def a_soif(self):
		if self.eau == 0:
			print("J'ai soif !")

		#rajouter si eau dans le champ de vision -> se déplacer vers elle

	def champ_de_vision(self):
		pass


	def detecte_nourriture(self):
		pass



class Herbivore(Animal):
	"""
	Animal grégaire quand il n'est pas en recherche de nourriture. Il s'enfuit à l'approche d'un prédateur.
	Détection d'un prédateur : probabilité inversemement proportionnelle à la distance du prédateur.
	Animal possédant un comportement décrit par un automate.
	"""

	def __init__(self):
		self.vie = 80
		self.rapidite = 10
		self.vision = (5,10)
		self.quota_nourriture = 5
		self.quota_eau = 3

	def calcVie(self):
		self.vie -= 1

	def bouger(self):
		pass

	def manger(self):
		while nourriture != quota_nourriture:
			if self.detecte_predateur():
				Animal.fuite(herbivore)
				break
			else:
				nourriture += 1

	def boire(self):
		while eau != quota_eau:
			if self.detecte_predateur():
				Animal.fuite(herbivore)
				break
			else:
				eau += 1

	def detecte_predateur(self):
		# prédateur dans le champ de vision 
		pass

	def action(self, ressource, ):
		"""
		Cas où l'herbivore sera contraint de changer de comportement.
		"""
		self.bouger()
		if self.detecte_predateur():
			# Prédateur détecté : nouveau comportement : fuite.
			Animal.fuite()
		elif Animal.a_faim(self):
			# Herbivore affamé : chercher de la nourriture.
			self.manger()
		elif Animal.a_soif(self):
			# Herbivore assoiffé : chercher de l'eau.
			self.boire()



		print("je mange")
		ressource[44][27].reduction()








class Predateur(Animal):
	def __init__(self):
		self.vie = 30
		self.rapidite = 40
		self.vision = (5,10)

	def calcVie(self):
		self.vie -= 1

	def action(self, ressource):
		pass

class Charognard(Animal):
	def __init__(self):
		self.vie = 30
		self.rapidite = 30
		self.vision = (5,10)

	def calcVie(self):
		self.vie -= 1

	def action(self,ressource):
		pass
