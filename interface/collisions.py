#!/usr/bin/python3.4
import random
import constantes
from PyQt5.QtCore import Qt, QPointF

def current_case(x_h, y_h):
    return (int(y_h//constantes.carre_res[1]), int(x_h//constantes.carre_res[0]))

def check_borders(fig, size_x, size_y):
    for i in range(fig.nbp):
        pt = fig.shape.at(i)

        if pt.x() < 0 or pt.x() > size_x:
            return False

        if pt.y() < 0 or pt.y() > size_y:
            return False
    return True


def check_rect_coll(fig, ofig):
    frect = fig.shape.boundingRect()  # retourne le rectangle qui englobe le polygone
    orect = ofig.shape.boundingRect()

    if frect.left() > orect.right() or frect.right() < orect.left() or frect.top() > orect.bottom() or frect.bottom() < orect.top():
        return False
    else:
        return True

def intersectSegment(A, B, I, P):
    D = QPointF(float(B.x() - A.x()), float(B.y() - A.y()))

    E = QPointF(float(P.x() - I.x()), float(P.y() - I.y()))

    det = D.x()*E.y() - D.y()*E.x()

    if det == 0:
        return -1

    t = - (A.x()*E.y()-I.x()*E.y()-E.x()*A.y()+E.x()*I.y()) / det
    if t < 0 or t >= 1:
        return 0

    u = - (-D.x()*A.y()+D.x()*I.y()+D.y()*A.x()-D.y()*I.x()) / det
    if u < 0 or u >= 1:
        return 0

    return 1

def check_glob_coll(fig, ofig):
    I = QPointF(100000.0+random.randint(0,100),100000.0+random.randint(0,100))

    for i in range(fig.nbp):
        P = fig.shape.at(i)
        nb_intersect = 0

        for j in range(ofig.nbp):
            A = ofig.shape.at(j)
            if j == ofig.nbp-1:
                B = ofig.shape.at(0)
            else:
                B = ofig.shape.at(j+1)

            nb_inter = intersectSegment(A, B, I, P)
            if nb_inter == -1:
                return check_glob_coll(fig, ofig)
            nb_intersect += nb_inter
        if nb_intersect%2 == 1:
            return True

    for i in range(ofig.nbp):
        P = ofig.shape.at(i)
        nb_intersect = 0

        for j in range(fig.nbp):
            A = fig.shape.at(j)
            if j == fig.nbp-1:
                B = fig.shape.at(0)
            else:
                B = fig.shape.at(j+1)

            nb_inter = intersectSegment(A, B, I, P)
            if nb_inter == -1:
                return check_glob_coll(fig, ofig)
            nb_intersect += nb_inter
        if nb_intersect%2 == 1:
            return True

    return False



'''
Check les collisions, d'abord par rectangle vu que c'est super rapide, puis si il y a collision
on check avec la méthode par polygones
Si il y a collision on retourne l'objet collisionné
'''
def check_collisions(fig, key_espece, index, eco, scene):

    collisionedObjects = []
    collBorders = check_borders(fig, scene[0], scene[1])

    if collBorders:
        for espece in eco:
            for i in range(0, len(eco[espece])):
                if espece != key_espece or index != i:
                    ofig = eco[espece][i].poly
        
                    if check_rect_coll(fig, ofig):
                        if check_glob_coll(fig, ofig):
                            collisionedObjects.append(eco[espece][i])

    return (collisionedObjects, collBorders)
