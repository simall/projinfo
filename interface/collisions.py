#!/usr/bin/python3.4
# -*- coding: Utf-8 -*-

import random
import constantes
import numpy as np
from math import atan2
from PyQt5.QtCore import Qt, QPointF

def sens_trigo(x):
    if x < 0:
        return (2*np.pi + x)
    else:
        return x

def current_case(x_h, y_h):
    '''
    Retourne la place (i,j) qu'occupe la ressource sur lequel est le point (x_h, y_h) dans la carte.
    Il suffit de diviser les coordonnées (x_h,y_h) par la longueur ou la largeur du carré qu'occupe la ressource sur la carte.
    '''
    return (int(y_h//constantes.carre_res[1]), int(x_h//constantes.carre_res[0]))

def collision_vision_cases(alpha, heading, rayon, carte, current_case, head):
    cases_vues = []
    overflow = False

    (k,l) = (current_case[0], current_case[1])

    nb_cases = rayon//constantes.carre_res[0]

    #détermination des sommets du carré entourant l'animal
    borders = []
    borders.append((max(k-nb_cases, 0),min(l+nb_cases, constantes.nb_carres_largeur-1)))#sommet (1,1)
    borders.append((max(k-nb_cases, 0),max(l-nb_cases, 0)))#sommet (-1,1)
    borders.append((min(k+nb_cases, constantes.nb_carres_hauteur-1),max(l-nb_cases, 0)))#sommet (-1,-1)

    #on parcourt toutes les cases du carré et on détermine si elles sont dans le champ de vision
    for i in range(borders[1][0], borders[2][0]+1):
        for j in range(borders[1][1], borders[0][1]+1):
            (x,y) = ((j+1/2)*constantes.carre_res[0], (i+1/2)*constantes.carre_res[0])

            if(np.sqrt((head.x()-x)**2 + (head.y()-y)**2) <= rayon):
                angle = sens_trigo(atan2(y-head.y(), x-head.x()))
                first_angle = sens_trigo(heading*np.pi/180 - alpha)
                sec_angle = np.mod(first_angle + 2*alpha, 2*np.pi)

                if((first_angle + 2*alpha) >= 2*np.pi):
                    overflow = True

                if (overflow and (angle > first_angle or angle < sec_angle)) or (angle > first_angle and angle < sec_angle):
                    cases_vues.append(carte[i][j])

    return cases_vues

def collision_vision_animaux(eco, espece, index):
    animaux_vus = []
    overflow = False

    animal_ref = eco[espece][index]
    head = animal_ref.poly.shape.at(0)
    head.setY(-head.y()+constantes.carre_res[1]*constantes.nb_carres_hauteur)
    alpha = animal_ref.vision.angle

    for key_espece in eco:
        for i in range(len(eco[key_espece])):
            animal = eco[key_espece][i]
            if key_espece != espece or i != index:
                center = animal.poly.get_center()
                center.setY(-center.y()+constantes.carre_res[1]*constantes.nb_carres_hauteur)

                if (np.sqrt((head.x()-center.x())**2 + (head.y()-center.y())**2) <= animal_ref.vision.rayon):
                    angle = sens_trigo(atan2(center.y()-head.y(), center.x()-head.x()))
                    first_angle = sens_trigo(animal_ref.poly.heading*np.pi/180 - alpha)
                    sec_angle = np.mod(first_angle + 2*alpha, 2*np.pi)

                    if((first_angle + 2*alpha) >= 2*np.pi):
                        overflow = True

                    if (overflow and (angle > first_angle or angle < sec_angle)) or (angle > first_angle and angle < sec_angle):
                        animaux_vus.append(animal)

    return animaux_vus

def check_borders(fig, size_x, size_y):
    '''
    Vérifie que le polygone ne sort pas de la carte
    '''
    for i in range(fig.nbp):
        pt = fig.shape.at(i)

        if pt.x() < 0 or pt.x() > size_x:
            return False

        if pt.y() < 0 or pt.y() > size_y:
            return False
    return True


def check_rect_coll(fig, ofig):
    '''
    Gestion des collisions simplifiée, en utilisant le rectangle qui entoure les polygones
    Prend en paramêtre:
    - le polygone que l'on souhaite déplacer fig
    - la liste de tous les autres polygones
    Retourne True si collision, False sinon
    '''
    frect = fig.shape.boundingRect()  # retourne le rectangle qui englobe le polygone
    orect = ofig.shape.boundingRect()

    if frect.left() > orect.right() or frect.right() < orect.left() or frect.top() > orect.bottom() or frect.bottom() < orect.top():
        return False
    else:
        return True

def intersectSegment(A, B, I, P):
    '''
    Vérifie s'il y a intersection entre les segments [AB] et [IP]
    Renvoie 0 si cas limite, 1 si intersection et 0 sinon
    '''
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
    '''
    Vérifie s'il y a collision entre deux polygones passés en paramêtre
    Renvoie True si collision, False sinon
    '''
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

def check_collisions(fig, key_espece, index, eco, scene):
    '''
    Check les collisions, d'abord par rectangle vu que c'est super rapide, puis si il y a collision
    on check avec la méthode par polygones
    Si il y a collision on retourne l'objet collisionné
    '''
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
