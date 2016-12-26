game = __import__("2048")
from copy import deepcopy
from math import log


## Verbose play function
## When called, prints every board state with score and moves
def play():
    board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    game.newTile(board)
    game.newTile(board)
    print(game.string(board))
    moves = 0
    while True:
        new_board = aimove(board)
        if (new_board == board):
            print(game.string(board))
            print("Final Score: " + str(game.score(board)))
            print("Total Moves: " + str(moves))
            break
        else:
            board = new_board
            game.newTile(board)
            print(game.string(board))
            moves += 1
            print("Score: " + str(game.score(board)))
            print("Moves: " + str(moves))

## Concise play function
## returns list of stats of that runthrough
def aiplay():
    board = [[0,0,0,0],
             [0,0,0,0],
             [0,0,0,0],
             [0,0,0,0]]
             game.newTile(board)
             game.newTile(board)
             moves = 0
             stats = []
             while True:
                 new_board = aimove(board)
                     if (new_board != board):
                         board = new_board
                             game.newTile(board)
                                 moves += 1
                                     else:
                                         break
                                     stats.append(game.score(board))
stats.append(game.maxNumber(board))
    stats.append(moves)
    stats.append(board)
    return stats

## Looping function for data collection
## prints the score, max tile, number of moves, and the final board for each game
def looper():
    maxes = []
    for i in range(0,10):
        list_of_stats = aiplay()
        ## print("Run Number: " + str(i))
        ##print("Final Score: " + str(list_of_stats[0]))
        ##print("Max Tile: " + str(list_of_stats[1]))
        print("Number of Moves: " + str(list_of_stats[2]))
        maxes.append(list_of_stats[1])
        print("Final Board: " + '\n' + game.string(list_of_stats[3]))
    print(maxes)

## Second heuristic used
## Awards points for every tile
## Penalizes the difference between every pair of adjacent boards
## Awards points for every empty tile
def heurV2(board):
    total = 0
    penalty = 0
    zeroes = 0
    maxValue = 0
    for i in range(0,4):
        for j in range(0,4):
            curr = board[i][j]
            total += curr
            if (curr > maxValue):
                maxValue = curr
            if (curr == 0):
                zeroes += 1
            if (j < 3):
                penalty += abs(curr - board[i][j+1])
            if (i < 3):
                penalty += abs(curr - board[i+1][j])
    zeroCalc = maxValue / 2.0 * zeroes / 14.0
    return ((total + zeroCalc) * 2 - penalty)

## First heuristic used
## Adds the score of zero tiles
## and the score of identical adjacent tiles
def heurV1(board):
    tileWeight = 1
    equalAdjacencyWeight = 1
    return ((number_of_zero_tiles(board) * tileWeight) +
            (equal_adjacent(board) * equalAdjacencyWeight))

## Compares for equality the tiles blow and to the right of the current
def compare_right_down(board, i, j):
    score = 0
    if (board[i][j] == 0):
        return 0
    else:
        if (board[i][j] == board[i+1][j] or
            board[i][j] == (board[i+1][j] / 2)):
            score +=1
            if (board[i][j] == board[i][j+1] or
                board[i][j] == (board[i][j+1] / 2)):
            score +=1
    return score

## Compares for equality the tile below the current
def compare_down(board, i, j):
    score = 0
    if (board[i][j] == 0):
        return 0
    else:
        if (board[i][j] == board[i+1][j] or
            board[i][j] == (board[i+1][j] / 2)):
            score +=1
    return score

## Compares for equality the tile to the right of the current
def compare_right(board, i, j):
    score = 0
    if (board[i][j] == 0):
        return 0
    else:
        if (board[i][j] == board[i][j+1] or
            board[i][j] == (board[i][j+1] / 2)):
            score +=1
    return score


## returns a value to represent the total tiles next
## to merge-able tiles
def equal_adjacent(board):
    running_total = 0
    for i in range(0,4):
        for j in range(0,4):
            if (i == 3 and j == 3):
                return running_total / 24.0
            elif (j == 3):
                running_total = running_total + compare_down(board, i, j)
            elif (i == 3):
                running_total = running_total + compare_right(board, i, j)
            else:
                running_total = running_total + compare_right_down(board, i, j)


## returns the number of zeroes
def number_of_zero_tiles(board):
    total = 0
    for i in range(0, 4):
        for j in range(0, 4):
            if (board[i][j] == 0):
                total +=1
    total = total / 16.0
    return total

## number of tiles on board
## allows for variable limit if desired
def number_of_tiles(board):
    total = 0
    output = 0
    for i in range(0, 4):
        for j in range(0, 4):
            if (board[i][j] != 0):
                total +=1
    if (total <= 16 and total >= 12):
        output = 10
    return output / 10.0

## Returns the next best board state from the moves possible
## from the given board
def aimove(board):
    a = 0
    moves = []
    values = []
    moves.append(game.left(board))
    moves.append(game.right(board))
    moves.append(game.up(board))
    moves.append(game.down(board))
    limit = 0
    ## if limit is set to zero, below can be used for a variable limit
    ## ex. searching farther if less moves are possible or less empty spaces are available
    
    if (number_of_tiles(board) == 1):
        limit = 4
    else:
        limit = 3
    
    for move in moves:
        if (move != board):
            a = expectimax(move, limit, False)
            values.append(a)
        else:
            values.append(float("-inf"))
    ##for num in values:
    ##print(num)
a = max(values)
    position = 0
    for i in range(0, len(values)):
        if (values[i] == a):
            position = i
            break
return moves[position]

## expectimax that follows the simple pseudocode from wikipedia
def expectimax(board, limit, player):
    a = 0
    if (limit == 0):
        return heurV2(board)
    elif (game.gameOver(board)):
        return -10000
    elif (player == True):
        a = float("-inf")
        moves = []
        moves.append(game.left(board))
        moves.append(game.right(board))
        moves.append(game.up(board))
        moves.append(game.down(board))
        for move in moves:
            if (move != board):
                a = max(a, expectimax(move, limit - 1, False))
    elif (player == False):
        a = 0
        spots = game.validSpawns(board)
        probability = 1 / len(spots)
        twoProb = probability * .9
        fourProb = probability * .1
        boards = []
        newBoard = deepcopy(board)
        for position in spots:
            ## could attempt some semblance of pruning from low probability board states
            ##if (twoProb > (1/200)):
            newBoard[position[0]][position[1]] = 2
                a += (probability * .9 * expectimax(newBoard, limit - 1, True))
                ##if (fourProb > (1/200)):
                newBoard[position[0]][position[1]] = 4
                a += (probability * .1 * expectimax(newBoard, limit - 1, True))
                newBoard[position[0]][position[1]] = 0
    return a

""" Uncomment for a verbose instance of the ai """         
play()
""" Uncomment for a set of concise info of multiple ai runs """
##looper()
