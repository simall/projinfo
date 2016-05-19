import constantes
from ressources import *
from pile import Pile

class ResMap():
	'''
	Créé une carte des ressources
	'''
	def __init__(self):
		'''
		Constructeur
		'''
		fichier = open(constantes.file_carte)
		num_line = 0

		self.carte = []
		self.drained_herb = Pile()
		self.dead_prey = Pile()
		self.rotten_prey = Pile()

		self.prev_case = 0

		for line in fichier:
			num_col = 0
			self.carte.append([])
			line = line.strip()

			for number in line:
				number = int(number)

				if number == 0:
					self.carte[num_line].append(Terre((num_col*constantes.carre_res[0], num_line*constantes.carre_res[1])))
				elif number == 1:
					self.carte[num_line].append(Herbe((num_col*constantes.carre_res[0], num_line*constantes.carre_res[1])))
				elif number == 2:
					self.carte[num_line].append(Eau((num_col*constantes.carre_res[0], num_line*constantes.carre_res[1])))

				num_col += 1
			num_line += 1

		fichier.close()

	def regen(self, i, j):
		cmpt = self.drained_herb.read_base()

		if cmpt is not None:
			reste = cmpt.nb_tours
		else:
			reste = 0

		self.drained_herb.put(i, j, constantes.cycles_regen - reste)
		(self.carte[i][j]).id_res = -(self.carte[i][j]).id_res #met en état épuisé

	def check_regen_state(self):
		elt = self.drained_herb.read()

		if elt is not None:
			if elt.nb_tours <= 0:
				(self.carte[elt.i][elt.j]).id_res = -(self.carte[elt.i][elt.j]).id_res #met en état open

				self.drained_herb.pop()
				self.check_regen_state()
			else:
				elt.nb_tours -= 1


	def dead(self, i, j):
		cmpt = self.dead_prey.read_base()

		if cmpt is not None:
			reste = cmpt.nb_tours
		else:
			reste = 0

		self.dead_prey.put(i, j, constantes.cycles_dead - reste)
		self.prev_case = (self.carte[i][j]).id_res
		(self.carte[i],[j]).id_res = 3

	def check_dead_state(self):
		elt = self.dead_prey.read()

		if elt is not None:
			if elt.nb_tours <= 0:
				(self.carte[elt.i][elt.j]).id_res = -(self.carte[elt.i][elt.j]).id_res #cadavre périmé

				self.rotten_prey.put(i, j, constantes.cycles_rotten)
				self.dead_prey.pop()
				self.check_dead_state()
			else:
				elt.nb_tours -= 1


	def check_rotten_state(self):
		elt = self.rotten_prey.read()

		if elt is not None:
			if elt.nb_tours <= 0:
				(self.carte[elt.i][elt.j]).id_res = self.prev_case

				self.rotten_prey.pop()
				self.check_rotten_state()
			else:
				elt.nb_tours -= 1
