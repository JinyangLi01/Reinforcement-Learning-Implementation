# Imports

import numpy as np
import matplotlib.pyplot as plt
import math
import itertools
import pickle


# Q Learing  Algorithm class
class Q_learning(object):
    # Main class to train the TD algorithm for the n number of episodes
    # the class takes the policy, alpha and lambda as the input
    def __init__(self, gamma, alpha, env, state_space, steps, e, order=3, actions=4, plot=False):
        self.alpha = alpha
        self.gamma = gamma
        self.env = env
        self.state_space = state_space
        self.q_value = np.random.uniform(0, 1, size= (state_space, actions))
        self.episolon = e
        self.steps = steps
        self.td_error = []
        self.order = order
        self.probs = [0.25, 0.25, 0.25, 0.25]
        self.plot = plot
        if self.env.name == "cart":
            self.c = np.array(list(itertools.product(range(order+1), repeat=4)))
            self.w = np.zeros((4, 2))  # linear function approximator


    def train(self, episodes):
        # Method to run the q_learning algorithm for n episodes
        # input: episodes
        # return: None
        for _ in range(episodes):
            state = self.env.reset() # reset the environment
            status = self.env.status

            print("Episode: ", _)
            # While we do not reach the terminal state
            count = 0
            while not status:

                # Choosing the action a_prime at the state s_prime

                if self.env.name == "cart":
                    action = self.sampleActionCart(state)  # todo sarsa policy change action function to accomdate the q value

                elif self.env.name == "grid":
                    action = self.sampleActionGrid(state) # todo sarsa policy

                else:
                    assert "Not Supported environment"

                # performing the action in the environment and observing the reward and moving to the new state s_prime
                new_state, reward, status = self.env.performAction(action)

                if status:
                    break

                # update the q values according to the previous state and new state
                self.update(reward, state, new_state, action)

                # changing the last state to new state
                state = new_state

        if self.plot:
            self.plotTdError()


    def update(self, reward, s, new_s, action):
        # Update the value function
        # input: reward, curr_state, and new state
        # return: None (update)

        # Getting the current and next state
        if self.env.name == "grid":
            i, j = s[0], s[1]
            i_new, j_new = new_s[0], new_s[1]
            s = i*5+j
            new_s= i_new*5 + j_new

            # gettting the last value and new value
            curr_state_value = self.q_value[s, action]
            next_state_value = max(self.q_value[new_s, :])

        else:
            temp_s = np.reshape(np.array(s), (1, 4))
            temp_new_s = np.reshape(np.array(new_s), (1, 4))
            curr_state_value = np.dot(temp_s, self.w)[0, action]
            next_state_value = np.dot(temp_new_s, self.w)[0, action_prime]

        # computing the td error
        delta_t = reward + self.gamma*next_state_value - curr_state_value   # td error

        # updating the value function if episode is under 100 else calculating
        # the squared error and adding the value to the td_error list.
        if self.env.name == "grid":
            self.q_value[s, action] = self.q_value[s, action] + self.alpha*delta_t

        else:
            grad = 1.0
            self.w = self.w + self.alpha * delta_t * grad

        self.td_error.append(delta_t*delta_t)

    # softmax tabular
    def sampleActionGrid(self, state, e_greedy=False):
        i, j = state
        index = i*5+j
        if e_greedy and np.random.rand() < self.episolon:
            action = np.random.choice([0, 1, 2, 3], p=self.probs)
        else:
            action = np.argmax(self.q_value[index, :])
        return action


    def sampleActionCart(self, state, e_greedy=True):
        # if e_greedy
        if e_greedy and np.random.rand() < self.episolon:
            action = np.random.choice([0, 1])

        # linear policy
        else:
            temp_s = np.reshape(np.array(state), (1, 4))
            action = np.argmax(np.dot(temp_s, self.w))

        return action

    def plotTdError(self):
        plt.plot(self.td_error)
        plt.show()

    def saveTDerror(self):
        if self.env.name == "cart":
            name = "TD_error/" + self.env.name + "_" + str(self.order) + "_" + str(self.alpha) + ".p"
        else:
            name = "TD_error/" + self.env.name + "_" + str(self.alpha) + ".p"
        pickle.dump(self.td_error, open(name , "wb"))

