#!/usr/local/bin/python3.4
# -*- coding: Utf-8 -*-

import sys
from abc import abstractmethod, ABCMeta
import constantes

#classe abstraite mère
class Ressource(metaclass=ABCMeta):
	"""
	Classe abstraite pour les ressources.
	"""
	cycle_vie = 0
	__quantite = 0

	@abstractmethod
	def reduction(self):
		pass

	@property
	def quantite(self):
	    return self._quantite

	@quantite.setter
	def quantite(self, quantite):
		if quantite >= 0:
			self.__quantite = quantite
		else:
			self.__quantite = 0

class Herbe(Ressource):
	def __init__(self):
		self.cycle_vie = constantes.cyles_par_jour
		self.quantite = 100

	def reduction(self):
		old = self.quantite
		self.quantite -= constantes.bouchee

		if old == self.quantite:
			return False
		else:
			return True
