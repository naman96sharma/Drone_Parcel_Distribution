# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 09:47:32 2016

@author: nicolas & taha
"""
AREA=600
MARGE=100

TAILLE_POLICE=10;
POLICE="Arial 10"

EPSILON = 0.000001        

from tkinter import *
import numpy as np
import random

# calcule le carré de la distance entre 2 points
def carre_distance(point1,point2):
    return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2

def belongs(diagramme,point):
    return np.argmin([carre_distance(cellule[0],point) for cellule in diagramme])

def perp_bisector(point1,point2):
    milieu = ((point1[0]+point2[0])/2, (point1[1]+point2[1])/2)
    vecteur = ((point1[1]-point2[1]), (point2[0]-point1[0]))
    return (vecteur,milieu)
                
def intersection_segment(ligne,point1,point2):
    l1 = (ligne[1])
    l2 = (ligne[0][0] + ligne[1][0],ligne[0][1] + ligne[1][1])
    xdiff = (l1[0] - l2[0], point1[0] - point2[0])
    ydiff = (l1[1] - l2[1], point1[1] - point2[1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff,ydiff)

    if div==0:
        return None # pas d'intersection

    d = (det(l1,l2), det(point1,point2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    
    # appartenance au segment
    if min(point1[0], point2[0]) - EPSILON <= x <= max(point1[0], point2[0]) + EPSILON and \
       min(point1[1], point2[1]) - EPSILON <= y <= max(point1[1], point2[1]) + EPSILON :
        return (x, y)
     
    return None
    
# renvoie les coordonnées du point symétrique au point passé en paramètre (argument 2) 
# par rapport à l'axe défini par ligne (argument 1)
def symmetric_point(ligne,point):
    l1 = (ligne[1])
    l2 = (ligne[0][0] + ligne[1][0], ligne[0][1] + ligne[1][1])
    b = l2[0]-l1[0]
    a = l1[1]-l2[1]
    c = a*l1[0] + b*l1[1]
    d = carre_distance(l1,l2)
    e = a*point[0] + b*point[1]
    
    x = point[0] + 2*a*(c-e)/d
    y = point[1] + 2*b*(c-e)/d
    return (x,y)
        
# génère une liste de germes aléatoire
def generate_random_germs(N):
    l = []
    for i in range(N):
         x = random.randint(0,AREA)
         y = random.randint(0,AREA)
         l.append((x,y))
    l.sort(key=lambda germe: carre_distance((AREA/2,AREA/2),germe)) # optimisation nécessaire
    return l        
    
#########################
# Fonctions de debogage #
#########################

def point_dessine(point):
    return (MARGE+point[0],MARGE+AREA-point[1])
 
def dessine_point(canvas,point):
    canvas.create_text(point_dessine(point),text="x",fill="red")
  
def dessine_segment(canvas,point1,point2):
    canvas.create_line(point_dessine(point1), point_dessine(point2),fill="purple")
  
def dessine_ligne(canvas,ligne):
    (vecteur,point) = ligne
    if vecteur[0] == 0:
        p1 = (point[1],0)
        p2 = (point[1],AREA)
    else:
        p1 = (0, point[1]-(point[0]*vecteur[1]/vecteur[0]))
        p2 = (AREA, point[1]-((point[0]-AREA)*vecteur[1]/vecteur[0]))
    canvas.create_line(point_dessine(p1),point_dessine(p2),fill="purple")


