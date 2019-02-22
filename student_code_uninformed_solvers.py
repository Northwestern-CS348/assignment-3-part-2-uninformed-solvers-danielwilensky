
from solver import *
from collections import deque

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.stack = deque()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        self.visited[self.currentState] = True
        if self.currentState.state == self.victoryCondition:
            return True
        moves = self.gm.getMovables() #don't need to check if false right? Always have a move
        if len(self.currentState.children) == 0:
            for i in moves:
                self.gm.makeMove(i)
                newState = GameState(self.gm.getGameState(), self.currentState.depth + 1, i)
                if newState not in self.visited.keys(): #only state gets hashed so doesn't matter its a diff object
                    self.visited[newState] = False
                newState.parent = self.currentState
                #this will add node to tree multiple times, think its wrong, but thats how they have order
                self.currentState.children.append(newState) #implicitly all in order of getMovables()
                self.gm.reverseMove(i)
        for i in self.currentState.children[::-1]:
            if self.visited[i] == False:
                self.stack.appendleft(i)
        nextState = self.stack.popleft()
        move = nextState.requiredMovable
        while self.currentState.nextChildToVisit == len(self.currentState.children):
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState == self.currentState.parent
        nextState.parent.nextChildToVisit += 1
        self.gm.makeMove(move)
        self.currentState = nextState
        if self.currentState.state == self.victoryCondition: ##make a test where actually win
            return True
        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = deque()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        self.visited[self.currentState] = True
        if self.currentState.state == self.victoryCondition:  # same as self.gm.isWon()?
            return True
        moves = self.gm.getMovables()  # don't need to check if false right? Always have a move
        if len(self.currentState.children) == 0:
            for i in moves:
                self.gm.makeMove(i)
                newState = GameState(self.gm.getGameState(), self.currentState.depth + 1, i)
                if newState not in self.visited.keys():  # only state gets hashed so doesn't matter its a diff object
                    self.visited[newState] = False
                    newState.parent = self.currentState
                    self.currentState.children.append(newState)  # implicitly all in order of getMovables()
                self.gm.reverseMove(i)
        for i in self.currentState.children:
            if self.visited[i] == False:
                self.queue.append(i)
        nextState = self.queue.popleft()
        move = nextState.requiredMovable
        backMoves = deque()
        if nextState.depth == self.currentState.depth:
            nextStateAncestor = nextState
        else: #nextState can only be deeper
            nextStateAncestor = nextState.parent
            backMoves.appendleft(move)
        while self.currentState != nextStateAncestor:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            backMoves.appendleft(nextStateAncestor.requiredMovable)
            nextStateAncestor = nextStateAncestor.parent
        for i in backMoves:
            self.gm.makeMove(i) #includes move
        self.currentState = nextState
        if self.currentState.state == self.victoryCondition:  # do I use self.victoryCondition? I just use self.gm.isWon()
            return True
        return False

