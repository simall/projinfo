#!/usr/bin/python3.4
# -*- coding: Utf-8 -*-

from math import atan2, sqrt
import numpy as np
import random
import constantes
from collisions import sens_trigo

compteur = 0

def doFollow(animal, ressources, eco, current_case, coll_vision_cases, coll_vision_eco, coll_touch):
	global compteur
	event = "retour_normal"
	herbi = None
	dist = 0

	head = animal.poly.shape.at(0)
	
	for elt in coll_vision_eco:
		if elt.espece == 'p':
			event = "danger"
			compteur = 8#8 tours de fuite, même s'il ne voit plus le prédateur
			return event
		elif elt.espece == 'h':
			if herbi is None:
				herbi = elt
				center = herbi.poly.get_center()
				dist = (head.x() - center.x())**2 + (head.y() - center.y())**2
			else:
				center = elt.poly.get_center()
				dist_calc = (head.x() - center.x())**2 + (head.y() - center.y())**2
				if dist_calc < dist:
					dist = dist_calc
					herbi = elt

	dist = sqrt(dist)

	if herbi is None:
		angle = random.uniform(-np.pi/2, np.pi/2)

		animal.tourner(ressources.carte, eco, angle)
		animal.translater(ressources.carte, eco, 1)
	else:
		if dist > 20:
			center = herbi.poly.get_center()
			head.setY(-head.y()+constantes.carre_res[1]*constantes.nb_carres_hauteur)
			center.setY(-center.y()+constantes.carre_res[1]*constantes.nb_carres_hauteur)

			angle = sens_trigo(atan2(center.y() - head.y(), center.x() - head.x()))

			animal.tourner(ressources.carte, eco, animal.poly.heading*np.pi/180 - angle)
			animal.translater(ressources.carte, eco, 1)

	if animal.eau < animal.quota_eau:
		event = "soif"
	elif animal.nourriture < animal.quota_nourriture:
		event = "faim"

	return event

def doLookFood(animal, ressources, eco, current_case, coll_vision_cases, coll_vision_eco, coll_touch):
	global compteur
	event = "faim"
	herbe = None
	dist = 0

	head = animal.poly.shape.at(0)

	for elt in coll_vision_eco:
		if elt.espece == 'p':
			event = "danger"
			compteur = 8
			return event

	case = ressources.carte[current_case[0]][current_case[1]]

	if case.id_res == 1:
		event = "nourriture_trouvee"
	else:
		for elt in coll_vision_cases:
			if elt.id_res == 1:
				if herbe is None:
					herbe = elt
					center = herbe.rect.center()
					dist = (head.x() - center.x())**2 + (head.y() - center.y())**2
				else:
					center = elt.rect.center()
					dist_calc = (head.x() - center.x())**2 + (head.y() - center.y())**2
					if dist_calc < dist:
						dist = dist_calc
						herbe = elt

		if herbe is None:
			angle = random.uniform(-np.pi/2, np.pi/2)

			animal.tourner(ressources.carte, eco, angle)
			animal.translater(ressources.carte, eco, 1)
		else:
			center = herbe.rect.center()
			head.setY(-head.y()+constantes.carre_res[1]*constantes.nb_carres_hauteur)
			center.setY(-center.y()+constantes.carre_res[1]*constantes.nb_carres_hauteur)

			angle = sens_trigo(atan2(center.y() - head.y(), center.x() - head.x()))

			animal.tourner(ressources.carte, eco, animal.poly.heading*np.pi/180 - angle)
			animal.translater(ressources.carte, eco, 1)

	return event

def doLookWater(animal, ressources, eco, current_case, coll_vision_cases, coll_vision_eco, coll_touch):
	global compteur
	event = "soif"
	eau = None
	dist = 0

	head = animal.poly.shape.at(0)

	for elt in coll_vision_eco:
		if elt.espece == 'p':
			event = "danger"
			compteur = 8
			return event

	case = ressources.carte[current_case[0]][current_case[1]]

	if case.id_res == 2:
		event = "eau_trouvee"
	else:
		for elt in coll_vision_cases:
			if elt.id_res == 2:
				if eau is None:
					eau = elt
					center = eau.rect.center()
					dist = (head.x() - center.x())**2 + (head.y() - center.y())**2
				else:
					center = elt.rect.center()
					dist_calc = (head.x() - center.x())**2 + (head.y() - center.y())**2
					if dist_calc < dist:
						dist = dist_calc
						eau = elt

		if eau is None:
			angle = random.uniform(-np.pi/2, np.pi/2)

			animal.tourner(ressources.carte, eco, angle)
			animal.translater(ressources.carte, eco, 1)
		else:
			center = eau.rect.center()
			head.setY(-head.y()+constantes.carre_res[1]*constantes.nb_carres_hauteur)
			center.setY(-center.y()+constantes.carre_res[1]*constantes.nb_carres_hauteur)

			angle = sens_trigo(atan2(center.y() - head.y(), center.x() - head.x()))

			animal.tourner(ressources.carte, eco, animal.poly.heading*np.pi/180 - angle)
			animal.translater(ressources.carte, eco, 1)

	return event

def doEat(animal, ressources, eco, current_case, coll_vision_cases, coll_vision_eco, coll_touch):
	global compteur
	event = "nourriture_trouvee"

	case = ressources.carte[current_case[0]][current_case[1]]
	animal.manger(case)

	if case.quantite == 0:
		ressources.regen(current_case[0], current_case[1])
		event = "faim"
		#print("nourriture:", animal.nourriture, "eau:", animal.eau, "event:", event, "state:", animal.comportement.currentState)

	for elt in coll_vision_eco:
		if elt.espece == 'p':
			event = "danger"
			compteur = 8
			return event

	if animal.nourriture >= animal.quota_nourriture:
		event = "retour_normal"
		return event

	return event

def doDrink(animal, ressources, eco, current_case, coll_vision_cases, coll_vision_eco, coll_touch):
	global compteur
	event = "eau_trouvee"

	case = ressources.carte[current_case[0]][current_case[1]]
	animal.boire(case)

	for elt in coll_vision_eco:
		if elt.espece == 'p':
			event = "danger"
			compteur = 8
			return event

	if animal.eau >= animal.quota_eau:
		event = "retour_normal"

	return event

def doEscape(animal, ressources, eco, current_case, coll_vision_cases, coll_vision_eco, coll_touch):
	global compteur
	event = "danger"

	head = animal.poly.shape.at(0)
	head.setY(-head.y()+constantes.carre_res[1]*constantes.nb_carres_hauteur)

	if compteur == 0:
		event = "retour_normal"
		return event

	for elt in coll_vision_eco:
		if elt.espece == 'p':
			center = elt.poly.get_center()
			center.setY(-center.y()+constantes.carre_res[1]*constantes.nb_carres_hauteur)

			angle = sens_trigo(atan2(center.y() - head.y(), center.x() - head.x()))

			animal.tourner(ressources.carte, eco, angle-np.pi)
			animal.translater(ressources.carte, eco, 1)
			compteur -= 1
			return event

	# if len(coll_touch) == 0:
	# 	animal.translater(ressources.carte, eco, 1)
	# else:
	# 	angle = ([-1,1][random.randint(0,1)])*np.pi/2
	# 	animal.tourner(ressources.carte, eco, angle)
	# 	animal.translater(ressources.carte, eco, 1)
	animal.translater(ressources.carte, eco, 1)

	compteur -= 1
	return event

class FSM():
	def __init__(self):
		self.transitions = {}
		self.events = []
		self.states = []

		self.currentEvent = None
		self.currentState = None

	def add_state(self, state):
		self.states.append(state)

	def add_event(self, event):
		self.events.append(event)

	def add_transition(self, state1, event, state2, func):
		key = state1+'.'+event
		self.transitions[key] = (state2, func)

	def run(self):
		key = self.currentState+'.'+self.currentEvent

		(s, f) = self.transitions[key]
		self.currentState = s

		return f