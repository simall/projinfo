import constantes
from ressources import *

class Carto(list):
	def __init__(self):
		carte = open(constantes.file_carte)
		num_line = 0

		for line in carte:
			num_col = 0
			self.append([])
			line = line.strip()

			for number in line:
				number = int(number)

				if number == 0:
					self[num_line].append(Terre((num_col*constantes.carre_res[0], num_line*constantes.carre_res[1])))
				elif number == 1:
					self[num_line].append(Herbe((num_col*constantes.carre_res[0], num_line*constantes.carre_res[1])))
				elif number == 2:
					self[num_line].append(Eau((num_col*constantes.carre_res[0], num_line*constantes.carre_res[1])))

				num_col += 1
			num_line += 1

		carte.close()