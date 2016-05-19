#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

class Case():
	i = 0
	j = 0

	nb_tours = 0

	def __str__(self):
		text = "[("+str(self.i)+","+str(self.j)+"), "+str(self.nb_tours)+"]"
		return text

class Pile():

	def __init__(self):
		self.contenu = []

	def __str__(self):
		text = ""

		for case in self.contenu:
			text += str(case)
			text += '\n'

		return text

	def is_empty(self):
		return len(self.contenu) == 0

	def put(self, i, j, nb_tours):
		data = Case()

		data.i = i
		data.j = j
		data.nb_tours = nb_tours

		self.contenu.append(data)

	def read(self):
		if self.is_empty() == False:
			return self.contenu[0]
		else:
			return None

	def read_base(self):
		if self.is_empty() == False:
			return self.contenu[-1]
		else:
			return None

	def pop(self):
		if self.is_empty() == False:
			return self.contenu.pop(0)
		else:
			return None


if __name__ == '__main__':
	p=Pile()
	print(p.is_empty())

	p.put(10,20,40)
	p.put(10,40,10)

	print(p.is_empty())
	print(p.read())
	print(p.contenu)
	p.pop()
	print(p.contenu)
