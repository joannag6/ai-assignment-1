board = [] # 2D array accessible by coordinates
whiteMoves = 0
blackMoves = 0

def isEmpty(i, j):
    return board[i][j] == '-'

def withinBounds(i, j):
    return (0 <= i <= len(board)-1) and (0 <= j <= len(board)-1)

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

def calcMoves(i, j): # TODO(return list of possible moves)
    return [x for x in [canGoRight(i, j), canGoLeft(i, j), canGoUp(i, j), canGoDown(i, j)] if x]

# read from input and generate board
for i in range(8):
    # add row to board
    board.append(input().split())

# print(board)

# determine if it's "Moves" or "Massacre")
command = input()

if command == 'Moves':
    for i in range(8):
        for j in range(8):
            currentchar = board[i][j]
            if currentchar == 'O':
                whiteMoves += len(calcMoves(i, j))
            elif currentchar == '@':
                blackMoves += len(calcMoves(i, j))

    print(whiteMoves)
    print(blackMoves)
elif command == 'Massacre':
    # do massacre stuff
    print('massacre')
else:
    print("Please enter a valid command (ie. 'Moves', 'Massacre')")
