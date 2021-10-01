from random import randint, random
from copy import deepcopy
from src.util import DIRECTIONS, STAY, count_dust
import PIL.Image
from PIL import ImageTk
from tkinter import *
import time

class Environment:
    """Classe Environnement"""

    def __init__(self, width, height, initial_value='p', p_dust=0.25, p_jewel=0.01, pos_agt=(0, 0)):
        self.width = width
        self.height = height
        self.grid = [[initial_value for _ in range(width)] for _ in range(height)]
        self.p_jewel = p_jewel
        self.p_dust = p_dust
        self.agent = pos_agt
        self.compteurs = {"nb_dust":0,"nb_jewel":0,"dust_aspi":0,'jewel_aspi':0,"jewel_saved":0,"cost":0}
        self.compteurs_save = deepcopy(self.compteurs)
        self.score = 0
        self.tour = 0

    def update(self):
        self.tour +=1
        if random() < self.p_dust:
            i = randint(0, self.height - 1)
            j = randint(0, self.width - 1)
            if self.grid[i][j] not in "jbd":
                self.grid[i][j] = 'd'
                self.compteurs["nb_dust"]+=1
            elif self.grid[i][j]  in "j":
                self.grid[i][j] = 'b'
                self.compteurs["nb_dust"]+=1
        if random() < self.p_jewel:
            i = randint(0, self.width - 1)
            j = randint(0, self.height - 1)
            if self.grid[i][j] not in "dbj" :
                self.grid[i][j] = 'j'
                self.compteurs["nb_jewel"]+=1
            elif self.grid[i][j]  in "d":
                self.grid[i][j] = 'b'
                self.compteurs["nb_jewel"]+=1

    def agent_update(self, action):  # = effector
        if action != STAY :
            self.compteurs["cost"]+=1
        if action in DIRECTIONS:
            self.agent = (self.agent[0] + action[0], self.agent[1] + action[1])

        
        if action == 'ASPI':
            if self.grid[self.agent[0]][self.agent[1]] == 'd' : 
                self.compteurs["dust_aspi"]+=1
                #self.compteurs["nb_dust"]-=1
            if self.grid[self.agent[0]][self.agent[1]] == 'j' :
                self.compteurs["jewel_aspi"]+=1
                #self.compteurs["nb_jewel"]-=1
            self.grid[self.agent[0]][self.agent[1]] = 'p'

        if action == 'RAM':
            if self.grid[self.agent[0]][self.agent[1]] in 'bj' : self.compteurs["jewel_saved"]+=1
            if self.grid[self.agent[0]][self.agent[1]]  == 'b':
                self.grid[self.agent[0]][self.agent[1]] = 'd'
            else :  
                self.grid[self.agent[0]][self.agent[1]] = 'p'


    def get_score(self):
        
        # mes = dict()
        # for k in self.compteurs.keys():
        #     mes[k] = self.compteurs[k]-self.compteurs_save[k]

        
        # score_dust = mes["dust_aspi"]/mes["nb_dust"] if mes["nb_dust"] !=0 else 0
        # score_jewel = mes["jewel_saved"]/mes["nb_jewel"] if mes["nb_jewel"] !=0 else 0
        # score_cost = 1/mes["cost"] if mes["cost"]!=0 else 10
        # self.score = score_dust+ score_jewel + score_cost - 10*mes["jewel_aspi"]


        # self.compteurs_save = deepcopy(self.compteurs)
        if self.compteurs['cost'] == 0 : self.score =0
        else :
            self.score = -self.compteurs["jewel_aspi"]+self.compteurs["dust_aspi"]/self.compteurs['cost']
        

        return self.score
        


    def show(self,msg=''):
        for j in range(self.height):
            for i in range(self.width):
                # print(i,j,end="|")
                if self.grid[i][j] == 'p': p = ' '
                if self.grid[i][j] == 'd': p = '#'
                if self.grid[i][j] == 'j': p = '*'
                if self.grid[i][j] == 'b': p = '@'
                if j == self.agent[1] and i == self.agent[0]: p = '>'
                print('|' + p, end='')
            if j == 0: print("|   " + msg + "   " + str(self.agent), end="")
            if j == 2: print("|   " + str(self.compteurs), end="")
            if j == 4: print("|   " + str(self.get_score()), end="")

            print("|")
    

    def init_graphique(self):
        self.fenetre = Tk()
        self.fenetre.configure(bg='light blue')
        self.fenetre.title("IA_TP1")
        self.fenetre.resizable(0,0)
        #--- Chargement des images ---
        self.imgAgent= ImageTk.PhotoImage(PIL.Image.open("images/Agent.png")) 
        self.imgJewel = ImageTk.PhotoImage(PIL.Image.open("images/jewel.png")) 
        self.imgDust = ImageTk.PhotoImage(PIL.Image.open("images/dust.png")) 
        self.imgDustJewel= ImageTk.PhotoImage(PIL.Image.open("images/dust_jewel.png")) 
         #--- Variables de mise en forme ---
        self.largeur = self.imgJewel.width()
        self.hauteur = self.imgJewel.height()
        self.margeGauche, self.margeHaut = 20, 20
        self.nbrLigne, self.nbrColonne = 5, 5

    def show_graphique(self):
        
        #--- Caneva principal ---
        caneva = Canvas(self.fenetre,bg='white',width=(2*self.margeGauche)+(self.nbrColonne*self.largeur),height=(2*self.margeHaut)+(self.nbrLigne*self.hauteur),relief='groove')
        caneva.grid(row=0,column=1)
        #--Affichage grille--
        for coordY_ligne in range(self.margeHaut,(self.nbrLigne*self.hauteur)+self.margeHaut+1,self.hauteur):
            if (coordY_ligne-self.margeHaut) % (self.nbrLigne*self.hauteur) == 0:
                epaisseur = 5
            else:
                epaisseur = 1
            
            caneva.create_line(self.margeGauche,coordY_ligne,(self.nbrColonne*self.largeur)+self.margeGauche,coordY_ligne,width=epaisseur)

        for coordX_colonne in range(self.margeGauche,(self.nbrColonne*self.largeur)+self.margeGauche+1,self.largeur):
            if (coordX_colonne-self.margeGauche) % (self.nbrColonne*self.largeur) == 0:
                epaisseur = 5
            else:
                epaisseur = 2
            
            caneva.create_line(coordX_colonne,self.margeHaut,coordX_colonne,(self.nbrLigne*self.hauteur)+self.margeHaut,width=epaisseur)
         #--Affichage icon--
        for j in range(self.height):
            for i in range(self.width):
                coordX = self.margeGauche+(i*self.largeur)
                coordY = self.margeHaut+(j*self.hauteur)
                if self.grid[i][j] == 'p': 
                    caneva.delete(self.fenetre,Image)
                if self.grid[i][j] == 'd': 
                    caneva.create_image(coordX,coordY,image=self.imgDust,anchor=NW) 
                if self.grid[i][j] == 'j': 
                     caneva.create_image(coordX,coordY,image=self.imgJewel,anchor=NW)
                if self.grid[i][j] == 'b': 
                     caneva.create_image(coordX,coordY,image=self.imgDustJewel,anchor=NW)
                if j == self.agent[1] and i == self.agent[0]: 
                    caneva.create_image(coordX,coordY,image=self.imgAgent,anchor=NW)
        self.fenetre.update()
        #self.fenetre.after(3000,lambda:self.fenetre.destroy())
        #self.fenetre.mainloop()  

    def get_grid(self):
        return deepcopy(self.grid.copy())
