#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 21:33:45 2017

@author: kalenga
"""

import matplotlib.pyplot as plt
import numpy as np
from noeud import Noeud
import random


def draw_wall(j, i, direction):
    if direction=="haut":
        plt.plot([i,i+1], [j,j], color='k', linewidth=1)
    if direction=="bas":
        plt.plot([i,i+1], [j+1,j+1], color='k', linewidth=1)
    if direction=="gauche":
        plt.plot([i,i], [j,j+1], color='k', linewidth=1)
    if direction=="droite":
        plt.plot([i+1,i+1], [j,j+1], color='k', linewidth=1)


def draw_borders(grid):
    for line in grid:
        for node in line:
            for direction, is_wall in node.frontier.items():
                if is_wall:
                    draw_wall(node.i, node.j, direction)
                    
            
    
def draw_way_out(chemin, grid):
    plt.gca().invert_yaxis()
    plt.gca().xaxis.set_ticks_position('top')
    draw_borders(grid)
    x=[]
    y=[]
    for node in chemin:
        #plt.plot([node.j+0.5],[node.i+0.5], marker='.', color='red', lw=1)
        x.append(node.j+0.5)
        y.append(node.i+0.5)
    plt.plot(x, y, marker='.', color='red', lw=1)
    plt.show()                    

                    
def create_link(node1, node2):
    node1.add_voisins([node2])
    node2.add_voisins([node1])
                
                
def prim_algorithm(grid, width, height, frontier, first):
    if len(frontier)==0:
        if first:
            #Je prends un node au hasard dans la grid
            i = random.randint(0,height-2)
            j = random.randint(0,width-2)
            first_node = grid[i][j]
            #Je rajoute le node dans le maze
            first_node.set_is_in()
            #Je prends les voisins de ce node
            first_node_frontier=[]
            if i != 0 :
                first_node_frontier.append(grid[i-1][j])
            if i != height-2 :
                first_node_frontier.append(grid[i+1][j])
            if j != 0 :
                first_node_frontier.append(grid[i][j-1])
            if j != width-2 :
                first_node_frontier.append(grid[i][j+1])
            #J'applique l'algo avec une frontière non vide cette fois-ci
            prim_algorithm(grid, width, height, first_node_frontier, False)
        else:
            print("labyrinthe construit")
    else:
        #Je prends un node au hasard dans la frontière
        n = len(frontier)
        l = random.randint(0,n-1)
        chosen_node = frontier[l]
        i = chosen_node.i
        j = chosen_node.j
        current_node = grid[i][j]
        #Je prends les voisins de ce node
        current_node_frontier=[]
        if i != 0 :
            current_node_frontier.append({"node":grid[i-1][j], "direction": "haut", "inverse_direction": "bas"})
        if i != height-2 :
            current_node_frontier.append({"node":grid[i+1][j], "direction": "bas", "inverse_direction": "haut"})
        if j != 0 :
            current_node_frontier.append({"node":grid[i][j-1], "direction": "gauche", "inverse_direction": "droite"})
        if j != width-2 :
            current_node_frontier.append({"node":grid[i][j+1], "direction": "droite", "inverse_direction": "gauche"})
        #Je prends les voisins appartenant déjà au maze
        current_node_in_frontier = []
        for node in current_node_frontier:
            if node["node"].is_in:
                current_node_in_frontier.append(node)
        #Je prends un node au hasard parmis les voisins qui sont dans le maze et je détruis le mur qui le sépare du node actuel
        n = len(current_node_in_frontier)
        if n != 0:
            selected_node = current_node_in_frontier[random.randint(0,n-1)]
            current_node.blow_wall_up(selected_node["direction"])
            selected_node["node"].blow_wall_up(selected_node["inverse_direction"])
            #Je crée une représentation en graphe
            create_link(current_node, selected_node["node"])
        #Je rajoute le node dans le maze
        current_node.set_is_in()
        #Je supprime le node de la frontière
        del frontier[l]
        #Je rajoute à la frontière les voisins n'appartenant pas encore au maze
        for node in current_node_frontier:
            if not node["node"].is_in and frontier.count(node["node"])==0:
                frontier.append(node["node"])
        prim_algorithm(grid, width, height, frontier, False)
        
        
        
def parcours_en_profondeur(grid, node, chemin):
    node.set_visited()
    if node.i==len(grid)-1 and node.j==len(grid[0])-1:
        return chemin
    else:
        for voisin in node.voisins:
            if not voisin.is_visited:
                chemin_bis = chemin[:]
                chemin_bis.append(voisin)
                resultat = parcours_en_profondeur(grid, voisin, chemin_bis)
                if resultat != None:
                    return resultat
                    break
        
        
def trouver_le_chemin(grid):
    chemin = [grid[0][0]]
    chemin_final = parcours_en_profondeur(grid, grid[0][0], chemin)
    return chemin_final
    

    


#Construction de la grille graphique
width=30
height=30
xvalues=[i for i in range(width)]
yvalues=[j for j in range(height)]
xx, yy = np.meshgrid(xvalues, yvalues)
plt.plot(xx, yy,  color='k', linestyle='none')
plt.gca().invert_yaxis()
plt.gca().xaxis.set_ticks_position('top')

#Construction de la grille en terme de noeud
rows=height-1
cols=width-1
grid=[[Noeud(i, j) for j in range(cols)] for i in range(rows)]

#Construction du labyrinthe, algorithme de Prim
prim_algorithm(grid, width, height, [], True)

#Update du labyrinthe dans la grille graphique
draw_borders(grid)

#ShowOff
plt.show()

#SolveOff
draw_way_out(trouver_le_chemin(grid), grid)




