import threading
from time import sleep
import os

from Agents import Agent1
from Environment import Environment
from searchTree import depth_first_search, breadth_first_search

clear = lambda: os.system('cls')


def env_loop(env):
    while True:
        clear()
        env.update()
        env.show()
        sleep(1)


def agent_loop(agent, env):
    while True:
        action = agent.get_action(env)
        env.agent_update(action)
        sleep(1)


if __name__ == "__main__":
    env = Environment(5, 5, p_dirt=0.25, p_jewel=0)
    aspi = Agent1(env, breadth_first_search)

    x = threading.Thread(target=env_loop, args=(env,))
    x.start()
    y = threading.Thread(target=agent_loop, args=(aspi, env))
    y.start()
