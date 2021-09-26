from copy import deepcopy
from util import legal_moves,count_dust,DIRECTIONS,STAY

class Agent():

    def __init__(self) :
        self.seq=[]


    def getAction(self,state):
        pass
        
        
        
class Agent_1(Agent):

    def __init__(self,initial_percept,algo):
        self.seq=[]
        self.update_state(initial_percept)
        self.goal = lambda state : state["nb_dust"]==0
        self.init_problem(self.state,self.goal)
        self.algo = algo
        self.search()

        

    def update_state(self,percept):
        self.state={'grid':percept.get_grid(),'pos':percept.agent,'nb_dust':count_dust(percept.get_grid())}


    def init_problem(self,state,goal) :
        self.problem = Problem_1(deepcopy(self.state),goal)

    def search(self) :
        self.seq = self.algo(self.problem)
        #print(self.seq)
        



    def getAction(self,percept):
        
        if len(self.seq) == 0 :
            self.__init__(percept,self.algo)
            if len(self.seq) == 0 : self.seq.append(STAY)
        print(self.seq)
        action = self.seq.pop(0)
        
        return action
        





class Problem():

    def is_goal(self,state):
        pass

    def get_succesor(self,state):
        pass

    def get_cost_seq(self,seq):
        pass


class Problem_1(Problem):

    def __init__(self,state,goal):
        self.initial_state = state
        self.isGoalState = goal

    def getStartState(self):
        return self.initial_state

    def  getSuccessors(self,state):
        succ = []
        for act in legal_moves(state["grid"],state["pos"]):
            n_state = dict()
            n_state["grid"]=deepcopy(state["grid"])
            n_state["nb_dust"]=state["nb_dust"]
            n_state["pos"]=(state["pos"][0],state["pos"][1])
            if act in DIRECTIONS :
                n_state["pos"]=(state["pos"][0]+act[0],state["pos"][1]+act[1])
            else :
                if act == "ASPI":
                    
                    n_state["grid"][n_state["pos"][0]][n_state["pos"][1]] = 'p'
                    if state["grid"][n_state["pos"][0]][n_state["pos"][1]] =='d':
                        n_state['nb_dust'] -=1
            succ.append((n_state,act))
        return succ
                    
       