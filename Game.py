import threading
from time import sleep
import os
clear = lambda: os.system('cls')

from Agents import Agent_1
from Environment import Environment
from searchTree import depthFirstSearch,breadthFirstSearch


if __name__ == "__main__":
    env = Environment(5,5,p_dirt=0.25,p_jewel=0)
    aspi = Agent_1(env,breadthFirstSearch)  


    #x = threading.Thread(target=env.update_environment, args=())
    #x.start()

    while True:
        clear()
        env.update()
        msg =aspi.getAction(env)
        env.agent_update(msg)
        env.show(str(msg))
        sleep(1)
