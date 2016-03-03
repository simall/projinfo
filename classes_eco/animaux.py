#!/usr/local/bin/python3.4
# -*- coding: Utf-8 -*-

import sys
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

class Herbivore(Animal):
	def __init__(self):
		self.vie = 80
		self.rapidite = 10
		self.vision = (5,10)

	def calcVie(self):
		self.vie -= 1

	def action(self, ressource):
		print("je mange")
		ressource[44][27].reduction()
