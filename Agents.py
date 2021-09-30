from copy import deepcopy
from util import legal_moves,count_dust,get_dirty_room, legal_moves_dim, get_jewel,DIRECTIONS,STAY


class Agent_but:

    def __init__(self,initial_percept,algo,goal):
        self.seq = [] # sequence d'action prévus par l'agent
        self.sensor(initial_percept) # fonction prenant une copie de l'environnement en entrée et retournant l'etat interne de l'agent (input :env  output state)
        self.goal = goal # l'état qui correspond au but 
        
        self.algo = algo # alogorithme de recherche dans un arbre (input : problem : output : seq)
        self.score = 0
        self.freq = 1 
        self.tour =0
        self.search()
    
    def is_goal(self,state):
        return all( state[k]==self.goal[k] for k in self.goal.keys)

    def sensor(self, percept): 
        self.bstate = {'grid': percept.get_grid(), 'pos': percept.agent}

    
    def get_succesor(self,state):
        pass
    
    def search(self) :
        self.seq = self.algo(self.bstate,self.is_goal,self.get_succesor)
        #print(self.seq)

    def learn(self,score):
        if self.score < score :
            self.freq +=1
        elif self.freq > 1:
            self.freq -= 1
        self.score = score

        

    def get_action(self):

        self.tour+=1
        if self.tour % self.freq == 0 :
            self.search()
        
        while len(self.seq) > 0:
            action = self.seq.pop(0)
            print(self.seq)
            print(self.state)
            return action
        
        return STAY



class Agent1(Agent_but):

    def __init__(self, initial_percept,algo):
        super().__init__(initial_percept,algo,goal={'nb_dust':0 ,'jewel_gobbed':0})
    
        

    def is_goal(self,state):
        return all([ state[k]==self.goal[k] for k in self.goal.keys()])

    def get_succesor(self,state):
        succ = []
        for act in legal_moves(state["grid"], state["pos"]):
            n_state = dict()
            n_state["grid"] = deepcopy(state["grid"])
            n_state["nb_dust"] = state["nb_dust"]
            n_state["pos"] = (state["pos"][0], state["pos"][1])
            n_state["jewel_gobbed"] = state["jewel_gobbed"]
            if act in DIRECTIONS:
                n_state["pos"] = (state["pos"][0] + act[0], state["pos"][1] + act[1])
            elif n_state["grid"][n_state["pos"][0]][n_state["pos"][1]] != 'p' :
                if act == "ASPI":
                    n_state["grid"][n_state["pos"][0]][n_state["pos"][1]] = 'p'
                    if state["grid"][n_state["pos"][0]][n_state["pos"][1]] == 'd':
                        n_state['nb_dust'] -= 1
                    if state["grid"][n_state["pos"][0]][n_state["pos"][1]] == 'j' :
                        n_state["jewel_gobbed"] +=1
                    if state["grid"][n_state["pos"][0]][n_state["pos"][1]] == 'b' :
                        n_state['nb_dust'] -= 1
                        n_state["jewel_gobbed"] +=1
                if act =="RAM":
                    if state["grid"][n_state["pos"][0]][n_state["pos"][1]] == 'j' :
                        n_state["grid"][n_state["pos"][0]][n_state["pos"][1]] = 'p'
                    if state["grid"][n_state["pos"][0]][n_state["pos"][1]] == 'b' :
                        n_state["grid"][n_state["pos"][0]][n_state["pos"][1]] = 'd'
                
            succ.append((n_state, act))
        return succ

    def sensor(self, percept): 
        self.bstate = {'grid': percept.get_grid(), 'pos': percept.agent, 'nb_dust': count_dust(percept.get_grid()),'jewel_gobbed':0}

  


    def get_action(self):

        if self.bstate["nb_dust"]<=3:
            self.search()
        
        
        while len(self.seq) > 0:
            action = self.seq.pop(0)
            print(self.seq)
            #print(self.state)
            return action
        
        self.search()
        return STAY
        
        

class Agent2(Agent_but):

    def __init__(self, initial_percept,algo):
        super().__init__(initial_percept,algo,goal={'nb_dust':0 ,'jewel_gobbed':0})
    
        

    def is_goal(self,state):
        return all([ state[k]==self.goal[k] for k in self.goal.keys()])

    def get_succesor(self,state):
        succ = []
        for act in legal_moves(state["grid"], state["pos"]):
            n_state = dict()
            n_state["grid"] = deepcopy(state["grid"])
            n_state["nb_dust"] = state["nb_dust"]
            n_state["pos"] = (state["pos"][0], state["pos"][1])
            n_state["jewel_gobbed"] = state["jewel_gobbed"]
            cost = 0
            if act in DIRECTIONS:
                cost = 1
                n_state["pos"] = (state["pos"][0] + act[0], state["pos"][1] + act[1])
            elif n_state["grid"][n_state["pos"][0]][n_state["pos"][1]] != 'p' :
                if act == "ASPI":
                    cost = 1
                    n_state["grid"][n_state["pos"][0]][n_state["pos"][1]] = 'p'
                    if state["grid"][n_state["pos"][0]][n_state["pos"][1]] == 'd':
                        n_state['nb_dust'] -= 1
                    if state["grid"][n_state["pos"][0]][n_state["pos"][1]] == 'j' :
                        n_state["jewel_gobbed"] +=1
                        cost += 50
                    if state["grid"][n_state["pos"][0]][n_state["pos"][1]] == 'b' :
                        n_state['nb_dust'] -= 1
                        n_state["jewel_gobbed"] +=1
                        cost += 50
                if act =="RAM":
                    cost = 1
                    if state["grid"][n_state["pos"][0]][n_state["pos"][1]] == 'j' :
                        n_state["grid"][n_state["pos"][0]][n_state["pos"][1]] = 'p'
                    if state["grid"][n_state["pos"][0]][n_state["pos"][1]] == 'b' :
                        n_state["grid"][n_state["pos"][0]][n_state["pos"][1]] = 'd'
            else: continue
            succ.append((n_state, act, cost))
        return succ

    def sensor(self, percept): 
        self.bstate = {'grid': percept.get_grid(), 'pos': percept.agent, 'nb_dust': count_dust(percept.get_grid()),'jewel_gobbed':0}

    def search(self) :
        self.seq = self.algo(self.bstate,self.is_goal,self.get_succesor,Heuristic_moins_nulle)
        #print(self.seq)
  


    def get_action(self):
        
        while len(self.seq) > 0:
            action = self.seq.pop(0)
            print(self.seq)
            #print(self.state)
            return action
        
        self.search()
        return STAY
        


def Heuristic_nulle(state):
    
    return state["nb_dust"]


def Heuristic_moins_nulle(state):
    posx,posy = state["pos"]
    if state["grid"][posx][posy] == 'd':
        h=0
    else : h=1 
    h+=state["nb_dust"]**2
    return h























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