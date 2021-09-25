import Agent
import Environment


if __name__ == "__main__":
    agent = Agent()
    env = Environment()

    env.updateEnvironment()  # thread
    while(True):
        # get the environment
        agent.update_sensors(env)
        #
        agent.getAction(env)
