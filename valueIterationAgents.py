# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        self.values_prime = self.values.copy()

        # Write value iteration code here
        "*** YOUR CODE HERE ***"


        # if self.iterations > 0:
        #     self.iterations += 2

        for i in range (self.iterations):
            #update the values
            
            #iterate through states
            for s in mdp.getStates():
                #max = 0
                options = []
                #iterate over actions
                if self.mdp.isTerminal(s):
                    self.values_prime[s] = self.mdp.getReward(s,None, None)
                    continue
                tot = 0
                for a in self.mdp.getPossibleActions(s):
                    nexts = self.mdp.getTransitionStatesAndProbs(s, a)
                    #for each action, calcuate value*probability of each possible successor
                    sum = 0
                    for newState in nexts:
                        #newState: (state,probability)
                        #options.append(newState[1]*self.values[newState[0]])
                        sum +=  newState[1]*self.values[newState[0]]
                    options.append(sum)
    

                #take the max
                maxVal = max (options)

                self.values_prime[s] =  self.discount *(maxVal) + (self.mdp.getReward(s,None, None))
            self.values = self.values_prime.copy()
            #self.values = self.values_prime.copy()


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        succs = self.mdp.getTransitionStatesAndProbs(state, action)
        #list of (state, prob)
        total =0
        #print succs
        # print self.mdp.isTerminal(state), succs
        for s in succs:
            #print self.values[s[0]]
            total += s[1] * self.values[s[0]]
        #print total
        #add reward in this state and gamma * future reward

        currentReward = self.mdp.getReward(state, None, None)
        future = self.discount * total
        return future + currentReward


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        bestScore = None
        bestMove = None
        actions = self.mdp.getPossibleActions(state)
        for a in actions:
            score = self.getQValue(state, a)
            if bestScore is None or score > bestScore:
                bestMove = a
                bestScore = score

        return bestMove
        

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
