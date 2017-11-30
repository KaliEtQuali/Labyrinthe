#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 21:53:26 2017

@author: kalenga
"""



class Noeud:
    def __init__(self, i, j):
        self.voisins = []
        self.frontier={"haut":True, "bas": True, "gauche":True, "droite":True}
        self.value = 0
        self.i = i
        self.j = j
        self.is_in = False
        self.is_visited = False
        
    def __repr__(self):
        return "Noeud {},{}".format(self.i, self.j) 
        
    def add_voisins(self, voisins):
        if len(voisins) != 0:
            for voisin in voisins:
                if self.voisins.count(voisin)==0:
                    self.voisins.append(voisin)
                
    def build_wall(self, direction):
        self.frontier[direction]=True
        
    def blow_wall_up(self, direction):
        self.frontier[direction]=False
        
    def set_is_in(self):
        self.is_in=True
        
    def set_visited(self):
        self.is_visited = True