BOARD_SIZE = 8

# CLASS DEFINITIONS BEGIN
#--------------------------------------------------------------------------------------------------------------------------------
def corner(i, j):
    corner_coords = {0, BOARD_SIZE - 1}
    return i in corner_coords and j in corner_coords


def withinBounds(i, j):
    return (0 <= i < BOARD_SIZE) and (0 <= j < BOARD_SIZE)

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

    def updateSets(self, newWhiteSet, newBlackSet):
        self.whitePieces = newWhiteSet
        self.blackPieces = newBlackSet

    def isEqual(self, otherGameState):
        return self.whitePieces == otherGameState.whitePieces and self.blackPieces == otherGameState.blackPieces    
    
#--------------------------------------------------------------------------------------------------------------------------------
# CLASS DEFINITIONS END. 



# FUNCTION DEFINITIONS BEGIN
#--------------------------------------------------------------------------------------------------------------------------------
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

    # TODO(shouldn't need to pass in whiteMoves and blackMoves, might use class next time)
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
    i = 0
    if massacreGoalCheck(startState):
        print(startState.prevMoves)
        return
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
        i+=1
        #   currentState = to_visit.pop() -- gets the head
        currentState = to_visit.pop()
        print("we popped")
        if massacreGoalCheck(currentState):
            debugPrintState(currentState)
            print(currentState.prevMoves)
            return
        #TODO
        #if i<3:
        #    debugPrintState(currentState)
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
                    #TODO: only doing this bcz idk if newWhitePieces == currentState.whitePieces is gonna create new variable or just point to currentState.whitePieces

                    newWhitePieces = set()
                    newBlackPieces = set()     
                    newPrevMoves = []
                    for w in currentState.whitePieces:
                        newWhitePieces.add(w)
                    for b in currentState.blackPieces:
                        newBlackPieces.add(b)
                    for m in currentState.prevMoves:
                        newPrevMoves.add(m)
                        # TODO need to change this to be same format as in spec
                        # TODO Currently it is a tuple of tuples. Maybe make it string?
                        newPrevMoves.add((whitePiece,move))

                    newWhitePieces.remove(whitePiece)
                    newWhitePieces.add(move)
                    newGameState = GameState(newWhitePieces, newBlackPieces, newPrevMoves)

                    # we then remove eaten black pieces.
                    removeEatenBlackPieces(newGameState)
                    # then we remove eaten white piecs. 
                    removeEatenWhitePieces(newGameState)
                    # we then check if number of whitepieces decreased. IF so, we do not add to to_visit set.
                    # we do check if newnode is in visited state, if so we do not add to to_visit set.
                    duplicate = 0
                    for visitedNodes in visited:
                        if(checkEquivalent(newGameState,visitedNodes)):
                            duplicate = 1
                    if (len(newGameState.whitePieces) == numWhite) and duplicate == 0:
                        to_visit.append(newGameState) 
    
        #todo debug 
        #print("we reached end of while loop")
        #   check if GoalState (num(blackPieces) = 0)
        
    # return moveSequence (prettified)
    # do this by returning currentState.prevMoves

# Function that takes in a game state that calculates which black pieces die given white has eating priority
def removeEatenBlackPieces(gameState):
    toRemove = []
    for blackPiece in gameState.blackPieces:
        # TODO: might wanna fix the way we handled corner and withinBounds function so that this can be cleaner? 
        i,j = blackPiece
        downi,downj = (i,j+1)
        down = downi,downj
        upi,upj = (i,j-1)
        up = upi,upj
        lefti,leftj = (i-1,j)
        left = lefti,leftj
        righti,rightj = (i+1,j)
        right = righti,rightj

        # check if piece can be eaten from up and down. 
        # if piece up and down are within bounds, check if piece up and down are corner or white.
        if ((up in gameState.whitePieces) or corner(upi,upj)) and ( (down in gameState.whitePieces) or corner(downi,downj)) :
            #print("debug1")
            toRemove.append(blackPiece)
        # check if piece can be eaten from left and right. 
        if ((left in gameState.whitePieces) or corner(lefti,leftj)) and ( (right in gameState.whitePieces) or (corner(righti,rightj)) ):
            #print("debug2")
            toRemove.append(blackPiece)

    for pieceToRemove in toRemove:
        gameState.blackPieces.remove(pieceToRemove)

# Function that takes in a game state that calculates which black pieces die given white has eating priority
def removeEatenWhitePieces(gameState):
    toRemove = []
    for whitePiece in gameState.whitePieces:
        # TODO: might wanna fix the way we handled corner and withinBounds function so that this can be cleaner? 
        i,j = whitePiece
        downi,downj = (i+1,j)
        down = downi,downj
        upi,upj = (i-1,j)
        up = upi,upj
        lefti,leftj = (i,j-1)
        left = lefti,leftj
        righti,rightj = (i,j+1)
        right = righti,rightj

        # check if piece can be eaten from up and down. 
        # if piece up and down are within bounds, check if piece up and down are corner or white.
        if (withinBounds(upi,upj) and withinBounds(downi,downj)) and (((up in gameState.blackPieces) or corner(upi,upj)) and ((down in gameState.blackPieces) or (corner(downi,downj))) ):
            #print("debug3")
            toRemove.append(whitePiece)

        # check if piece can be eaten from left and right. 
        if (withinBounds(lefti,leftj) and withinBounds(righti,rightj)) and (((left in gameState.blackPieces) or corner(lefti,leftj)) and ((right in gameState.blackPieces) or (corner(righti,rightj))) ):
            #print("debug4")
            toRemove.append(whitePiece)

    for pieceToRemove in toRemove:
        gameState.whitePieces.remove(pieceToRemove)



# Function to check if we are in a goal state for massacre
def massacreGoalCheck(gameState):
    # If the state we send has no black pieces, we are in goal state. 
    return (len(gameState.blackPieces) == 0)
    
# Function to check if two states are equivalent in the game. 
def checkEquivalent(state1,state2):
    return state1.whitePieces == state2.whitePieces and state1.blackPieces == state2.blackPieces


# FUNCTION DEFINITIONS END
#--------------------------------------------------------------------------------------------------------------------------------

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