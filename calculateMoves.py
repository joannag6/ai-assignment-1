BOARD_SIZE = 8
blackPieces = set() 
whitePieces = set()
whiteMoves = 0
blackMoves = 0

def corner(i, j):
    corner_coords = {0, BOARD_SIZE-1}
    return i in corner_coords and j in corner_coords

def isEmpty(i, j):
    return (i, j) not in blackPieces and (i, j) not in whitePieces and not corner(i, j)

def withinBounds(i, j):
    return (0 <= i < BOARD_SIZE) and (0 <= j < BOARD_SIZE)

def canJumpRight(i, j):
    return (i,j+2) if withinBounds(i,j+2) and isEmpty(i,j+2) else None

def canJumpLeft(i, j):
    return (i,j-2) if withinBounds(i,j-2) and isEmpty(i,j-2) else None

def canJumpUp(i, j):
    return (i-2,j) if withinBounds(i-2,j) and isEmpty(i-2,j) else None

def canJumpDown(i, j):
    return (i+2,j) if withinBounds(i+2,j) and isEmpty(i+2,j) else None

def canGoRight(i, j):
    return (i, j+1) if withinBounds(i,j+1) and isEmpty(i,j+1) else canJumpRight(i, j)

def canGoLeft(i, j):
    return (i,j-1) if withinBounds(i,j-1) and isEmpty(i,j-1) else canJumpLeft(i, j)

def canGoUp(i, j):
    return (i-1,j) if withinBounds(i-1,j) and isEmpty(i-1,j) else canJumpUp(i, j)

def canGoDown(i, j):
    return (i+1,j) if withinBounds(i+1,j) and isEmpty(i+1,j) else canJumpDown(i, j)

def calcMoves(coord): # TODO(return list of possible moves)
    i, j = coord
    return [x for x in [canGoRight(i, j), canGoLeft(i, j), canGoUp(i, j), canGoDown(i, j)] if x]

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

print(whitePieces, blackPieces)

# determine if it's "Moves" or "Massacre")
command = input()

if command == 'Moves':
    for whiteCoord in whitePieces:
        whiteMoves += len(calcMoves(whiteCoord))
    for blackCoord in blackPieces:
        blackMoves += len(calcMoves(blackCoord))

    print(whiteMoves)
    print(blackMoves)
elif command == 'Massacre':
    # do massacre stuff
    print('massacre')
else:
    print("Please enter a valid command (ie. 'Moves', 'Massacre')")
