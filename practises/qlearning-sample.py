import numpy as np
import random
import sys

Q = np.zeros((6, 6), np.float)

R = np.array([
    [-1, -1, -1, -1, 0, -1],
    [-1, -1, -1, 0, -1, 100],
    [-1, -1, -1, 0, -1, -1],
    [-1, 0, 0, -1, 0, -1],
    [0, -1, -1, 0, -1, 100],
    [-1, 0, -1, -1, 0, 100]
], dtype=np.float)


def randomAction(state):
    rewards = R[state]
    actions = [i for i in range(6) if rewards[i] >= 0]
    action = random.choice(actions)
    reward = rewards[action]
    return (action, reward)


def randomNextState(state=None):
    if state == None:
        return random.choice(range(6))
    else:
        rewards = R[state]
        nextStates = [i for i in range(6) if rewards[i] >= 0]
        return random.choice(nextStates)


def getNextStates(action):
    rewards = R[action]
    return [i for i in range(6) if R[action][i] >= 0]


def getAllActions(state):
    return [i for i in range(6) if R[state][i] >= 0]


def getAllState(action):
    return [i for i in range(6) if R[i, action] >= 0]

def maxQ(state):
    rewards=Q[state]
    return max(rewards)

# Q(s,a)=R(s,a)+y*max{Q(s',a')}
def updateQ(state, action):
    sys.stdout.write('Q(%s,%s)' % (state, action))
    Q[state,action]=R[state,action]+0.8*maxQ(action)


def isGoalState(state):
    return state == 5


def randomStartState():
    return random.choice(range(6))


def startEpisode():
    state = randomNextState()
    # action=state
    sys.stdout.write('state : %s ' % state)
    while not isGoalState(state):
        nextStates=getAllState(state)
        nextState=random.choice(nextStates)
        action=nextState
        updateQ(state,action)
        state = nextState
        sys.stdout.write(' --> %s ' % state)
    # updateQ(state,action)

def tranining():
    trainingCount = 0
    while trainingCount < 1000:
        sys.stdout.write('start %s episode ' % trainingCount)
        startEpisode()
        trainingCount += 1
        sys.stdout.write('\n')
    print(Q)


# print(randomStartState())
tranining()
# print(getAllActions(1))
# print(getAllState(5))