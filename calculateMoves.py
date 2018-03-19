# TODO(Use proper docstring for documentation)
# CONSTANTS ------------------------------------------------------------------
BOARD_SIZE = 8
# ----------------------------------------------------------------------------

# CLASS DEFINITIONS ----------------------------------------------------------
class Movement:
    def __init__(self, state):
        self.state = state

    def updateState(self, newState):
        self.state = newState

    # returns list of possible moves
    def calcMovesForCoord(self, coord):
        i, j = coord
        moveList = []
        for move in [self.canGoRight_(i, j),
                     self.canGoLeft_(i, j),
                     self.canGoUp_(i, j),
                     self.canGoDown_(i, j)]:
            if move:
                moveList.append(move)
        return moveList

    # checks if cell is empty, (does not contain pieces and is not a corner)
    def isEmpty_(self, i, j):
        return ((i, j) not in self.state.blackPieces
                and (i, j) not in self.state.whitePieces
                and not corner(i, j))

    # series of functions that checks if a piece can move or jump.
    # canGo functions check if the adjacent cell is empty and within bounds.
    # if not empty, it is a piece or a corner. We then call canJump functions
    # to see if player can jump - the target cell for jump is empty and within
    # bounds.
    def canJumpRight_(self, i, j):
        if withinBounds(i+2, j) and self.isEmpty_(i+2, j):
            return (i+2, j )

    def canJumpLeft_(self, i, j):
        if withinBounds(i-2, j ) and self.isEmpty_(i-2, j):
            return (i-2, j )

    def canJumpUp_(self, i, j):
        if withinBounds(i , j-2) and self.isEmpty_(i, j-2):
            return (i, j-2)

    def canJumpDown_(self, i, j):
        if withinBounds(i, j+2) and self.isEmpty_(i , j+2):
            return (i, j+2)

    def canGoRight_(self, i, j):
        if withinBounds(i+1, j) and self.isEmpty_(i+1, j):
            return (i+1, j)
        return self.canJumpRight_(i, j)

    def canGoLeft_(self, i, j):
        if withinBounds(i-1, j ) and self.isEmpty_(i-1, j ):
            return (i-1, j)
        return self.canJumpLeft_(i, j)

    def canGoUp_(self, i, j):
        if withinBounds(i , j-1) and self.isEmpty_(i , j-1):
            return (i , j-1)
        return self.canJumpUp_(i, j)

    def canGoDown_(self, i, j):
        if withinBounds(i , j+1) and self.isEmpty_(i , j+1):
            return (i , j+1)
        return self.canJumpDown_(i, j)


class GameState:
    # sets of whitePieces and blackPieces
    # list of prevMoves, construct from parent

    def __init__(self, whitePieces, blackPieces, prevMoves):
        self.whitePieces = whitePieces
        self.whiteSorted = tuple(sorted(whitePieces))
        self.blackPieces = blackPieces
        self.blackSorted = tuple(sorted(blackPieces))
        self.prevMoves = prevMoves

    def __hash__(self):
        return hash((self.whiteSorted, self.blackSorted))

    def __eq__(self, otherGameState):
        return (self.whitePieces == otherGameState.whitePieces
                and self.blackPieces == otherGameState.blackPieces)

    def updateSets(self, newWhiteSet, newBlackSet):
        self.whitePieces = newWhiteSet
        self.whiteSorted = tuple(sorted(newWhiteSet))
        self.blackPieces = newBlackSet
        self.blackSorted = tuple(sorted(newBlackSet))

# ----------------------------------------------------------------------------

# FUNCTION DEFINITIONS -------------------------------------------------------
def corner(i, j):
    corner_coords = {0, BOARD_SIZE - 1}
    return i in corner_coords and j in corner_coords


def withinBounds(i, j):
    return (0 <= i < BOARD_SIZE) and (0 <= j < BOARD_SIZE)



def setUpBoard():
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

def isEnemy(enemyPieces, coordinate):
    i, j = coordinate
    return withinBounds(i, j) and (coordinate in enemyPieces or corner(i, j))


def canEat(enemyPieces, side1, side2):
    return isEnemy(enemyPieces, side1) and isEnemy(enemyPieces, side2)


def removeEatenPieces(ownPieces, enemyPieces):
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


# Check if we are in a goal state (no more black pieces) for massacre
def massacreGoalCheck(gameState):
    return (len(gameState.blackPieces) == 0)


def debugPrintState(state):
    print("the following is white pieces")
    print(state.whitePieces)
    print("the following is blackPieces")
    print(state.blackPieces)
    print("movelist")
    print(state.prevMoves)


def printSequence(moveSequence):
    for (x, y) in moveSequence:
        print(str(x) + ' -> ' + str(y))


def dfs(startState, maxDepth):
    numWhite = len(startState.whitePieces)
    visited = {startState}
    to_visit = [startState]
    while to_visit:
        currentState = to_visit.pop()

        # Check if already reached goal state!
        if massacreGoalCheck(currentState):
            printSequence(currentState.prevMoves)
            return True

        if len(currentState.prevMoves) == maxDepth:
            continue

        movementService.updateState(currentState)
        visited.add(currentState)

        # Generate childStates (by using calcMoves on each whitePiece)
        for whitePiece in currentState.whitePieces:
            # Get all moves that piece can do, then for each move generate the
            # GameState node that results from that move with updated white set,
            # black set and prevMoves list.
            moveList = movementService.calcMovesForCoord(whitePiece)
            for move in moveList:
                newWhitePieces = currentState.whitePieces.copy()
                newBlackPieces = currentState.blackPieces.copy()
                newPrevMoves = currentState.prevMoves.copy()

                newWhitePieces.remove(whitePiece)
                newWhitePieces.add(move)
                newPrevMoves.append((whitePiece,move))

                # we then remove eaten black pieces. (white has priority)
                removeEatenPieces(newBlackPieces, newWhitePieces)
                # then we remove eaten white pieces.
                removeEatenPieces(newWhitePieces, newBlackPieces)

                newGameState = GameState(newWhitePieces, newBlackPieces, newPrevMoves)

                # If number of whitepieces decreased, it's not a good move so
                # don't add to to_visit stack. Also check if newnode has
                # already been visited state.
                if (len(newGameState.whitePieces) == numWhite
                    and newGameState not in visited):
                    to_visit.append(newGameState)
                    visited.add(newGameState)
    return False


# Set up initial GameState according to input
def setUpBoard():
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


# Prints the total number of moves for both players
def calcTotalMoves():
    whiteMoves = 0
    blackMoves = 0

    for whiteCoord in startState.whitePieces:
        whiteMoves += len(movementService.calcMovesForCoord(whiteCoord))
    for blackCoord in startState.blackPieces:
        blackMoves += len(movementService.calcMovesForCoord(blackCoord))

    print(whiteMoves)
    print(blackMoves)


# Print sequence of moves that will lead to eating all black pieces
def massacre(startState):
    depth = 1
    while True:
        if dfs(startState, depth): # found a solution!
            break
        else:
            depth += 1

# ----------------------------------------------------------------------------

startState = GameState(set(), set(), [])
movementService = Movement(startState)

setUpBoard()

# determine if it's "Moves" or "Massacre"
command = input()

if command == 'Moves':
    # calculate available moves for each player
    calcTotalMoves()
elif command == 'Massacre':
    # do massacre stuff
    massacre(startState)
    print("massacre complete")
else:
    print("Please enter a valid command (ie. 'Moves', 'Massacre')")
