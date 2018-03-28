"""COMP30024 Artificial Intelligence Project Part A (2018 Sem 1)

Authors:
Jia Shun LOW (743436)
Joanna Grace Cho Ern LEE (710094)

This module carries out two calculations:
    - The number of available moves for each player
    - A sequence of moves for White pieces that would eliminate all Black pieces
      assuming the Black pieces are unable to move.

An example input is:
X - - - - - - X
- - - - - - - -
- - - - - O O -
- - - - @ O - -
- - - - - - - -
- - - - - O - -
- - - - @ - @ @
X - - - - - - X
Moves

where the first 8 lines represent the board and the pieces, and the last line
specifies which calculation to be printed to standard output.
"""

BOARD_SIZE = 8


class Movement:
    """Class for all movement functionality required for any piece."""
    def __init__(self, state):
        """Stores the current state of the game at setup. This lets the class
        know where all the pieces are at the current point in time.
        """
        self.state = state

    def updateState(self, newState):
        """Updates the current game state so calculations are up to date."""
        self.state = newState

    def calcMovesForCoord(self, coord):
        """Returns a list of all coordinates reachable from given coord."""
        i, j = coord
        moveList = []
        for move in [self.canGoRight_(i, j),
                     self.canGoLeft_(i, j),
                     self.canGoUp_(i, j),
                     self.canGoDown_(i, j)]:
            if move:
                moveList.append(move)
        return moveList

    def isEmpty_(self, i, j):
        """Checks if there are any pieces in the cell specified by (i, j)."""
        return ((i, j) not in self.state.blackPieces
                and (i, j) not in self.state.whitePieces
                and not corner(i, j))

    def canJumpRight_(self, i, j):
        """Checks if piece can jump right"""
        if withinBounds(i+2, j) and self.isEmpty_(i+2, j):
            return (i+2, j )

    def canJumpLeft_(self, i, j):
        """Checks if piece can jump left"""
        if withinBounds(i-2, j ) and self.isEmpty_(i-2, j):
            return (i-2, j )

    def canJumpUp_(self, i, j):
        """Checks if piece can jump up"""
        if withinBounds(i , j-2) and self.isEmpty_(i, j-2):
            return (i, j-2)

    def canJumpDown_(self, i, j):
        """Checks if piece can jump down"""
        if withinBounds(i, j+2) and self.isEmpty_(i , j+2):
            return (i, j+2)

    def canGoRight_(self, i, j):
        """Checks if piece can move right"""
        if withinBounds(i+1, j) and self.isEmpty_(i+1, j):
            return (i+1, j)
        return self.canJumpRight_(i, j)

    def canGoLeft_(self, i, j):
        """Checks if piece can move left"""
        if withinBounds(i-1, j ) and self.isEmpty_(i-1, j ):
            return (i-1, j)
        return self.canJumpLeft_(i, j)

    def canGoUp_(self, i, j):
        """Checks if piece can move up"""
        if withinBounds(i , j-1) and self.isEmpty_(i , j-1):
            return (i , j-1)
        return self.canJumpUp_(i, j)

    def canGoDown_(self, i, j):
        """Checks if piece can move down"""
        if withinBounds(i , j+1) and self.isEmpty_(i , j+1):
            return (i , j+1)
        return self.canJumpDown_(i, j)


class GameState:
    """Class which stores the state of the game at a given time. This includes
    the locations of all the white pieces and all the black pieces on the board
    as well as the list of moves which derived this state from the StartState.
    """

    def __init__(self, whitePieces, blackPieces, prevMoves):
        self.whitePieces = whitePieces
        self.blackPieces = blackPieces

        # Store pieces in tuples as well so they are hashable
        self.whiteSorted = tuple(sorted(whitePieces))
        self.blackSorted = tuple(sorted(blackPieces))
        self.prevMoves = prevMoves

    def __hash__(self):
        """Customised hash function to use the tuple forms of the pieces."""
        return hash((self.whiteSorted, self.blackSorted))

    def __eq__(self, otherGameState):
        """Define state equality to be the respective locations of both the
        white and black pieces.
        """
        return (self.whitePieces == otherGameState.whitePieces
                and self.blackPieces == otherGameState.blackPieces)

    def updateSets(self, newWhiteSet, newBlackSet):
        """Updates the locations of the white and black pieces on the board."""
        self.whitePieces = newWhiteSet
        self.blackPieces = newBlackSet
        self.whiteSorted = tuple(sorted(newWhiteSet))
        self.blackSorted = tuple(sorted(newBlackSet))


def corner(i, j):
    """Checks if coordinates given is a corner of the board."""
    corner_coords = {0, BOARD_SIZE - 1}
    return i in corner_coords and j in corner_coords


def withinBounds(i, j):
    """Checks if coordinates given is on the board."""
    return (0 <= i < BOARD_SIZE) and (0 <= j < BOARD_SIZE)


def isEnemy(enemyPieces, coordinate):
    """Checks if coordinates belong to the enemy (or is a corner)."""
    i, j = coordinate
    return withinBounds(i, j) and (coordinate in enemyPieces or corner(i, j))


def canEat(enemyPieces, side1, side2):
    """Checks a piece between side1 and side2 will be eaten."""
    return isEnemy(enemyPieces, side1) and isEnemy(enemyPieces, side2)


def removeEatenPieces(ownPieces, enemyPieces):
    """Given both sets of coordinates, remove own eaten pieces."""
    toRemove = []
    for piece in ownPieces:
        i,j = piece
        down = (i,j+1)
        up = (i,j-1)
        left = (i-1,j)
        right = (i+1,j)

        # check if piece can be eaten from up and down / left and right
        # by checking if within bounds and if they are corner or white.
        if canEat(enemyPieces, up, down) or canEat(enemyPieces, left, right):
            toRemove.append(piece)
    for pieceToRemove in toRemove:
        ownPieces.remove(pieceToRemove)
    return ownPieces


def massacreGoalCheck(gameState):
    """Check if current state is the goal state (no more black pieces)."""
    return (len(gameState.blackPieces) == 0)


def setUpBoard(startState):
    """Sets up StartState according to the input."""
    blackPieces = set()
    whitePieces = set()
    # read from input and generate board
    for i in range(BOARD_SIZE):
        # add row to board
        rowInput = input().split()
        for j in range(BOARD_SIZE):
            char = rowInput[j]
            if char == 'O':
                whitePieces.add((j, i))
            elif char == '@':
                blackPieces.add((j, i))
    startState.updateSets(whitePieces, blackPieces)


def printSequence(moveSequence):
    """Prints sequence of moves according to project specs."""
    for (x, y) in moveSequence:
        print(str(x) + ' -> ' + str(y))


def dfs(startState, movementService, maxDepth):
    """Performs DFS, generating new child states until goal state found."""
    numWhite = len(startState.whitePieces)
    visited = {startState}
    to_visit = [startState]

    # Check if already reached goal state!
    if massacreGoalCheck(startState):
        printSequence(startState.prevMoves)
        return True

    while to_visit:
        currentState = to_visit.pop()

        movementService.updateState(currentState)
        visited.add(currentState)

        # Generate childStates (by using calcMoves on each whitePiece)
        for whitePiece in currentState.whiteSorted:
            # Get all moves that piece can do, then for each move generate the
            # GameState node that results from that move with updated white set,
            # black set and prevMoves list.
            moveList = movementService.calcMovesForCoord(whitePiece)

            for move in moveList:
                whitePieces = currentState.whitePieces.copy()
                blackPieces = currentState.blackPieces.copy()
                prevMoves = currentState.prevMoves.copy()

                whitePieces.remove(whitePiece)
                whitePieces.add(move)
                prevMoves.append((whitePiece,move))

                # we then remove eaten black pieces. (white has priority)
                removeEatenPieces(blackPieces, whitePieces)
                # then we remove eaten white pieces.
                removeEatenPieces(whitePieces, blackPieces)

                newGameState = GameState(whitePieces, blackPieces, prevMoves)

                # Check if already reached goal state!
                if massacreGoalCheck(newGameState):
                    printSequence(newGameState.prevMoves)
                    return True

                # If number of whitepieces decreased, it's not a good move so
                # don't add to to_visit stack. Also check if newnode has
                # already been visited state and the new node is below maxdepth
                if (len(newGameState.whitePieces) == numWhite
                        and newGameState not in visited
                        and len(currentState.prevMoves) < maxDepth):
                    to_visit.append(newGameState)
                    visited.add(newGameState)
    return False


def calcTotalMoves(startState, movementService):
    """Prints the total number of moves for both players."""
    whiteMoves = 0
    blackMoves = 0

    for whiteCoord in startState.whitePieces:
        whiteMoves += len(movementService.calcMovesForCoord(whiteCoord))
    for blackCoord in startState.blackPieces:
        blackMoves += len(movementService.calcMovesForCoord(blackCoord))

    print(whiteMoves)
    print(blackMoves)


def massacre(startState, movementService):
    """Print sequence of moves that will lead to eating all black pieces."""
    depth = 0
    while True:
        if dfs(startState, movementService, depth): # found a solution!
            break
        else:
            depth += 1


def main():
    startState = GameState(set(), set(), [])
    movementService = Movement(startState)
    setUpBoard(startState)

    # determine if it's "Moves" or "Massacre"
    command = input()

    if command == 'Moves':
        # calculate available moves for each player
        calcTotalMoves(startState, movementService)
    elif command == 'Massacre':
        # print out sequence of moves which leads to massacre of enemy pieces
        massacre(startState, movementService)
    else:
        print("Please enter a valid command (ie. 'Moves', 'Massacre')")


if __name__ == "__main__":
    main()
