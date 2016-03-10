#!/usr/local/bin/python3.4
# -*- coding: Utf-8 -*-

import sys
from abc import abstractmethod, ABCMeta
import constantes

from PyQt5.QtCore import QRectF

#classe abstraite mère
class Ressource(metaclass=ABCMeta):
	"""
	Classe abstraite pour les ressources.
	"""
	cycle_vie = 0
	__quantite = 0
	id_res = ''

	@abstractmethod
	def reduction(self):
		pass

	@property
	def quantite(self):
	    return self.__quantite

	@quantite.setter
	def quantite(self, quantite):
		if quantite >= 0:
			self.__quantite = quantite
		else:
			self.__quantite = 0

class Herbe(Ressource):
	def __init__(self, pos):
		self.cycle_vie = constantes.cyles_par_jour
		self.quantite = 100
		self.id_res = 1

		self.rect = QRectF(pos[0], pos[1], constantes.carre_res[0], constantes.carre_res[1])

	def reduction(self):
		old = self.quantite
		self.quantite -= constantes.bouchee

		return (old-self.quantite)

class Eau(Ressource):
	def __init__(self, pos):
		self.cycle_vie = -1#ressource infinie
		self.quantite = -1
		self.id_res = 2

		self.rect = QRectF(pos[0], pos[1], constantes.carre_res[0], constantes.carre_res[1])

	def reduction(self):
		return constantes.bouchee

class Terre():
	def __init__(self, pos):
		self.id_res = 0
		self.rect = QRectF(pos[0], pos[1], constantes.carre_res[0], constantes.carre_res[1])
