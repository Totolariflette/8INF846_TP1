import util


def depth_first_search(problem):
    # Les noeuds contienent l etat actuel et la liste des actions pour arriver a cet etat depuis le debut
    node = {"state": problem.get_start_state(), "path": []}
    # on stocke les etats deja visites pour ne pas y repasser
    visited_state = []
    # implementation du dfs avec une pile
    pile = util.Stack()
    pile.push(node)

    while not pile.isEmpty():
        node = pile.list[len(pile.list) - 1]  # on recupere le premier element sans le depiler
        visited_state.append(node["state"])  # on l'ajoute aux etats visites
        if problem.isGoalState(node[
                                   "state"]):  # si l'etat est les but du probleme on arrete et on renvoie le chemin pour arriver a cet etat
            return node["path"]
        feuille = True
        for suc in problem.get_successors(node["state"]):  # on parcours tous les successeur de l'etat actuel
            if not suc[0] in visited_state:  # si le successeur n'a pas deja ete visite
                newNode = {"state": suc[0], "path": node["path"] + [suc[1]]}  # on construit le noeud
                pile.push(newNode)  # on empile
                feuille = False
        if feuille:  # si le neoud n'as pas de successeur qui n'ont pas ete visite on le depile
            pile.pop()


def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    node = {"state": problem.get_start_state(), "path": []}  # noeud qui contient l'etat plus le chemin pour y acceder
    q = util.Queue()  # implementation avec une file
    q.push(node)
    seen_state = [problem.get_start_state()]

    while not q.isEmpty():
        node = q.pop()
        if problem.isGoalState(node["state"]):
            return node["path"]
        for suc in problem.get_successors(node["state"]):
            if not suc[0] in seen_state:
                seen_state.append(suc[0])
                q.push({"state": suc[0], "path": node["path"] + [suc[1]]})
