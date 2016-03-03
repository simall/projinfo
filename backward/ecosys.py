#!/usr/bin/python3.4
# -*- coding: Utf-8 -*-

import sys
from abc import abstractmethod, ABCMeta
from animaux import *
from ressources import *
from carto import *
import constantes

class Ecosys():
	def __init__(self):
		self.nb_jours = 0
		self.curr_cycle = 0
		self.nb_cycles_par_jour = constantes.cyles_par_jour

		self.eco = {}
		self.nb_animaux = {}		
		self.nb_especes = 0
		
		self.carto = Carto()

	def __str__(self):
		string = ''
		string += 'jour '+str(self.nb_jours)+'\n'
		for key_espece in self.eco:
			string += 'espèce '+key_espece+' ('+str(self.nb_animaux[key_espece])+')\n'
			for animal in self.eco[key_espece]:
				string += '\t'+str(animal.vie)+' '+str(animal.nourriture)+'\n'

		return string

	def add_animal(self, animal, nom):
		if nom not in self.eco:
			self.nb_especes += 1

		#ajoute l'animal à la bonne espèce
		Temp = self.eco.get(nom, [])
		Temp.append(animal)
		self.eco[nom] = Temp

		#augmente le nombre d'animaux de l'espèce correspondante
		self.nb_animaux[nom] = self.nb_animaux.get(nom, 0) + 1

	def next_cycle(self):
		'''
		réalise toute les actions pour un cycle
		augmente le nombre de cycles effectués
		gère les jours
		'''
		#pour tous les animaux de l'écosystème, action !
		self.curr_cycle = (self.curr_cycle+1)%self.nb_cycles_par_jour
		if self.curr_cycle == 0:
			self.nb_jours += 1
			#fait tous ce qu'il y a à faire sur les animaux à la fin de la journée
			for espece in self.eco:
				for animal in self.eco[espece]:
					animal.action(self.carto)
					animal.calcVie()

					animal.eau = 0
					animal.nourriture = 0

if __name__ == '__main__':
	eco = Ecosys()
	eco.add_animal(Herbivore(), 'bulbi')
	eco.add_animal(Herbivore(), 'bulbi')

	for i in range(2500):
		eco.next_cycle()

	print(eco)
