import util

class BlackjackMDP(util.MDP):
    def __init__(self, cardValues, multiplicity, threshold, peekCost):
        """
        cardValues: array of card values for each card type
        multiplicity: number of each card type
        threshold: maximum total before going bust
        peekCost: how much it costs to peek at the next card
        """
        self.cardValues = cardValues
        self.multiplicity = multiplicity
        self.threshold = threshold
        self.peekCost = peekCost

    # Return the start state.
    # Look at this function to learn about the state representation.
    # The first element of the tuple is the sum of the cards in the player's
    # hand.
    # The second element is the index (not the value) of the next card, if the player peeked in the
    # last action.  If they didn't peek, this will be None.
    # The final element is the current deck.
    def startState(self):
        return (0, None, (self.multiplicity,) * len(self.cardValues))  # total, next card (if any), multiplicity for each card

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be done in succAndProbReward
    def actions(self, state):
        return ['Take', 'Peek', 'Quit']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.  Indicate a terminal state (after quitting or
    # busting) by setting the deck to None. 
    # When the probability is 0 for a particular transition, don't include that 
    # in the list returned by succAndProbReward.
    def succAndProbReward(self, state, action):
        # BEGIN_YOUR_CODE

        sumValue, peekIndex, deckState = state

        # step1. 종료 조건인지 확인하기
        if deckState is None :
            return []

        result = []

        if action == "Take":
            if peekIndex is None:
                for cardindex, cardCount in enumerate(deckState):

                    if cardCount==0:
                        continue

                    deckList = list(deckState)
                    deckList[cardindex]-=1
                    deckTuple = tuple(deckList)

                    newValue = sumValue + self.cardValues[cardindex]
                    prob = cardCount/sum(deckState)
                    reward =0

                    if newValue > self.threshold:
                        deckTuple=None
                    elif sum(deckTuple) ==0 :
                        deckTuple=None; reward = newValue


                    nextState = (newValue,None,deckTuple)
                    result.append((nextState, prob, reward))


            else:
                    # existing peekIndex
                    # update deck state
                deckList = list(deckState)
                deckList[peekIndex] -= 1
                deckTuple = tuple(deckList)
                newValue = sumValue + self.cardValues[peekIndex]

                prob = 1
                reward = 0

                if newValue > self.threshold:
                    deckTuple=None
                elif sum(deckTuple) == 0 :
                    deckTuple=None; reward=newValue

                nextState=(newValue,None,deckTuple)
                result.append((nextState, prob, reward))


        elif action =="Peek":
            sumValue, peekIndex, deckState = state

            if peekIndex is None:
                for cardIndex, cardCount in enumerate(deckState):
                    if cardCount==0 :
                        continue
                    prob = cardCount/sum(deckState)
                    nextState=(sumValue, cardIndex, deckState)
                    reward = -self.peekCost

                    result. append ((nextState, prob, reward))

        elif action == "Quit":
            nextState=(sumValue, peekIndex, None)
            prob=1
            reward = sumValue
            result.append((nextState, prob, reward))


        return result
        # END_YOUR_CODE

    def discount(self):
        return 1

print('\n========== Problem C ==========')
mdp1 = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=10, peekCost=1)
startState = mdp1.startState()
preBustState = (6, None, (1, 1))
postBustState = (11, None, None)
mdp2 = BlackjackMDP(cardValues=[1, 5], multiplicity=2, threshold=15, peekCost=1)
preEmptyState = (11, None, (1,0))
'''
print('\n---------- Test c1 ----------')
# Make sure the succAndProbReward function is implemented correctly.
vanilla_tests = [
    ([((1, None, (1, 2)), 0.5, 0), ((5, None, (2, 1)), 0.5, 0)], mdp1, startState, 'Take'),
    ([((0, None, None), 1, 0)], mdp1, startState, 'Quit'),
    ([((7, None, (0, 1)), 0.5, 0), ((11, None, None), 0.5, 0)], mdp1, preBustState, 'Take'),
    ([], mdp1, postBustState, 'Take'),
    ([], mdp1, postBustState, 'Quit'),
    ([((12, None, None), 1., 12)], mdp2, preEmptyState, 'Take'),
]
print('Vanilla Blackjack')
for no, (answer, mdp, state, action) in enumerate(vanilla_tests):
    print('No %d'%(no+1), end=' ')
    if answer != mdp.succAndProbReward(state, action):
        print('=> wrong')
    else:
        print('=> right')
    print('- state: {}, action: {}'.format(state, action))
    print('- true answer =', answer)
    print('- your answer =', mdp.succAndProbReward(state, action))
'''
"""
print('\n---------- Test c2 ----------')
peek_tests = [
    ([((0, 0, (2, 2)), 0.5, -1), ((0, 1, (2, 2)), 0.5, -1)], mdp1, startState, 'Peek'),
    ([((1 , None, (1, 2) ), 1, 0)] , mdp1, (0, 0, (2, 2)), 'Take'),
    ([], mdp1, postBustState, 'Peek'),
]
print('Peeking Blackjack')
for no, (answer, mdp, state, action) in enumerate(peek_tests):
    print('No %d'%(no+1), end=' ')
    if answer != mdp.succAndProbReward(state, action):
        print('=> wrong')
    else:
        print('=> right')
    print('- state: {}, action: {}'.format(state, action))
    print('- true answer =', answer)
    print('- your answer = ', mdp.succAndProbReward(state, action))
"""
'''
print('\n---------- Test c3 ----------')
algorithm = ValueIteration()
algorithm.solve(mdp1, verbose=True)
for s in algorithm.V:
    print('V(%s) = %f'%(s, algorithm.V[s]))
print('------------')
for s in algorithm.pi:
    print('pi(%s) = %s'%(s, algorithm.pi[s]))
print('------------')
print('Q1 (6, None, (1, 1) => %s'%(algorithm.pi[(6, None, (1, 1))]))
print('Q2 (6, 0, (1, 1) => %s'%(algorithm.pi[(6, 0, (1, 1))]))
'''