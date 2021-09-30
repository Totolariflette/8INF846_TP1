from random import randint, random
from copy import deepcopy
from util import DIRECTIONS, STAY, count_dust
import PIL.Image
from PIL import ImageTk
from tkinter import *
import time


class Environment:
    def __init__(self, width, height, initial_value='p', p_dirt=0.25, p_jewel=0.01, pos_agt=(0, 0)):
        self.width = width
        self.height = height
        self.grid = [[initial_value for _ in range(width)] for _ in range(height)]
        self.p_jewel = p_jewel
        self.p_dirt = p_dirt
        self.agent = pos_agt

    def update(self):
        if random() < self.p_dirt:
            i = randint(0, self.height - 1)
            j = randint(0, self.width - 1)
            if self.grid[i][j] != 'j':
                self.grid[i][j] = 'd'
            else:
                self.grid[i][j] = 'b'
        if random() < self.p_jewel:
            i = randint(0, self.width - 1)
            j = randint(0, self.height - 1)
            if self.grid[i][j] != 'd':
                self.grid[i][j] = 'j'
            else:
                self.grid[i][j] = 'b'

    def agent_update(self, action):  # = effector
        if action in DIRECTIONS:
            self.agent = (self.agent[0] + action[0], self.agent[1] + action[1])

        if action == 'ASPI':
            self.grid[self.agent[0]][self.agent[1]] = 'p'

    def show(self, msg=''):
        for j in range(self.height):
            for i in range(self.width):
                # print(i,j,end="|")
                if self.grid[i][j] == 'p': p = ' '
                if self.grid[i][j] == 'd': p = '#'
                if self.grid[i][j] == 'j': p = '*'
                if self.grid[i][j] == 'b': p = '@'
                if j == self.agent[1] and i == self.agent[0]: p = '>'
                print('|' + p, end='')
            if j == 1: print("|   " + msg + "   " + str(self.agent), end="")
            if j == 3: print("|   " + str(count_dust(self.grid)), end="")

            print("|")

    def show_Graphique(self, msg=''):
            #--- Fenêtre Principale ---
        fenetre = Tk()
        fenetre.configure(bg='light blue')
        fenetre.title("IA_TP1")
        fenetre.resizable(0,0)

        #--- Chargement des images ---
        imgAgent= ImageTk.PhotoImage(PIL.Image.open("Agent.png")) 
        imgJewel = ImageTk.PhotoImage(PIL.Image.open("jewel.png")) 
        imgDust = ImageTk.PhotoImage(PIL.Image.open("dust.png")) 
        imgDustJewel = ImageTk.PhotoImage(PIL.Image.open("dust_jewel.png")) 
        #--- Variables de mise en forme ---
        largeur = imgJewel.width()
        hauteur = imgJewel.height()
        margeGauche, margeHaut = 20, 20
        nbrLigne, nbrColonne = 5, 5

        #--- Caneva principal ---
        caneva = Canvas(fenetre,bg='white',width=(2*margeGauche)+(nbrColonne*largeur),height=(2*margeHaut)+(nbrLigne*hauteur),relief='groove')
        caneva.grid(row=0,column=1)
        #--Affichage grille--
        for coordY_ligne in range(margeHaut,(nbrLigne*hauteur)+margeHaut+1,hauteur):
            if (coordY_ligne-margeHaut) % (nbrLigne*hauteur) == 0:
                epaisseur = 5
            else:
                epaisseur = 1
            
            caneva.create_line(margeGauche,coordY_ligne,(nbrColonne*largeur)+margeGauche,coordY_ligne,width=epaisseur)

        for coordX_colonne in range(margeGauche,(nbrColonne*largeur)+margeGauche+1,largeur):
            if (coordX_colonne-margeGauche) % (nbrColonne*largeur) == 0:
                epaisseur = 5
            else:
                epaisseur = 2
            
            caneva.create_line(coordX_colonne,margeHaut,coordX_colonne,(nbrLigne*hauteur)+margeHaut,width=epaisseur)
         #--Affichage icon--
        for j in range(self.height):
            for i in range(self.width):
                coordX = margeGauche+(i*largeur)
                coordY = margeHaut+(j*hauteur)
                if self.grid[i][j] == 'p': 
                    caneva.delete(fenetre,Image)
                if self.grid[i][j] == 'd': 
                    caneva.create_image(coordX,coordY,image=imgDust,anchor=NW) 
                if self.grid[i][j] == 'j': 
                     caneva.create_image(coordX,coordY,image=imgJewel,anchor=NW)
                if self.grid[i][j] == 'b': 
                     caneva.create_image(coordX,coordY,image=imgDustJewel,anchor=NW)
                if j == self.agent[1] and i == self.agent[0]: 
                    caneva.create_image(coordX,coordY,image=imgAgent,anchor=NW)
        fenetre.update()
        fenetre.after(3000,lambda:fenetre.destroy())
        fenetre.mainloop()  

    def get_grid(self):
        return deepcopy(self.grid.copy())
