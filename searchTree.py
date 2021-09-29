import util


def depth_first_search(start_state,is_goal,succesor_fct):
    # Les noeuds contienent l etat actuel et la liste des actions pour arriver a cet etat depuis le debut
    node = {"state": start_state, "path": []}
    # on stocke les etats deja visites pour ne pas y repasser
    visited_state = []
    # implementation du dfs avec une pile
    pile = util.Stack()
    pile.push(node)

    while not pile.isEmpty():
        node = pile.list[len(pile.list) - 1]  # on recupere le premier element sans le depiler
        visited_state.append(node["state"])  # on l'ajoute aux etats visites
        if is_goal(node["state"]):  # si l'etat est les but du probleme on arrete et on renvoie le chemin pour arriver a cet etat
            return node["path"]
        feuille = True
        for suc in succesor_fct(node["state"]):  # on parcours tous les successeur de l'etat actuel
            if not suc[0] in visited_state:  # si le successeur n'a pas deja ete visite
                newNode = {"state": suc[0], "path": node["path"] + [suc[1]]}  # on construit le noeud
                pile.push(newNode)  # on empile
                feuille = False
        if feuille:  # si le neoud n'as pas de successeur qui n'ont pas ete visite on le depile
            pile.pop()


def breadth_first_search(start_state,is_goal,succesor_fct):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    node = {"state": start_state, "path": []}  # noeud qui contient l'etat plus le chemin pour y acceder
    q = util.Queue()  # implementation avec une file
    q.push(node)
    seen_state = [start_state]

    while not q.isEmpty():
        node = q.pop()
        if is_goal(node["state"]):
            return node["path"]
        for suc in succesor_fct(node["state"]):
            if not suc[0] in seen_state:
                seen_state.append(suc[0])
                q.push({"state": suc[0], "path": node["path"] + [suc[1]]})


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    # On implemente A* avec une file de prorit e 
    #  3 methodes importante :
    #     -push(elmt,priorit e) insert un  element avec une priorit e associ e
    #     -pop(elmt) r ecup ere l' element avec la priorit e la plus faible 
    #     -update(elmt,priotit e) met a jours la priorit e d'un  el ement si s'element est deja dans la file avec une priorit e plus haute
    openList = util.PriorityQueue()
    closedList = list()

    # les noeuds corresponde aux  etats.
    state = problem.getStartState()
    #on cr e e un dictionnaire pour associer a chaque etat les information : 
    #  - dist : cout depuis le noeud initial
    #  - prio : la valeur de priorit e de l"etat dans la file
    #  - path : le chemin jusqu'a cet etat avec ce cout et cette priorit e
    nodeInfo=dict()
    nodeInfo[state] = {"dist":0,"prio":0,"path":[]}
    openList.push(state,0)#on place l'etat initial dans la file

    while not openList.isEmpty():
        state = openList.pop() #on r ecup ere l'etat avec la prio la plus basse
        cdist = nodeInfo[state]["dist"] #et les infos associ es
        cpath = nodeInfo[state]["path"]
        if (problem.isGoalState(state)): # si c'est la solution on renvoie le chemin 
            return cpath
        for suc in problem.getSuccessors(state):# pour tous les successeurs de l'etat courant:
            if not (suc[0] in closedList): #si on ne la pas deja parcouru ( dans closedlist)
                #on calcule la priorit e du successeur en fonction de sa distance et de l'heuristique
                g= cdist+suc[2]
                h=heuristic(suc[0],problem)
                p= h+g
                if nodeInfo.has_key(suc[0]) and nodeInfo[suc[0]]["prio"]<p : # si le noeud existe deja dans la file avec une priorit e inferieur
                    pass # on ne fait rien
                else : # sinon on place le noeud dans la file ( ou on le met a jour)
                    nodeInfo[suc[0]]= {"dist":g,"prio":p,"path":cpath+[suc[1]]}
                    openList.update(suc[0],p)
        closedList.append(state)#on place ensuite le noeud courant dans la liste des noeuds deja visit e
            
              