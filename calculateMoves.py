# CONSTANTS
#-----------------------------------------------------------------------------
BOARD_SIZE = 8

# CLASS DEFINITIONS BEGIN
#-----------------------------------------------------------------------------
class Movement:
    def __init__(self, state):
        self.state = state

    def updateState(self, newState):
        self.state = newState

    # returns list of possible moves
    def calcMovesForCoord(self, coord):
        i, j = coord
        return [x for x in [self.canGoRight_(i, j), self.canGoLeft_(i, j), self.canGoUp_(i, j), self.canGoDown_(i, j)] if x]

    # checks if cell is empty, that is it does not contain pieces or is not a corner.
    def isEmpty_(self, i, j):
        return (i, j) not in self.state.blackPieces and (i, j) not in self.state.whitePieces and not corner(i, j)

    # series of functions that checks if a piece can move or jump.
    # canGo functions check if the adjacent cell is empty and within bounds, then tries tso move.
    # if not empty, it is a piece or a corner. We then call canJump functions to see if
    # we can perform a jump, the target cell for jump is empty and within bounds.
    def canJumpRight_(self, i, j):
        return (i, j + 2) if withinBounds(i, j + 2) and self.isEmpty_(i, j + 2) else None

    def canJumpLeft_(self, i, j):
        return (i, j - 2) if withinBounds(i, j - 2) and self.isEmpty_(i, j - 2) else None

    def canJumpUp_(self, i, j):
        return (i - 2, j) if withinBounds(i - 2, j) and self.isEmpty_(i - 2, j) else None

    def canJumpDown_(self, i, j):
        return (i + 2, j) if withinBounds(i + 2, j) and self.isEmpty_(i + 2, j) else None

    def canGoRight_(self, i, j):
        return (i, j + 1) if withinBounds(i, j + 1) and self.isEmpty_(i, j + 1) else self.canJumpRight_(i, j)

    def canGoLeft_(self, i, j):
        return (i, j - 1) if withinBounds(i, j - 1) and self.isEmpty_(i, j - 1) else self.canJumpLeft_(i, j)

    def canGoUp_(self, i, j):
        return (i - 1, j) if withinBounds(i - 1, j) and self.isEmpty_(i - 1, j) else self.canJumpUp_(i, j)

    def canGoDown_(self, i, j):
        return (i + 1, j) if withinBounds(i + 1, j) and self.isEmpty_(i + 1, j) else self.canJumpDown_(i, j)


class GameState:
    #   sets of whitePieces and blackPieces
    #   list of prevMoves, construct from parent

    def __init__(self, whitePieces, blackPieces, prevMoves):
        self.whitePieces = whitePieces
        self.blackPieces = blackPieces
        self.prevMoves = prevMoves

    def __eq__(self, otherGameState):
        return (self.whitePieces == otherGameState.whitePieces
                and self.blackPieces == otherGameState.blackPieces)

    def updateSets(self, newWhiteSet, newBlackSet):
        self.whitePieces = newWhiteSet
        self.blackPieces = newBlackSet

#-----------------------------------------------------------------------------
# CLASS DEFINITIONS END.



# FUNCTION DEFINITIONS BEGIN
#-----------------------------------------------------------------------------
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
                whitePieces.add((i, j))
            elif char == '@':
                blackPieces.add((i, j))

    startState.updateSets(whitePieces, blackPieces)


# Function that calculates the total number of moves, then prints them to stdout
def calcTotalMoves():
    movementService = Movement(startState)

    whiteMoves = 0
    blackMoves = 0

    for whiteCoord in startState.whitePieces:
        whiteMoves += len(movementService.calcMovesForCoord(whiteCoord))
    for blackCoord in startState.blackPieces:
        blackMoves += len(movementService.calcMovesForCoord(blackCoord))

    print(whiteMoves)
    print(blackMoves)

def debugPrintState(state):
    print("the following is white pieces")
    print(state.whitePieces)
    print("the following is blackPieces")
    print(state.blackPieces)
    print("movelist")
    print(state.prevMoves)

def massacre(startState):
    # debug TODO
    #debugPrintState(startState)
    numWhite = len(startState.whitePieces)
    # set startState
    # visited = set(GameStates)
    visited = {startState}
    # to_visit stack = [startState]
    to_visit = [startState]
    # while to_visit:
    while to_visit:
        #   currentState = to_visit.pop() -- gets the head
        currentState = to_visit.pop()
        if massacreGoalCheck(currentState):
            # debugPrintState(currentState)
            print(currentState.prevMoves)
            return
        movementService = Movement(currentState)
        #   add currentState to visitedStates set()
        visited.add(currentState)
        #   generate childStates (by using calcMoves on each whitePiece)
        # For each whitepiece in the current state...
        # TODO debug
        #print("we started while loop")
        for whitePiece in currentState.whitePieces:
            # get all moves that piece can do, then for each move...
            moveList = movementService.calcMovesForCoord(whitePiece)
            for move in moveList:
                # generate the gamestate node that results from that move...
                # we need to generate new white set, black set, and update list of prevMoves, then
                # use those to create new gameState.

                newWhitePieces = currentState.whitePieces.copy()
                newBlackPieces = currentState.blackPieces.copy()
                newPrevMoves = currentState.prevMoves.copy()

                newWhitePieces.remove(whitePiece)
                newWhitePieces.add(move)
                newPrevMoves.append((whitePiece,move))

                # we then remove eaten black pieces. (white has priority)
                removeEatenPieces(newBlackPieces, newWhitePieces)
                # then we remove eaten white piecs.
                removeEatenPieces(newWhitePieces, newBlackPieces)

                newGameState = GameState(newWhitePieces, newBlackPieces, newPrevMoves)

                # we then check if number of whitepieces decreased. IF so, we do not add to to_visit set.
                # we do check if newnode is in visited state, if so we do not add to to_visit set.
                if (len(newGameState.whitePieces) == numWhite) and newGameState not in visited:
                    to_visit.append(newGameState)

    # return moveSequence (prettified)
    # do this by returning currentState.prevMoves

def isOpponent(opponentPieces, coordinate):
    i, j = coordinate
    return withinBounds(i, j) and coordinate in opponentPieces or corner(i, j)

def canEat(opponentPieces, side1, side2):
    return isOpponent(opponentPieces, side1) and opponentPieces(opponentPieces, side2)

def removeEatenPieces(ownPieces, opponentPieces):
    toRemove = []
    for piece in ownPieces:
        i,j = piece
        down = (i,j+1)
        up = (i,j-1)
        left = (i-1,j)
        right = (i+1,j)

        # check if piece can be eaten from up and down / left and right
        # by checking if within bounds and if they are corner or white.
        if canEat(opponentPieces, up, down) or canEat(opponentPieces, left, right):
            toRemove.append(piece)

    for pieceToRemove in toRemove:
        ownPieces.remove(pieceToRemove)
    return ownPieces

# Function to check if we are in a goal state for massacre
def massacreGoalCheck(gameState):
    # If the state we send has no black pieces, we are in goal state.
    return (len(gameState.blackPieces) == 0)

# Function to check if two states are equivalent in the game.
def checkEquivalent(state1,state2):
    return (state1.whitePieces == state2.whitePieces
            and state1.blackPieces == state2.blackPieces)


# FUNCTION DEFINITIONS END
#-----------------------------------------------------------------------------

startState = GameState(set(), set(), [])

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
