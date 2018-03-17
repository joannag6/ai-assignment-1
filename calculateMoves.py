BOARD_SIZE = 8

def corner(i, j):
    corner_coords = {0, BOARD_SIZE-1}
    return i in corner_coords and j in corner_coords

def withinBounds(i, j):
    return (0 <= i < BOARD_SIZE) and (0 <= j < BOARD_SIZE)

class GameState:
    #   sets of whitePieces and blackPieces
    #   list of prevMoves, construct from parent

    def __init__(self, whitePieces, blackPieces, prevMoves):
        self.whitePieces = whitePieces
        self.blackPieces = blackPieces
        self.prevMoves = prevMoves

    def updateSets(self, newWhiteSet, newBlackSet):
        self.whitePieces = newWhiteSet
        self.blackPieces = newBlackSet

    def isEqual(self, otherGameState):
        return self.whitePieces == otherGameState.whitePieces and self.blackPieces == otherGameState.blackPieces

    def isEmpty_(self, i, j):
        return (i, j) not in self.blackPieces and (i, j) not in self.whitePieces and not corner(i, j)

    def canJumpRight(self, i, j):
        return (i,j+2) if withinBounds(i,j+2) and self.isEmpty_(i,j+2) else None

    def canJumpLeft(self, i, j):
        return (i,j-2) if withinBounds(i,j-2) and self.isEmpty_(i,j-2) else None

    def canJumpUp(self, i, j):
        return (i-2,j) if withinBounds(i-2,j) and self.isEmpty_(i-2,j) else None

    def canJumpDown(self, i, j):
        return (i+2,j) if withinBounds(i+2,j) and self.isEmpty_(i+2,j) else None

    def canGoRight(self, i, j):
        return (i,j+1) if withinBounds(i,j+1) and self.isEmpty_(i,j+1) else self.canJumpRight(i,j)

    def canGoLeft(self, i, j):
        return (i,j-1) if withinBounds(i,j-1) and self.isEmpty_(i,j-1) else self.canJumpLeft(i,j)

    def canGoUp(self, i, j):
        return (i-1,j) if withinBounds(i-1,j) and self.isEmpty_(i-1,j) else self.canJumpUp(i,j)

    def canGoDown(self, i, j):
        return (i+1,j) if withinBounds(i+1,j) and self.isEmpty_(i+1,j) else self.canJumpDown(i,j)

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

def calcMovesForCoord(coord): # TODO(return list of possible moves)
    i, j = coord
    return [x for x in [startState.canGoRight(i, j), startState.canGoLeft(i, j), startState.canGoUp(i, j), startState.canGoDown(i, j)] if x]

# Function that calculates the total number of moves, then prints them to stdout
def calcTotalMoves():
    whiteMoves = 0
    blackMoves = 0

    #TODO(shouldn't need to pass in whiteMoves and blackMoves, might use class next time)
    for whiteCoord in startState.whitePieces:
        whiteMoves += len(calcMovesForCoord(whiteCoord))
    for blackCoord in startState.blackPieces:
        blackMoves += len(calcMovesForCoord(blackCoord))

    print(whiteMoves)
    print(blackMoves)

def massacre():
    # set startState
    # moveSequence stack [((x1, y1), (x2, y2))]
    # visited = set(GameStates)
    # to_visit stack = [startState]
    # while to_visit:
    #   currentState = to_visit.pop() -- gets the head
    #   add currentState to visitedStates set()
    #   generate childStates (by using calcMoves on each whitePiece)
    #       each move is a separate childState
    #   for each childState, check if any pieces got eaten - removeEatenPieces()
    #   if num(whitePieces) decreases, remove that childStates
    #   check if in visitedStates - remove childState
    #   check if GoalState (num(blackPieces) = 0)

    # return moveSequence (prettified)
    print('yay massacre')

startState = GameState(set(), set(), [])

setUpBoard()

# determine if it's "Moves" or "Massacre")
command = input()

if command == 'Moves':
    # calculate available moves for each player
    calcTotalMoves()
elif command == 'Massacre':
    # do massacre stuff
    massacre()
else:
    print("Please enter a valid command (ie. 'Moves', 'Massacre')")
