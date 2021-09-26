from Agent import Agent
from Environment import Environment
import threading
import time


if __name__ == "__main__":
    agent = Agent()
    env = Environment()

    x = threading.Thread(target=env.update_environment, args=())
    x.start()

    while True:
        # get the environment
        # agent.update_sensors(env)
        # Action
        # agent.get_action(env)

        # Thread sleep & tests
        print("Main Thread is up")
        print(env.get_matrix())
        time.sleep(2)
