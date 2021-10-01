from src.util import DIRECTIONS, legal_moves


def nullHeuristic(state):
    return 0


def heuristic1(state):
    
    return state[3]


def heuristic2(state):
    posx,posy = state[1]
    if state[0][posx][posy] == 'd':
        h=0
    else : h=1 
    h+=state[2]**2
    return h

def heuristic3(state):
    posx,posy = state[1]
    h=0
    for act in legal_moves(state[0],state[1]):
        if act in DIRECTIONS:
            if state[0][posx+act[0]]+ state[0][posy+act[1]] == 'd' :
                h+=1
            if state[0][posx]+ state[0][posy]=='d':
                h+=1

    h/=1 # plus il y a de case sales autours plus une case est interessante
    h+=state[2]**2 # une grille avec moins de poussière est toujours plus interessante
    h+=state[3]*100 #Aspirer un bijoux est très grave
    return h
