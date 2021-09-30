import threading
import time
from time import sleep
import os
import sys
from tkinter import *

from Agents import Agent1,Agent2
from Environment import Environment
from searchTree import depth_first_search, breadth_first_search,aStarSearch

clear = lambda: os.system('cls')

FREQ_LEARN = 25



def env_loop(env):
    fenetre = Tk()
    fenetre.configure(bg='light blue')
    fenetre.title("IA_TP1")
    fenetre.resizable(0,0)
    while True:
        clear()
        env.update()
        env.show()
        env.show_graphique(fenetre)
        sleep(0.25)


def agent_loop(agent, env):
    c=1
    while True:
        print("iter : "+str(c)+" Score : "+str(agent.score)+ " Freq : "+str(agent.freq))
        agent.sensor(env)
        action = agent.get_action()
        env.agent_update(action)
        if env.tour >= c*FREQ_LEARN  :
            agent.learn(env.get_score())
            c+=1
        sleep(0.25)


def menu_select_agent():
    clear = lambda: os.system('cls')

    print("""
    
    Veuillez selectionner un algorithme :
        1. Non informé
        2. Informé
        
        3. Exit the program
    """)
    ans = input("")
    if ans == "1":
        return Agent1(env, breadth_first_search)
    elif ans == "2":
        return Agent2(env, aStarSearch)
    elif ans == "3":
        sys.exit()
    else:
        print("Valeur incorrecte")
        time.sleep(2)
        clear()
        menu_select_agent()


if __name__ == "__main__":
    env = Environment(5, 5, p_dust=0.25, p_jewel=0.05)
    aspi = menu_select_agent()

    x = threading.Thread(target=env_loop, args=(env,))
    x.start()
    y = threading.Thread(target=agent_loop, args=(aspi, env))
    y.start()
    
    y.join()
   
    
    
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

