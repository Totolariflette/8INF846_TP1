from copy import deepcopy
from util import legal_moves,count_dust,get_dirty_room, legal_moves_dim, DIRECTIONS,STAY


class Agent_but:

    def __init__(self,initial_percept,algo,goal):
        self.seq = [] # sequence d'action prévus par l'agent
        self.sensor(initial_percept) # fonction prenant une copie de l'environnement en entrée et retournant l'etat interne de l'agent (input :env  output state)
        self.goal = goal # l'état qui correspond au but 
        
        self.algo = algo # alogorithme de recherche dans un arbre (input : problem : output : seq)
       
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
        

    def get_action(self):
        
        while len(self.seq) > 0:
            action = self.seq.pop(0)
            print(self.seq)
            print(self.state)
            return action
        
        self.search()
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
            else:
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
        if self.bstate["nb_dust"]>5 :
            posx,posy= self.bstate["pos"]
            self.bstate["grid"] = self.bstate["grid"][posx-1:posx+1][posy-1:posy+1]
            self.bstate["nb_dust"] = count_dust(self.bstate["grid"])

        
        while len(self.seq) > 0:
            action = self.seq.pop(0)
            print(self.seq)
            #print(self.state)
            return action
        
        self.search()
        return STAY
        
        


