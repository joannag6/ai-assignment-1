board = [] # 2D array accessible by coordinates
whiteMoves = 0
blackMoves = 0

def isEmpty(i, j):
    return board[i][j] == '-'

def outOfBounds(i, j):
    return not ((0 <= i <= len(board)-1) and (0 <= j <= len(board)-1))

def canJumpRight(i, j):
    return not outOfBounds(i,j+2) and isEmpty(i,j+2)

def canJumpLeft(i, j):
    return not outOfBounds(i,j-2) and isEmpty(i,j-2)

def canJumpUp(i, j):
    return not outOfBounds(i-2,j) and isEmpty(i-2,j)

def canJumpDown(i, j):
    return not outOfBounds(i+2,j) and isEmpty(i+2,j)

def canGoRight(i, j):
    return (not outOfBounds(i,j+1) and isEmpty(i,j+1)) or canJumpRight(i, j)

def canGoLeft(i, j):
    return (not outOfBounds(i,j-1) and isEmpty(i,j-1)) or canJumpLeft(i, j)

def canGoUp(i, j):
    return (not outOfBounds(i-1,j) and isEmpty(i-1,j)) or canJumpUp(i, j)

def canGoDown(i, j):
    return (not outOfBounds(i+1,j) and isEmpty(i+1,j)) or canJumpDown(i, j)

def calcMoves(i, j):
    return canGoRight(i, j) + canGoLeft(i, j) + canGoUp(i, j) + canGoDown(i, j)

# read from input and generate board
for i in range(8):
    # add row to board
    board.append(input().split())

# print(board)

# determine if it's "Moves" or "Massacre")
command = input()

for i in range(8):
    for j in range(8):
        currentchar = board[i][j]
        if currentchar == 'O':
            whiteMoves += calcMoves(i, j)
        elif currentchar == '@':
            blackMoves += calcMoves(i, j)

print(whiteMoves)
print(blackMoves)
