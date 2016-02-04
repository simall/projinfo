#!/usr/bin/python3.4
# -*- coding: Utf-8 -*-

import sys
from abc import abstractmethod, ABCMeta

#classe abstraite mère
class Animal(metaclass=ABCMeta):
	'''
	classe abstraite
	'''
	vie = 0

	def vieillir(self):
		self.vie -= 1

#les carnivores
class Carnivore(Animal):
	def __init__(self):
		self.vie = 100

class Predateur1(Carnivore):
	def __init__(self):
		super().__init__()

#les herbivores
class Herbivore(Animal):
	def __init__(self):
		self.vie = 80
