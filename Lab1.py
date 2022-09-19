# student name: Idil Bil

# A command-line Tic-Tac-Toe game 
from ast import Or
import random

board = [' '] * 9 # A list of 9 strings, one for each cell, 
                  # will contain ' ' or 'X' or 'O'
played = set()    # A set to keep track of the played cells 

def init() -> None:
    """ prints the banner messages 
        and prints the intial board on the screen
    """
    print("Welcome to Tic-Tac-Toe!")
    print("You play X (first move) and computer plays O.")
    print("Computer plays randomly, not strategically.")
    printBoard()

def printBoard() -> None:
    """ prints the board on the screen based on the values in the board list """
    print(board[0], "|", board[1], "|", board[2],"     ", "0 | 1 | 2")
    print("--+---+--", "     ", "--+---+--")
    print(board[3], "|", board[4], "|", board[5],"     ", "3 | 4 | 5")
    print("--+---+--", "     ", "--+---+--")
    print(board[6], "|", board[7], "|", board[8],"     ", "6 | 7 | 8")

def playerNextMove() -> None:
    """ prompts the player for a valid cell number, 
        and prints the info and the updated board;
        error checks that the input is a valid cell number 
    """
    try:                                                #runs if the type of the index is int
        idx = int(input("Next move for X (state a valid cell num):"))
        if idx < 0 or idx > 8:                          #checks if the index is inside the range
            print("Must enter a valid cell number")
            playerNextMove()
        elif board[idx] == 'X' or board[idx] == 'O':    #checks if that cell has been used before
            print("This cell has already been used")
            playerNextMove()
        else:                                           #if the chosen cell index is valid
            played.add(idx)                             #adds the valid cell index in the list of used ones
            board[idx] = 'X'                            #players move
            printBoard()
    except:                                             #if the index is not a valid integer
        print("Must be an integer")                 
        playerNextMove()

def computerNextMove() -> None:
    """ Computer randomly chooses a valid cell, 
        and prints the info and the updated board 
    """
    num = int((random.randint(0, 8)))               #computer chooses a random number
    while (num in played):                          #checks if that cell has been used
            num = int((random.randint(0, 8)))       #if it was chooses another random number
    played.add(num)                                 #adds the valid cell number in the list of used ones
    board[num] = 'O'                                #computers move
    printBoard()

def hasWon(who: str) -> bool:
    """ returns True if who (being passed 'X' or 'O') has won, False otherwise """
    if who == board[0] == board[1] == board[2]  or who == board[3] == board[4] == board[5] or who == board[6] == board[7] == board[8] or who == board[0] == board[3] == board[6] or who == board[1] == board[4] == board[7] or who == board[2] == board[5] == board[8] or who == board[0] == board[4] == board[8] or who == board[2] == board[4] == board[6]:
        #checks all the winning conditions
        return True 
    else:
        return False

def terminate(who: str) -> bool:
    """ returns True if who (being passed 'X' or 'O') has won or if it's a draw, False otherwise;
        it also prints the final messages:
                "You won! Thanks for playing." or 
                "You lost! Thanks for playing." or 
                "A draw! Thanks for playing."  
    """
    if hasWon(who) and who == 'X':                  #player won
        print("You won! Thanks for playing.")
        return True
    elif hasWon(who) and who == 'O':                #computer won
        print("You lost! Thanks for playing.")
        return True
    elif not hasWon(who) and len(played) == 9:      #no one won and the board is full (draw)
        print("A draw! Thanks for playing.")
        return True
    else:
        return False

if __name__ == "__main__":
    # Use as is. 
    init()
    while True:
        playerNextMove()            # X starts first
        if(terminate('X')): break   # if X won or a draw, print message and terminate
        computerNextMove()          # computer plays O
        if(terminate('O')): break   # if O won or a draw, print message and terminate
