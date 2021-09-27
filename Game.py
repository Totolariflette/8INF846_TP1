import threading
from time import sleep
import os
clear = lambda: os.system('cls')

from Agents import Agent_1
from Environment import Environment
from searchTree import depthFirstSearch,breadthFirstSearch




def env_loop(env):
    while True :
        clear()
        env.update()
        env.show()
        sleep(1)


def agent_loop(agent,env):
    while True :
        action = agent.getAction(env)
        env.agent_update(action)
        sleep(1)


if __name__ == "__main__":
    env = Environment(5,5,p_dirt=0.25,p_jewel=0)
    aspi = Agent_1(env,breadthFirstSearch)  


    x = threading.Thread(target=env_loop,args=(env,))
    x.start()
    y =threading.Thread(target=agent_loop, args=(aspi,env))
    y.start()

    

   




