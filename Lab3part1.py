#student name:      Idil Bil

def checkColumn(puzzle: list, column: int):
    """ 
        param puzzle: a list of lists containing the puzzle 
        param column: the column to check (a value between 0 to 8)

        This function checks the indicated column of the puzzle, and 
        prints whether it is valid or not. 
        
        As usual, this function must not mutate puzzle 
    """  
    valid_integers = [1, 2, 3, 4, 5, 6, 7, 8, 9]                                    #list created to check if the inputs could exist in sudoku
    SIZE = 9                                
    used = set()                                                                    #a set named "used" is initialized to represent each column
    for row in range(SIZE):                                                         #for loop to check each list inside the list "puzzle"
        used.add(puzzle[row][column])                                               #adds each used integer to the set "used"
    if len(used) == SIZE and all(elements in used for elements in valid_integers):  #checks if everything in the set is unique and valid for sudoku
        print("Column " + str(column) + " valid")       
    else:
        print("Column " + str(column) + " not valid")        
        
def checkRow(puzzle: list, row: int):
    """ 
        param puzzle: a list of lists containing the puzzle 
        param row: the row to check (a value between 0 to 8)

        This function checks the indicated row of the puzzle, and 
        prints whether it is valid or not. 
        
        As usual, this function must not mutate puzzle 
    """
    valid_integers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if len(puzzle[row]) == len(set(puzzle[row])) and all(elements in puzzle[row] for elements in valid_integers):   
        #checks if every integer inside a row is unique and valid for sudoku
        print("Row " + str(row) + " valid") 
    else:
        print("Row " + str(row) + " not valid")

def checkSubgrid(puzzle: list, subgrid: int):
    """ 
        param puzzle: a list of lists containing the puzzle 
        param subgrid: the subgrid to check (a value between 0 to 8)
        Subgrid numbering order:    0 1 2
                                    3 4 5
                                    6 7 8
        where each subgrid itself is a 3x3 portion of the original list
        
        This function checks the indicated subgrid of the puzzle, and 
        prints whether it is valid or not. 
        
        As usual, this function must not mutate puzzle 
    """
    valid_integers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    #gridnumber is defined as a list that includes the subgrid lists
    gridnumber = [  [puzzle[0][0], puzzle[0][1], puzzle[0][2], puzzle[1][0], puzzle[1][1], puzzle[1][2], puzzle[2][0], puzzle[2][1], puzzle[2][2]],
                    [puzzle[0][3], puzzle[0][4], puzzle[0][5], puzzle[1][3], puzzle[1][4], puzzle[1][5], puzzle[2][3], puzzle[2][4], puzzle[2][5]],
                    [puzzle[0][6], puzzle[0][7], puzzle[0][8], puzzle[1][6], puzzle[1][7], puzzle[1][8], puzzle[2][6], puzzle[2][7], puzzle[2][8]],
                    [puzzle[3][0], puzzle[3][1], puzzle[3][2], puzzle[4][0], puzzle[4][1], puzzle[4][2], puzzle[5][0], puzzle[5][1], puzzle[5][2]],
                    [puzzle[3][3], puzzle[3][4], puzzle[3][5], puzzle[4][3], puzzle[4][4], puzzle[4][5], puzzle[5][3], puzzle[5][4], puzzle[5][5]],
                    [puzzle[3][6], puzzle[3][7], puzzle[3][8], puzzle[4][6], puzzle[4][7], puzzle[4][8], puzzle[5][6], puzzle[5][7], puzzle[5][8]],
                    [puzzle[6][0], puzzle[6][1], puzzle[6][2], puzzle[7][0], puzzle[7][1], puzzle[7][2], puzzle[8][0], puzzle[8][1], puzzle[8][2]],
                    [puzzle[6][3], puzzle[6][4], puzzle[6][5], puzzle[7][3], puzzle[7][4], puzzle[7][5], puzzle[8][3], puzzle[8][4], puzzle[8][5]],
                    [puzzle[6][6], puzzle[6][7], puzzle[6][8], puzzle[7][6], puzzle[7][7], puzzle[7][8], puzzle[8][6], puzzle[8][7], puzzle[8][8]],
                ]
    if len(gridnumber[subgrid]) == len(set(gridnumber[subgrid])) and all(elements in gridnumber[subgrid] for elements in valid_integers):   
        #checks if every integer inside a subgrid is unique and valid for sudoku
        print("Subgrid " + str(subgrid) + " valid") 
    else:
        print("Subgrid " + str(subgrid) + " not valid")

if __name__ == "__main__":
    test1 = [ [6, 2, 4, 5, 3, 9, 1, 8, 7],      #all should be valid
              [5, 1, 9, 7, 2, 8, 6, 3, 4],
              [8, 3, 7, 6, 1, 4, 2, 9, 5],
              [1, 4, 3, 8, 6, 5, 7, 2, 9],
              [9, 5, 8, 2, 4, 7, 3, 6, 1],
              [7, 6, 2, 3, 9, 1, 4, 5, 8],
              [3, 7, 1, 9, 5, 6, 8, 4, 2],
              [4, 9, 6, 1, 8, 2, 5, 7, 3],
              [2, 8, 5, 4, 7, 3, 9, 1, 6]
            ]
    test2 = [ [6, 2, 4, 5, 3, 9, 1, 8, 7],      #only rows and subgrids should be valid
              [5, 1, 9, 7, 2, 8, 6, 3, 4],
              [8, 3, 7, 6, 1, 4, 2, 9, 5],
              [6, 2, 4, 5, 3, 9, 1, 8, 7],
              [5, 1, 9, 7, 2, 8, 6, 3, 4],
              [8, 3, 7, 6, 1, 4, 2, 9, 5],
              [6, 2, 4, 5, 3, 9, 1, 8, 7],
              [5, 1, 9, 7, 2, 8, 6, 3, 4],
              [8, 3, 7, 6, 1, 4, 2, 9, 5]
            ]
    test3 = [ [1, 1, 1, 1, 1, 1, 1, 1, 1],      #only columns should be valid
              [2, 2, 2, 2, 2, 2, 2, 2, 2],
              [3, 3, 3, 3, 3, 3, 3, 3, 3],
              [4, 4, 4, 4, 4, 4, 4, 4, 4],
              [5, 5, 5, 5, 5, 5, 5, 5, 5],
              [6, 6, 6, 6, 6, 6, 6, 6, 6],
              [7, 7, 7, 7, 7, 7, 7, 7, 7],
              [8, 8, 8, 8, 8, 8, 8, 8, 8],
              [9, 9, 9, 9, 9, 9, 9, 9, 9]
            ]
    test4 = [ [10, 2, 4, 5, 3, 9, 1, 8, 7],     #all except row 0, column 0 and subgrid 0 should be valid
              [5, 1, 9, 7, 2, 8, 6, 3, 4],
              [8, 3, 7, 6, 1, 4, 2, 9, 5],
              [1, 4, 3, 8, 6, 5, 7, 2, 9],
              [9, 5, 8, 2, 4, 7, 3, 6, 1],
              [7, 6, 2, 3, 9, 1, 4, 5, 8],
              [3, 7, 1, 9, 5, 6, 8, 4, 2],
              [4, 9, 6, 1, 8, 2, 5, 7, 3],
              [2, 8, 5, 4, 7, 3, 9, 1, 6]
            ]
    
    testcase = test1   #modify here for other testcases

    SIZE = 9

    for col in range(SIZE):         #checking all columns
        checkColumn(testcase, col)
    for row in range(SIZE):         #checking all rows
        checkRow(testcase, row)
    for subgrid in range(SIZE):     #checking all subgrids
        checkSubgrid(testcase, subgrid)
