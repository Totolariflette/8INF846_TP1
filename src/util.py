"""
Quelques fonctions utiles pour l'agent + implementation des piles, files et files de prioritées utilisés dans les algorithme de recherche.

Implémentation des Piles files et files de priorité par John DeNero (denero@cs.berkeley.edu) pour l'université de  Berkeley, http://ai.berkeley.edu (The Pacman AI projects)
"""

import heapq


HAUT = (0,-1)
BAS = (0,1)
GAUCHE = (1,0)
DROITE = (-1,0)
STAY =(0,0)

DIRECTIONS = {HAUT,BAS,GAUCHE,DROITE,STAY}


def count_dust(grid):
    c=0
    for ligne in grid :
        for case in ligne:
            if case == 'd' or case =='b' : c+=1
    return c

def get_dirty_room(grid):
    c=[]
    for i,ligne in enumerate(grid) :
        for j,case in enumerate(ligne):
            if case in 'db' : c.append((i,j))
    return c

def get_jewel(grid):
    c=[]
    for i,ligne in enumerate(grid) :
        for j,case in enumerate(ligne):
            if case == 'jb' : c.append((i,j))
    return c


def legal_moves(grid,pos):
    moves = {'ASPI','RAM'}
    for d in DIRECTIONS:
        if 0<=pos[0]+d[0]<len(grid) and 0<=pos[1]+d[1]<len(grid[0]) :
            moves.add(d)
    return moves
    
def legal_moves_dim(dim,pos):
    moves = {'ASPI','RAM'}
    for d in DIRECTIONS:
        if 0<=pos[0]+d[0]<dim[0] and 0<=pos[1]+d[1]<dim[1] :
            moves.add(d)
    return moves

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)