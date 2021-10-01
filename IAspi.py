import threading
from time import sleep
import os,sys,getopt


from src.Agents import Agent_aveugle, Agent_informe
from src.Environment import Environment
from src.searchTree import depth_first_search , breadth_first_search ,aStarSearch
from src.heuristiques import nullHeuristic,heuristic1,heuristic2,heuristic3

clear = lambda: os.system('cls') # fonction pour reinitialiser l'affichage du terminal




def env_loop(env,GRAPHIQUE):
    if GRAPHIQUE :
        env.init_graphique()
  
    try:
        while True:
            clear()
            env.update()
            env.show()
            if GRAPHIQUE :
                env.show_graphique()
            sleep(0.25)
    except KeyboardInterrupt :
        pass 


def agent_loop(agent, env,freq_learn):
   
    c=1
    try:
        while True:
            agent.sensor(env)
            action = agent.get_action()
            env.agent_update(action)
            if freq_learn and c%freq_learn==0 :
                agent.learn(env.get_score())
            c+=1
            sleep(0.25)
    except KeyboardInterrupt :
        pass 




help ="Usage : Game.py [OPTIONS]\n\
    liste des options :\n\
        -A algorithme d'exploration d'arbre au choix parmis BFS(Breadth First Search), DFS(Depth First Search) A(Astar) , par défaut A\n\
        -H heuristique pour A* 0,1,2,3 au choix\n\
        -f fréquence d'apprentissage : nombre d'iteration avant que l'agent mette à jour sa fréquence d'exploration(par defaut non apprennant)\n\
        -s taille de la grille ( par defaut 5)\n\
        -p probabilité que de la poussière apparaisse à chaque tour (defaut : 0.25)\n\
        -j probabilité qu'un bijou apparaisse à chaque tour (defaut : 0.10)\n\
        -g lance l'interface graphique (seulemet avec grille de taille 5)\n\
        -d debug pas de threads "




def main(argv):

    FREQ_LEARN = 0 # 0 == False
    ALGO = aStarSearch
    HEURISTIQUE = heuristic3
    GRAPHIC = False
    DEBUG = False
    SIZE = 5
    P_DUST = 0.25
    P_JEWEL= 0.1

    algo_dict = {"BFS":breadth_first_search,"DFS":depth_first_search,"A":aStarSearch}
    h_dict = {"0":nullHeuristic,"1":heuristic1,"2":heuristic2,'3':heuristic3}

    try:
      opts, args = getopt.getopt(argv,"hA:H:f:gdj:s:p:")
    except getopt.GetoptError:
      print(help)
      sys.exit(2)
    for opt, arg in opts:
      
      if opt == '-h':
         print(help)
         sys.exit()
      elif opt == '-A':
        ALGO = algo_dict[arg]
      elif opt == '-H':
        HEURISTIQUE = h_dict[arg]
      elif opt == '-f':
        FREQ_LEARN = int(arg)
      elif opt == '-s':
        SIZE = int(arg)
      elif opt == '-p':
        P_DUST= float(arg)
      elif opt == '-j':
        P_JEWEL = float(arg)
      elif opt == '-g':
        if SIZE==5 : GRAPHIC=True
      elif opt == '-d':
        DEBUG=True
    
    #print(str(FREQ_LEARN ),str(ALGO),str(HEURISTIQUE),str(PROBLEM ),str(GRAPHIC ),str(DEBUG ),str(SIZE),str(P_DUST ),str(P_JEWEL))
    env = Environment(SIZE,SIZE,p_dust=P_DUST,p_jewel=P_JEWEL)

    
    if ALGO in (breadth_first_search,depth_first_search):
        aspi = Agent_aveugle(env,ALGO,FREQ_LEARN)
    if ALGO in [aStarSearch]:
        aspi = Agent_informe(env,ALGO,FREQ_LEARN,HEURISTIQUE)

    
    

    if DEBUG :
        c =0
        if GRAPHIC :
            env.init_graphique()
        
        while True:
            clear()
            print("iter : "+str(c)+" Score : "+str(env.get_score())+ " periode : "+str(aspi.periode))
            c+=1
            env.update()
            aspi.sensor(env)
            action = aspi.get_action()
            env.agent_update(action)
            if FREQ_LEARN and c%FREQ_LEARN==0:
                aspi.learn(env.get_score())
            env.show()
            if GRAPHIC : env.show_graphique()
    else :

        kill = threading.Event()
        fil_env = threading.Thread(target=env_loop, args=(env,GRAPHIC))
        
        fil_agt= threading.Thread(target=agent_loop, args=(aspi,env,FREQ_LEARN))
        fil_env.start()
        fil_agt.start()
        

        try:
            while fil_env.join():
                pass
        except KeyboardInterrupt :
            sys.exit()
        
        #fil_env.join()
        sys.exit()





if __name__ == "__main__":
   main(sys.argv[1:])










# def menu_select_agent():
#     clear = lambda: os.system('cls')

#     print("""
    
#     Veuillez selectionner un algorithme :
#         1. Non informé
#         2. Informé
        
#         3. Exit the program
#     """)
#     ans = input("")
#     if ans == "1":
#         return Agent1(env, breadth_first_search)
#     elif ans == "2":
#         return Agent2(env, aStarSearch)
#     elif ans == "3":
#         sys.exit()
#     else:
#         print("Valeur incorrecte")
#         time.sleep(2)
#         clear()
#         menu_select_agent()


# if __name__ == "__main__":
#     env = Environment(5, 5, p_dust=0.25, p_jewel=0.05)
#     aspi = menu_select_agent()

#     x = threading.Thread(target=env_loop, args=(env,))
#     x.start()
#     y = threading.Thread(target=agent_loop, args=(aspi, env))
#     y.start()
    
#     y.join()
#     sys.exit()
   
    
    
    # c =0
    # while True:
    #     clear()
    #     print("iter : "+str(c)+" Score : "+str(aspi.score)+ " Freq : "+str(aspi.freq))
    #     c+=1
    #     env.update()
    #     aspi.sensor(env)
    #     action = aspi.get_action()
    #     if c%FREQ_LEARN == 0 :
    #         aspi.learn(env.get_score())
    #     env.agent_update(action)
    #     env.show()
    #     sleep(1)

