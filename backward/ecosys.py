#!/usr/bin/python3.4
# -*- coding: Utf-8 -*-

import sys

sys.path.append('../classes_eco/')
sys.path.append('../backward/')
sys.path.append('../res/')
sys.path.append('../interface/')

from animaux import *
from ressources import *
from carto import *
import constantes
import time

from PyQt5.QtCore import QObject, pyqtSignal

class Ecosys(QObject):
	'''
	Créé un écosystème
	'''
	signal = pyqtSignal()

	def __init__(self):
		'''
		Constructeur
		'''
		super().__init__()

		self.nb_jours = 0
		self.curr_cycle = 0
		self.nb_cycles_par_jour = constantes.cyles_par_jour

		self.eco = {}
		self.nb_animaux = {}		
		self.nb_especes = 0
		
		self.carto = ResMap()

	def __str__(self):
		'''
		Définit l'affichage de l'écosystème
		'''
		string = ''
		string += 'jour '+str(self.nb_jours)+'\n'
		for key_espece in self.eco:
			string += 'espèce '+key_espece+' ('+str(self.nb_animaux[key_espece])+')\n'
			for animal in self.eco[key_espece]:
				string += '\t'+str(animal.vie)+' '+str(animal.nourriture)+'\n'

		return string

	def add_animal(self, animal, nom):
		'''
		Ajoute un animal à l'écosystème. Le nom est relatif à chaque espèce
		'''
		if nom not in self.eco:
			self.nb_especes += 1

		#ajoute l'animal à la bonne espèce
		animal.espece = nom

		Temp = self.eco.get(nom, [])
		animal.index = self.nb_animaux.get(nom, 0)
		Temp.append(animal)
		self.eco[nom] = Temp

		#augmente le nombre d'animaux de l'espèce correspondante
		self.nb_animaux[nom] = self.nb_animaux.get(nom, 0) + 1

	def next_cycle(self):
		'''
		Réalise toute les actions pour un cycle
		Augmente le nombre de cycles effectués
		Gère les jours
		'''
		jour_ecoule = False
		(height, width) = (constantes.nb_carres_hauteur*constantes.carre_res[0], constantes.nb_carres_largeur*constantes.carre_res[1])

		#pour tous les animaux de l'écosystème, action !
		self.curr_cycle = (self.curr_cycle+1)%self.nb_cycles_par_jour
		if self.curr_cycle == 0:
			self.nb_jours += 1
			jour_ecoule = True

		#fait tous ce qu'il y a à faire sur les animaux à la fin de la journée
		for espece in self.eco:
			for animal in self.eco[espece]:
				if jour_ecoule:
					animal.nourriture = 0
					animal.eau = 0

				#appel de la current case
				head = animal.poly.head()
				curr_case = current_case(head.x(), head.y())
				#appel de la fonction de collision vision cases
				coll_vision_cases = collision_vision_cases(animal.vision.angle, animal.poly.heading, animal.vision.rayon, self.carto.carte, curr_case, head)
				#appel de la fonction de collision vision animaux
				coll_vision_animaux = collision_vision_animaux(self.eco, animal.espece, animal.index)
				#appel de la fonction de collisions entre animaux
				coll_touch = (check_collisions(animal.poly, animal.espece, animal.index, self.eco, (height, width)))[0]
				#appel de animal.next_state
				animal.next_state(self.carto, self.eco, curr_case, coll_vision_cases, coll_vision_animaux, coll_touch)

				animal.vision.update(animal.poly.head(), animal.poly.heading)
				self.signal.emit()

				animal.calcVie(jour_ecoule)

		self.carto.check_regen_state()
		self.carto.check_dead_state()
		self.carto.check_rotten_state()
		
		if jour_ecoule:
			print(self.nb_jours)

	def is_dead(self, animal):
		'''
		Renvoit True si l'animal passé en paramètre est mort, False sinon
		'''
		if animal.vie == 0:
			return True
		else:
			return False

	def retirer(self, espece, index):
		'''
		Retire un animal de l'écosystème
		'''
		self.eco[espece].pop(index)
		self.nb_animaux[espece] -= 1

if __name__ == '__main__':
	ecosys = Ecosys()
	ecosys.add_animal(Herbivore(), 'h')
	ecosys.add_animal(Herbivore(), 'h')

	ecosys.next_cycle()

	print(ecosys)
