from util import manhattanDistance
from game import Directions
import random
import util
from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min(
            [manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food)
                                  for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(
            newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(
            newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)

        def minimum(state, agentIndex, depth):
            if state.isLose() or state.isWin():  # If the game is finished(win or lose)
                # go to the evaluation function
                return self.evaluationFunction(state)

            if agentIndex == state.getNumAgents() - 1:  # If it is the last ghost
                return min(maximum(state.getNextState(agentIndex, action), depth) for action in state.getLegalActions(agentIndex))
                # Take the minimum value of the maximum function with the depth
            else:
                return min(minimum(state.getNextState(agentIndex, action), agentIndex + 1, depth) for action in
                           state.getLegalActions(agentIndex))
                # If not, keep taking the minimum value of this function with the next agent

        def maximum(state, depth):
            # If the game is finished(win or lose or no more depth)
            if state.isLose() or state.isWin() or depth == self.depth:
                # go to the evaluation function
                return self.evaluationFunction(state)

            return max(minimum(state.getNextState(0, action), 1, depth + 1) for action in state.getLegalActions(0))
            # Take the maximum value of the minimum function on the pacman and the next depth

        best = max(gameState.getLegalActions(0),
                   key=lambda action: minimum(gameState.getNextState(0, action), 1, 1))
        # The best action is the maximum sorted by action in minimum function
        return best

        raise NotImplementedError("To be implemented")
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        def minimum(state, agentIndex, depth, a, b):
            if state.isLose() or state.isWin():  # If the game is finished(win or lose)
                # go to the evaluation function
                return self.evaluationFunction(state)

            v = float("inf")
            for action in state.getLegalActions(agentIndex):
                if agentIndex == state.getNumAgents() - 1:  # If it is the last ghost
                    newV = maximum(state.getNextState(
                        agentIndex, action), depth, a, b)  # record the return value of maximum function
                else:  # If not
                    newV = minimum(state.getNextState(
                        agentIndex, action), agentIndex + 1, depth, a, b)  # record the value of minimum function with the next agent

                # update current value with minimum between current value and the new value
                v = min(v, newV)
                if v < a:  # If the value is smaller than the alpha
                    return v
                # Save beta as the minimum between beta and current value
                b = min(b, v)
            return v

        def maximum(state, depth, a, b):
            # If the game is finished(win or lose or no more depth)
            if state.isLose() or state.isWin() or depth == self.depth:
                # go to the evaluation function
                return self.evaluationFunction(state)

            v = float("-inf")
            # pruning
            if depth == 0:  # If at the first layer
                best = state.getLegalActions(0)  # Take the pacman's state
            for action in state.getLegalActions(0):  # For the pacman's actions
                newV = minimum(state.getNextState(
                    0, action), 1, depth + 1, a, b)  # record the value of minimum function on the pacman and the next depth
                if newV > v:  # Update the value if the new one is greater than current
                    v = newV
                    if depth == 0:  # And if at the first layer
                        best = action  # Take this action
                if v > b:  # Return the current value if it is greater than beta
                    return v
                # Save alpha as the maximum between alpha and current value
                a = max(a, v)

            if depth == 0:  # If at the first layer
                return best
            return v

        # Start by taking maximum with layer 0, large alpha beta
        best = maximum(gameState, 0, float("-inf"), float("inf"))
        return best

        raise NotImplementedError("To be implemented")
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)

        def expectation(state, agentIndex, depth):
            if state.isLose() or state.isWin():  # If the game is finished(win or lose)
                # go to the evaluation function
                return self.evaluationFunction(state)

            # the probability is one out of total num of actions
            probability = 1.0 / len(state.getLegalActions(agentIndex))
            val = 0
            for action in state.getLegalActions(agentIndex):
                if agentIndex == state.getNumAgents() - 1:  # If it is the last ghost
                    val += maximum(state.getNextState(agentIndex,
                                                      action), depth) * probability  # Add the maximum function times probability
                else:
                    val += expectation(state.getNextState(agentIndex, action), agentIndex +
                                       1, depth) * probability  # If not, add the expectation with the next agent
            return val

        def maximum(state, depth):
            # If the game is finished(win or lose or no more depth)
            if state.isLose() or state.isWin() or depth == self.depth:
                # go to the evaluation function
                return self.evaluationFunction(state)

            val = max(expectation(state.getNextState(0, action), 1, depth + 1)
                      for action in state.getLegalActions(0))  # Take the maximum value of expectation on the next depth
            return val

        best = max(gameState.getLegalActions(), key=lambda action: expectation(
            gameState.getNextState(0, action), 1, 1))
        return best  # The best action is the maximum sorted by action in expectation function

        raise NotImplementedError("To be implemented")
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)

    pacman = currentGameState.getPacmanPosition()  # Get the pacman's position
    # Store the position of the foods in a list
    foods = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()  # Get the position of the ghosts
    closestFoodDis = min(manhattanDistance(pacman, food)
                         for food in foods) if foods else 5  # Get the distance of the closest food
    closestGhostDis = min(manhattanDistance(pacman, ghost.getPosition())
                          for ghost in ghosts)  # Get the distance of the closest ghost
    score = currentGameState.getScore()  # Get the score
    evaluation = 1.0 / closestFoodDis + score - closestGhostDis
    """
    1. The closer the food is, the greater the fraction is
    2. add up the original score
    3. Cut off the closest ghost's distance
    """
    return evaluation

    raise NotImplementedError("To be implemented")
    # End your code (Part 4)


# Abbreviation
better = betterEvaluationFunction
