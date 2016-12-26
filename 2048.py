from copy import deepcopy
from random import randint
from math import log

## A Board is a list of lists of numbers
"""
    Example:     [[0,1,2,3],
    [4,5,6,7],
    [8,9,0,1],
    [2,3,4,5]]
    
    """


## Returns a list of tuples (i,j)
## where each represents position of an open space on a board
def validSpawns(board):
    spots = []
    for i in range(0,4):
        for j in range(0,4):
            if (board[i][j] == 0):
                spots.append((i,j))
    return spots

## Returns the maximum tile value of a board
def maxNumber(board):
    maxValue = 0
    for row in board:
        for elem in row:
            if (elem > maxValue):
                maxValue = elem
    return maxValue


## returns a string version of the 2D array to be pretty printed
def string(board):
    maxStringLength = len(str(maxNumber(board)))
    output = ("-" * 5) + ("-" * 4 * maxStringLength) + '\n'
    for i in range(0,4):
        output = output + "|"
        for j in range(0,4):
            spaces = maxStringLength - len(str(board[i][j]))
            output = output + (" " * spaces) + str(board[i][j]) + "|"
        output = output + '\n'
    output = output + ("-" * 5) + ("-" * 4 * maxStringLength)
    return output

## returns the score of the board as we understood it
## for every tile, multiply it's value by one less than
## lg of that tile. Sum and return
## Example: tile of 32 = 2^5. Score of that tile is: (5 - 1)*32
def score(board):
    score = 0
    for i in range(0,4):
        for j in range(0,4):
            if (board[i][j] != 0):
                power = log(board[i][j], 2)
                score = score + ((power - 1) * board[i][j])
    return score


## Spawns a new tile
def newTile(board):
    spots = validSpawns(board)
    if (spots != None):
        ## tile with value 2 has 90% chance of spawning, while tile with value 4 has 10%
        if (randint(0, 9) == 0):
            tileType = 4
        else:
            tileType = 2
        ## selects a random tile location from the spots (available) list
        tileLocation = randint(0, len(spots) - 1)
        i = spots[tileLocation][0]
        j = spots[tileLocation][1]
        ## putting the new tile in the correct location
        board[i][j] = tileType


## End game condition
def gameOver(board):
    spots = validSpawns(board)
    ## if there are no more spots available, ends game
    if not spots:
        boardLeft = left(board)
        boardRight = right(board)
        boardUp = up(board)
        boardDown = down(board)
        ## see if all the board states from moving are the same as the original board
        if all(x == board for x in (boardLeft, boardRight, boardUp, boardDown)):
            return True
        else:
            return False
    else:
        return False


## Transposes along diagonal
"""
    Example:    | 1 2 3 4 |    | 1 5 9 3 |
    | 5 6 7 8 | -> | 2 6 0 4 |
    | 9 0 1 2 |    | 3 7 1 5 |
    | 3 4 5 6 |    | 4 8 2 6 |
    """
def transpose(board):
    board = [list(i) for i in zip(*board)]
    return board


## Axis as 1 or 3 pushes all to left
## Axis as 2 or 4 pushes all to right
def shift(board, axis):
    second = []
    for i in range(0,4):
        memory = []
        for item in board[i]:
            memory.append(item)
        if axis == 3 or axis == 1:
            memory.sort(key=bool, reverse=True)
        else:
            memory.sort(key=bool)
        second.append(memory)
    return second


## Merges all identical values towards the left
## while iterating from the left
def mergeLeft(board):
    row1 = board[0]
    row2 = board[1]
    row3 = board[2]
    row4 = board[3]
    memory = []
    pos = 0
    while pos < 3:
        pos2 = pos + 1
        if row1[pos] == row1[pos2]:
            row1[pos] = row1[pos] * 2
            row1[pos2] = 0
        if row2[pos] == row2[pos2]:
            row2[pos] = row2[pos] * 2
            row2[pos2] = 0
        if row3[pos] == row3[pos2]:
            row3[pos] = row3[pos] * 2
            row3[pos2] = 0
        if row4[pos] == row4[pos2]:
            row4[pos] = row4[pos] * 2
            row4[pos2] = 0
        pos += 1
    memory.append(row1)
    memory.append(row2)
    memory.append(row3)
    memory.append(row4)
    return memory

## Merges all identical tiles towards the right
## iterating from the right
def mergeRight(board):
    row1 = board[0]
    row2 = board[1]
    row3 = board[2]
    row4 = board[3]
    memory = []
    pos = 3
    while pos > 0:
        pos2 = pos - 1
        if row1[pos] == row1[pos2]:
            row1[pos] = row1[pos] * 2
            row1[pos2] = 0
        if row2[pos] == row2[pos2]:
            row2[pos] = row2[pos] * 2
            row2[pos2] = 0
        if row3[pos] == row3[pos2]:
            row3[pos] = row3[pos] * 2
            row3[pos2] = 0
        if row4[pos] == row4[pos2]:
            row4[pos] = row4[pos] * 2
            row4[pos2] = 0
        pos -= 1
    memory.append(row1)
    memory.append(row2)
    memory.append(row3)
    memory.append(row4)
    return memory

## Movement functions: left, right, up, down
def left(board):
    memory = deepcopy(board)
    memory = shift(memory, 1)
    memory = mergeLeft(memory)
    memory = shift(memory, 1)
    return memory


def right(board):
    memory = deepcopy(board)
    memory = shift(memory, 2)
    memory = mergeRight(memory)
    memory = shift(memory, 2)
    return memory


def up(board):
    memory = deepcopy(board)
    memory = transpose(memory)
    memory = left(memory)
    memory = transpose(memory)
    return memory


def down(board):
    memory = deepcopy(board)
    memory = transpose(memory)
    memory = right(memory)
    memory = transpose(memory)
    return memory


def play():
    ## Board initialization
    board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    newTile(board)
    newTile(board)
    print(string(board))
    
    while True:
        move = int(input("8 - up, 4 - left, 5 - down, 6 - right, 0 - quit\n"))
        newBoard = []
        if (move == 8):
            newBoard = up(board)
        elif (move == 4):
            newBoard = left(board)
        elif (move == 5):
            newBoard = down(board)
        elif (move == 6):
            newBoard = right(board)
        else:
            print(string(board))
            print("Final score: " + str(score(board)))
            print("Largest tile: " + str(maxNumber(board)))
            break
        if (newBoard != board):
            newTile(newBoard)
            board = newBoard
        print(string(board))
        print("Current score: " + str(score(board)))
        if (gameOver(board)):
            print(string(board))
            print("Final score: " + str(score(board)))
            print("Largest tile: " + str(maxNumber(board)))
            break


""" Uncomment this to play """
##play()
