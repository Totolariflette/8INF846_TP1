from random import randint, random
from copy import deepcopy
from util import DIRECTIONS,count_dust    


class Environment():
    def __init__(self,width,height,initial_value='p',p_dirt=0.25,p_jewel=0.01,pos_agt=(0,0)) :
        self.width = width
        self.height = height
        self.grid =[[initial_value for _ in range(width) ] for _ in  range(height)]
        self.p_jewel = p_jewel
        self.p_dirt = p_dirt
        self.agent = pos_agt

    def update(self):
        if random() < self.p_dirt:
            i=randint(0,self.height-1) 
            j=randint(0,self.width-1) 
            if self.grid[i][j] != 'j' : self.grid[i][j] = 'd' 
            else  : self.grid[i][j] = 'b'
        if random() < self.p_jewel:
            i= randint(0,self.width-1) 
            j=randint(0,self.height-1) 
            if self.grid[i][j] != 'd' : self.grid[i][j] = 'j' 
            else  : self.grid[i][j] = 'b'


    def agent_update(self,action):
        if action in DIRECTIONS :
            self.agent = (self.agent[0]+action[0],self.agent[1]+action[1])
            
        if action == 'ASPI':
            self.grid[self.agent[0]][self.agent[1]]='p'

        

    def show(self,msg):
        for j in range(self.height):
            for i in range(self.width):
                #print(i,j,end="|")
                if self.grid[i][j] =='p' : p =' '
                if self.grid[i][j] =='d' : p = '#'
                if self.grid[i][j] =='j' : p = '*'
                if self.grid[i][j] =='b' : p = '@'
                if j== self.agent[1] and i == self.agent[0] : p = '>'
                print('|'+p,end='')
            if j==1 : print("|   "+msg+"   " + str(self.agent),end="")
            if j==3 : print("|   "+str(count_dust(self.grid)),end="")
            

            print("|")
        

        
    def get_grid(self):
        return deepcopy(self.grid.copy())
