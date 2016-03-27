# -*- coding: utf-8 -*-

class Element():
	"""
	Crée un élément contenant des données.
	"""

	def __init__(self, data):
		"""
		Constructeur.
		"""
		self.content = data
		self.next = None

	def __str__(self):
		"""
		Affiche le contenu de l'élément.
		"""
		return "\n " + str(self.content)

class Liste():
	"""
	Création de la liste en ajoutant ou supprimant des éléments.
	"""

	def __init__(self):
		"""
		Constructeur. Création d'un premier élément (fantôme).
		"""
		self.first = Element(None)

	def est_vide(self):
		"""
		Renvoie True si la liste est vide. False sinon.
		"""
		if self.first.next is None:
			return True
		return False

	def insert(self, data, idx):
		"""
		Crée un élément à l'aide de la classe Element(), puis l'insert conformément à l'indice choisi.
		Dans le cas où l'indice est identique à un autre élément, la méthode l'insert avant l'élement 
		de l'indice répété.
		"""
		new_element = Element(data)
		cur_element = self.first
		idx_element = 0
		while cur_element.next is not None and idx_element != idx:
			cur_element = cur_element.next
			idx_element += 1
		tmp = cur_element.next
		new_element.next = tmp
		cur_element.next = new_element

	def lire_fin(self):
		"""
		Renvoie le dernier élément de la liste.
		"""
		if self.est_vide() == False:
			cur_element = self.first
			while cur_element.next is not None:
				cur_element = cur_element.next
			return cur_element.content

	def supprime_element(self,data):
		"""
		Recherche un élément en fonction de son contenu et le supprime.
		Méthode plus générale qui ne s'applique pas uniquement l'élément de la fin de la liste.
		"""
		if self.est_vide() == False:
			cur_element = self.first
			prev_element = None
			while cur_element.next is not None:
				if data == cur_element.next.content:
					cur_element.next = cur_element.next.next
				else:
					prev_element = cur_element
					cur_element = cur_element.next

	def __str__(self):
		"""
		Affiche la liste des éléments.
		"""
		elt = self.first
		content_str = "Les éléments de cette liste sont : "
		while elt is not None:
			content_str += str(elt)
			elt = elt.next
		return content_str

if __name__ == '__main__':
	lst = Liste()
	print(lst.est_vide())
	lst.insert(10, 0)
	lst.insert(20, 0)
	lst.insert(30, 0)
	lst.insert(40, 0)
	lst.insert(20, 0)
	print(lst)
	print(lst.est_vide())
	print(lst.supprime_element(lst.lire_fin))
	print(lst)

