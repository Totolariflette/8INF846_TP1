from copy import deepcopy
from util import legal_moves,count_dust,get_dirty_room, DIRECTIONS,STAY


class Agent:

    def __init__(self):
        self.seq = []

    def get_action(self, state):
        pass


class Agent1(Agent):

    def __init__(self, initial_percept,algo):
        self.seq = []
       
        self.update_state(initial_percept)
        self.goal = lambda state : (state["nb_dust"]==0 and state["jewel_gobbed"]==0)
        self.init_problem()
        self.algo = algo
        self.search()

    def update_state(self, percept):  # = sensor
        self.state = {'grid': percept.get_grid(), 'pos': percept.agent, 'nb_dust': count_dust(percept.get_grid()),'jewel_gobbed':0}

    def init_problem(self) :
        self.problem = Problem_blind(deepcopy(self.state),self.goal)

    def search(self) :
        self.seq = self.algo(self.problem)
        #print(self.seq)
        


    def get_action(self,percept):
        
        if len(self.seq) == 0 :
            self.__init__(percept,self.algo)
            if len(self.seq) == 0 : self.seq.append(STAY)
        print(self.seq)
        print(self.state)
        action = self.seq.pop(0)

        return action



class Agent2(Agent):

    def __init__(self, initial_percept,algo,heuristic):
        self.seq = []
        self.update_state(initial_percept)
        self.goal = lambda state : (state["nb_dust"]==0 and state["jewel_gobbed"]==0)
        self.init_problem()
        self.algo = algo
        self.heuristic = heuristic
        self.search()

    def update_state(self, percept):  # = sensor
        self.state = {'grid': percept.get_grid(), 'pos': percept.agent, 'nb_dust': count_dust(percept.get_grid()),'jewel_gobbed':0}

    def init_problem(self) :
        self.problem = Problem_informed(deepcopy(self.state),self.goal)

    def search(self) :
        self.seq = self.algo(self.problem,self.heuristic)
        #print(self.seq)
        


    def get_action(self,percept):
        
        if len(self.seq) == 0 :
            self.__init__(percept,self.algo)
            if len(self.seq) == 0 : self.seq.append(STAY)
        print(self.seq)
        print(self.state)
        action = self.seq.pop(0)

        return action


class Problem:

    def is_goal(self, state):
        pass

    def get_succesor(self, state):
        pass

    def get_cost_seq(self, seq):
        pass


class Problem_blind(Problem):

    def __init__(self, state, goal):
        self.initial_state = state
        self.isGoalState = goal

    def get_start_state(self):
        return self.initial_state

    def get_successors(self, state):
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
                    




class Problem_informed(Problem):
    def __init__(self,state,goal):
        self.initial_state = state
        self.isGoalState = goal

    def get_start_state(self):
        return self.initial_state

    def  get_successors(self,state):
        succ = []
        for act in legal_moves(state["grid"],state["pos"]):
            n_state = dict()
            n_state["grid"]=deepcopy(state["grid"])
            n_state["dirty_room"]=deepcopy(state["dirty_room"])
            n_state["pos"]=(state["pos"][0],state["pos"][1])
            cost = 1
            if act == STAY : act = 0
            if act in DIRECTIONS :
                n_state["pos"]=(state["pos"][0]+act[0],state["pos"][1]+act[1])
            else :
                if act == "ASPI":
                    
                    n_state["grid"][n_state["pos"][0]][n_state["pos"][1]] = 'p'
                    if state["grid"][n_state["pos"][0]][n_state["pos"][1]] =='d':
                        n_state["dirty_room"].remove(n_state["pos"])
            succ.append((n_state,act,cost))
        return succ


        

