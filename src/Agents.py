from copy import deepcopy
from src.util import legal_moves,count_dust,get_dirty_room, legal_moves_dim, get_jewel,DIRECTIONS,STAY


class Agent_but:
    """ 
    Classe générale pour un Agent basé sur le but, on etendra cette classe en fonction de si l'agent utilise un algo informé,non informé, apprend...
    """

    def __init__(self,initial_percept,algo,apprenant):
       

        self.bstate = (None,None,0) # L'etat interne de l'agent: un tuple contenant : Une copie de la grille, la position de l'agent, le nombre de salles sales,le nombre de bijoux aspirés)
        self.sensor(initial_percept) # fonction prenant une copie de l'environnement en entrée et qui met à jours l'etat interne de l'agent (input :env  output state)
        
        self.seq = [] # sequence d'action prévus par l'agent (intentions)
        self.algo = algo # alogorithme de recherche dans un arbre (input : problem : output : seq)

        self.apprenant =apprenant

        self.score = 0
        self.periode = 10 
        self.tour =0
        self.limit = 5
        #self.search()
    
    def is_goal(self,state):
        """" Fonction prenant en entrée un etat et renvoyant vrai si l'etat est bien le but """
        return (state[2]==0 and state[3]==0) # On a atteint le but si toutes les salles sont propres et qu'aucun bijoux n'a été aspiré

    def sensor(self, percept): 
        grid = percept.get_grid()
        self.bstate = (grid, percept.agent, count_dust(grid),0)

    
    def get_succesor(self,state): 
        """ Fonction retournant tous les prochains etats possible sous forme de tuples contenants : 
            1 -l'etat futur, 
            2-L'action pour se rendre dans cet etat
            (3- seulement pour algo informé) Le cout pour se rendre dans ce nouvel etat
        input : etat
        output : liste de tuples 

        à implementer dans les sous classe en fonction de l'algo et de la représentation des etats
        """
        pass
    
    def search(self) :
        """Exploration l'agent execute l'algorithme d'exploration qui contruit l'arbre au fur à mesure de son exploration en fonction de l'algo choisit """
        if self.bstate[2] > self.limit:
            self.limit_search()
        else:
            self.seq = self.algo(self.bstate,self.is_goal,self.get_succesor)
        #print(self.seq)

    def learn(self,score):
        if self.score < score :
            self.periode+=1
        elif self.periode > 1:
            self.periode -= 1
        self.score = score

    def is_goal_limited(self,state):
        """" Fonction prenant en entrée un etat et renvoyant vrai si l'etat est bien le but """
        return (state[2]==self.bstate[2]-self.limit and state[3]==0) # On a atteint le but si toutes les salles sont propres et qu'aucun bijoux n'a été aspiré


    def limit_search(self):
        self.seq = self.algo(self.bstate,self.is_goal_limited,self.get_succesor)

        

    def get_action(self):
        """
        Retourne la prochaine action de l'agent
        """
        self.tour+=1
        while len(self.seq) > 0:
            if self.apprenant and self.tour%self.periode == 0:
                self.search()
            action = self.seq.pop(0)
            return action

        
        self.search()
        
        return STAY



class Agent_aveugle(Agent_but):

    def __init__(self,initial_percept,algo,apprenant):
       super().__init__(initial_percept,algo,apprenant)
       self.limit = 3
    

    def get_succesor(self,state):
        succ = []
        for act in legal_moves(state[0], state[1]): # un nouvel etat pour chaque action possibles ( deplacement dans chaque direction + asp + ram)
            
            n_grid = deepcopy(state[0])
            n_nb_dust = state[2]
            n_pos_x,n_pos_y = state[1]
            n_pos = (n_pos_x,n_pos_y)
            n_jewel_gobbed = state[3]

            case =  n_grid[n_pos_x][n_pos_y]  

            if act in DIRECTIONS: # Soit le robot ce deplace on met à jour la position
                n_pos = (n_pos_x + act[0], n_pos_y + act[1])
            elif case not in 'pj' : # On ne considère pas les cas ou le robot aspire ou rammasse alors qu'il est sur une case vide ou un bijou, cela permet d'avoir moins de branches inutiles a explorer
                if act == "ASPI":  # Soit il aspire, on met à jour l'etat 
                    n_grid[n_pos[0]][n_pos[1]] = 'p'
                    if case == 'd':
                        n_nb_dust -= 1
                    if case == 'b' :
                        n_nb_dust -= 1
                        n_jewel_gobbed +=1
                if act =="RAM": # soit il rammasse, on met à jour l'etat 
                    if case == 'j' :
                        n_grid[n_pos[0]][n_pos[1]] = 'p'
                    if case == 'b' :
                        n_grid[n_pos[0]][n_pos[1]] = 'd'
            n_state=(n_grid,n_pos,n_nb_dust,n_jewel_gobbed) 
            succ.append((n_state, act))
        return succ


    

        
        

class Agent_informe(Agent_but):

    def __init__(self, initial_percept,algo,apprenant,heuristique):
        super().__init__(initial_percept,algo,apprenant)
        self.heuristique = heuristique
    
    

    def get_succesor(self,state):
        succ = []
        for act in legal_moves(state[0], state[1]): # un nouvel etat pour chaque action possibles ( deplacement dans chaque direction + asp + ram)
            
            n_grid = deepcopy(state[0])
            n_nb_dust = state[2]
            n_pos_x,n_pos_y = state[1]
            n_pos = (n_pos_x,n_pos_y)
            n_jewel_gobbed = state[3]

            case =  n_grid[n_pos_x][n_pos_y]  

            cost = 0 

            if act in DIRECTIONS: # Soit le robot ce deplace on met à jour la position
                n_pos = (n_pos_x + act[0], n_pos_y + act[1])
                cost=1
            elif case not in 'pj' : # On ne considère pas les cas ou le robot aspire ou rammasse alors qu'il est sur une case vide ou un bijou, cela permet d'avoir moins de branches inutiles a explorer
                if act == "ASPI":  # Soit il aspire, on met à jour l'etat 
                    cost=1
                    n_grid[n_pos[0]][n_pos[1]] = 'p'
                    if case == 'd':
                        n_nb_dust -= 1
                    if case == 'b' :
                        n_nb_dust -= 1
                        n_jewel_gobbed +=1
                        cost += 50
                if act =="RAM": # soit il rammasse, on met à jour l'etat 
                    cost +=1
                    if case == 'j' :
                        n_grid[n_pos[0]][n_pos[1]] = 'p'
                    if case == 'b' :
                        n_grid[n_pos[0]][n_pos[1]] = 'd'
            n_state=(n_grid,n_pos,n_nb_dust,n_jewel_gobbed) 
            succ.append((n_state, act,cost))
        return succ    

   
    def search(self) :
        self.seq = self.algo(self.bstate,self.is_goal,self.get_succesor,self.heuristique)


    def limit_search(self):
        self.seq = self.algo(self.bstate,self.is_goal_limited,self.get_succesor,self.heuristique)

        
  

        

























# class Agent2(Agent_but):

#     def __init__(self, initial_percept,algo):
#         super().__init__(initial_percept,algo,goal={'d_room':[ ] ,'jewel_gobbed':0})
#         self.dim = (len(initial_percept.grid),len(initial_percept.grid[0]))
    
        

#     def is_goal(self,state):
#         return all([ state[k]==self.goal[k] for k in self.goal.keys()])

#     def get_succesor(self,state):
#         succ = []
#         for act in legal_moves_dim(self.dim, state["pos"]):
#             n_state = dict()
#             n_state["d_room"] = state["d_room"]
#             n_state["j_room"] = state["j_room"]
#             n_state["pos"] = (state["pos"][0], state["pos"][1])
#             n_state["jewel_gobbed"] = state["jewel_gobbed"]
#             pos = state["pos"]
#             if act in DIRECTIONS:
#                 pos = (pos[0] + act[0], pos[1] + act[1])
#                 n_state["pos"] = pos
#             elif pos in state["d_room"] or pos in state["j_room"]:
#                 if act == "ASPI":
#                     if pos in n_state["d_room"] :
#                         n_state["d_room"].remove(pos)
#                     if pos in n_state["j_room"] :
#                         n_state["jewel_gobbed"] +=1
#                         n_state["j_room"].remove(pos)
#                 if act =="RAM":
#                     if pos in n_state["j_room"] :
#                         n_state["j_room"].remove(pos)
                    
#             succ.append((n_state, act))
#         return succ

#     def sensor(self, percept): 
#         self.bstate = { 'pos': percept.agent, 'd_room': get_dirty_room(percept.get_grid()),'j_room':get_jewel(percept.get_grid()),'jewel_gobbed':0}

  


#     def get_action(self):

        
        
        
#         print(self.bstate)
#         while len(self.seq) > 0:
#             action = self.seq.pop(0)
#             print(self.seq)
#             #print(self.state)
#             return action
#         self.search()
        
#         return STAY