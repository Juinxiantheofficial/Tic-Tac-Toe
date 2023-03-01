import random
import math
import numpy as np 

def check_move(board, turn, col, pop):    
    row = int(len(board)/7)
    
    #When player doesn't choose to pop
    if pop == False:
        #check if the selected index is empty
        if board[7*(row-1) + col] != 0:
            return False

    #When player choose to pop
    elif pop == True:
        #check if the number at the index is the player's number
        if board[col] != turn:
            return False
             
    return True 

def apply_move(board, turn, col, pop):
    row = int(len(board)/7)
    new_board = board.copy()
    empty_row = -1

    #Assigning the updated index into the array
    if pop == True:
        for i in range(row-1):
            new_board[7*i+col] = board[7*(i+1)+col]
        new_board[7*(row-1)+col] = 0
    
    #Add the respective player's number into the selected index in the array 
    elif pop == False:
        for i in range(row):
            if new_board[7*i+col] == 0:  #Assigning only if the index is empty
                empty_row = i
                break
        new_board[7*empty_row+col] = turn  #Update the board with player's move
    
    return new_board

def check_victory(board, who_played):
    row = int(len(board)/7)
    winner = 0
    next_who_played = 0

    if who_played == 1:
        next_who_played = 2
    else:
        next_who_played = 1

    #Check horizontal win
    for r in range(row):
        for c in range (4):
            if board[7*r+c] == board[7*r+c+1] == board[7*r+c+2] == board[7*r+c+3] == who_played:
                winner = 1
    
    #Check vertical win
    for c in range(7):
        for r in range (row-3):
            if board[7*r+c] == board[7*(r+1)+c] == board[7*(r+2)+c] == board[7*(r+3)+c] == who_played:
                winner = 1
    
    #Check positive diagonal win
    for r in range(row-3):
        for c in range (4):
            if board[7*r+c] == board[7*(r+1)+c+1] == board[7*(r+2)+c+2] == board[7*(r+3)+c+3] == who_played: 
                winner = 1

    #Check negative diagonal win
    for r in range(row-3):
        for c in range (4):
            if board[7*(r+3)+c] == board[7*(r+2)+c+1] == board[7*(r+1)+c+2] == board[7*(r)+c+3] == who_played: 
                winner = 1

    """"" This section begins to check if the opponnent consist of 4 consecutive discs when pop move was done by the previous player [Test Case 4] """
    #Check horizontal win (opponent)
    for r in range(row):    
        for c in range (4):
            if board[7*r+c] == board[7*r+c+1] == board[7*r+c+2] == board[7*r+c+3] == next_who_played:
                winner = 2
    
    #Check vertical win (opponent)
    for c in range(7):
        for r in range (row-3):
            if board[7*r+c] == board[7*(r+1)+c] == board[7*(r+2)+c] == board[7*(r+3)+c] == next_who_played:
                winner = 2
    
    #Check positive diagonal win (opponent)
    for r in range(row-3):
        for c in range (4):
            if board[7*r+c] == board[7*(r+1)+c+1] == board[7*(r+2)+c+2] == board[7*(r+3)+c+3] == next_who_played: 
                winner = 2

    #Check negative diagonal win (opponent)
    for r in range(row-3):
        for c in range (4):
            if board[7*(r+3)+c] == board[7*(r+2)+c+1] == board[7*(r+1)+c+2] == board[7*(r)+c+3] == next_who_played: 
                winner = 2

    if winner == 1:
        return who_played
    elif winner == 2:
        return next_who_played
    else:
        return 0

def computer_move(board, turn, level):
    tf_array = [True,False]

    #Only apply random move based on the random number generated
    if level == 1:
        return(random.randint(0, 6),tf_array[random.randint(0, 1)])

    if level == 2:
        temp_board = board.copy()
        opp_win_by_place = [0, 0, 0, 0, 0, 0, 0]
        opp_win_by_pop = [0, 0, 0, 0, 0, 0, 0]

        #Check for computer's direct win
        for i in range(7):
            if check_victory(apply_move(board, turn, i, False),turn) == turn and check_move(board, turn, i, False):                
                return (i, False)
            if check_victory(apply_move(board, turn, i, True),turn) == turn and check_move(board, turn, i, True):
                return (i, True)

        #Check for player's direct win
        for i in range(7):
            temp_board = apply_move(temp_board,turn+1,i,False)
            if check_victory(temp_board,turn+1) == turn+1 and check_move(temp_board, turn+1, i, False):
                return(i, False)

        #Randomly apply move that will not lead to opposition winning
        while True:
            col = random.randint(0, 6)
            pop = tf_array[random.randint(0, 1)]
            if pop and opp_win_by_pop[col] == 1:
                continue
            elif not pop and opp_win_by_place[col] == 1:
                continue
            else:
                return (col, False)

    return (0, False)


def display_board(board):
    column_labels = ['    0','   1','   2','   3','   4','   5','   6']
    row_labels = []
    n_row = int(len(board)/7)

    #Append the row labels based on user's input
    for i in range(1, n_row+1):
        row_labels.append(i)

    #Print board structures
    for i in range(1, n_row+1):
        print('  ' + '-' * 29)
        print(str(row_labels[-i]) + ' |', end = "")
        for j in range(7):
            print(' ' + str(board[7*(n_row-i)+j])+ ' |', end = "")
        print()
    print('  ' + '-' * 29)

    #Print column labels
    for i in column_labels:
        print(i, end = '')
    print()

#Check if player's input is within the stated range
def determine_row():
    n_column = 7
    row = 6
    inp_row = input("Enter the number of row, type 'None' if no preference:")

    #Fix the number of rows at 7 if user does not have a preference
    if inp_row == 'None':
        n_row = row
    else:
        n_row = int(inp_row)

    #Repeat the prompt for correct input within the stated range
    while n_row <= 5 or n_row >= 10:
        print('Out of range! The number of row can only be within 6 to 9!')
        inp_row = input("Enter the number of row, type 'None' if no preference:")
        n_row = int(inp_row)
        if inp_row == 'None':
            n_row = row
    return n_row

#Options to play against computer player or human player
def opponent_option():
    option = int(input("Enter '1' to play with human || Enter '2' to play with computer:"))
    if option == 1:
        return 0

    #Choose between different level of difficulties
    else:
        print('LEVEL 1 - Press 1\nLEVEL 2 - Press 2')
        level = int(input('Choose level of difficulty: '))
        while not level == 1 and not level == 2:
            print('Error !')
            level = int(input('Choose level of difficulty: '))
        return level 


def menu():
    game_over = False
    turn = 1

    row = determine_row()
    board = [0 for i in range(7*row)]

    level = opponent_option()
    display_board(board)
    
    while not game_over:
        if turn == 1:
            print('Player 1 turns!')
            if level == 0:
                while True:
                    col = int(input('Enter your column you want to make a move (0-6): '))
                    while not (0 <= col <= 6):
                        print('Please enter within the valid range!')
                        col = int(input('Enter your column you want to make a move (0-6): '))

                    pop = input('Do you want to pop or drop a disc? (Y for pop / N for drop): ')

                    while True: 
                        if pop == 'Y' or pop == 'y':
                            pop = True
                            break
                        elif pop == 'N' or pop == 'n':
                            pop = False
                            break
                        else: 
                            print('Invalid input! ')
                            pop = input('Do you want to pop or drop a disc? (Y for pop / N for drop): ')

                    if check_move(board, turn, col, pop):
                        board = apply_move(board, turn, col, pop)
                        #display_board(board)
                        if check_victory(board, turn) > 0:
                            display_board(board)
                            if level == 0:
                                print('Congratulation! Player ' + str(check_victory(board, turn)) + ' wins')
                                exit()
                            else:
                                print('Congratulation! Bot1 wins!')
                                exit()
                        break
                    else:
                        print('Invalid move!')
            else:
                while True:
                    col_pop = computer_move(board, turn, level)
                    if check_move(board, turn, col_pop[0], col_pop[1]):
                        board = apply_move(board, turn, col_pop[0], col_pop[1])
                        if check_victory(board, turn) == 1:
                            display_board(board)
                            print('Congratulation! Bot1 wins!')
                            exit()
                        break
                    else:
                        print('Invalid move!')

        elif turn == 2:
            print('Player 2 turns!')
            while True:
                col = int(input('Enter your column you want to make a move (0-6): '))

                while not (0 <= col <= 6):
                    print('Please enter within the valid range!')
                    col = int(input('Enter your column you want to make a move (0-6): '))

                pop = input('Do you want to pop or drop a disc? (Y for pop / N for drop): ')

                while True: 
                    if pop == 'Y' or pop == 'y':
                        pop = True
                        break
                    elif pop == 'N' or pop == 'n': 
                        pop = False
                        break
                    else: 
                        print('Invalid input! ')
                        pop = input('Do you want to pop or drop a disc? (Y for pop / N for drop): ')

                if check_move(board, turn, col, pop):
                    board = apply_move(board, turn, col, pop)
                    #display_board(board)
                    if check_victory(board, turn) > 0:
                        display_board(board)
                        print('Congratulation! Player ' + str(check_victory(board, turn)) + ' wins')
                        exit()
                    break
                else:
                    print('Invalid move!')

        display_board(board)
        turn += 1
        if turn > 2:
            turn = 1

if __name__ == '__main__':
    #menu()

    def test():
    
        # ***************** check_move ***************** #
        print()
        
        board = [0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        if check_move(board, 1, 1, False): print("test check_move 1 - OK !")
        else: print("test check_move 1 - Problem in the check_move function output !")
        
        board = [0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        if not check_move(board, 1, 1, True): print("test check_move 2 - OK !")
        else: print("test check_move 2 - Problem in the check_move function output !")
        
        board = [1,0,0,0,0,0,0,  2,0,0,0,0,0,0,  1,0,0,0,0,0,0,  2,0,0,0,0,0,0,  1,0,0,0,0,0,0,  2,0,0,0,0,0,0]
        if not check_move(board, 1, 0, False): print("test check_move 3 - OK !")
        else: print("test check_move 3 - Problem in the check_move function output !")
        
        board = [1,0,0,0,0,0,0,  2,0,0,0,0,0,0,  1,0,0,0,0,0,0,  2,0,0,0,0,0,0,  1,0,0,0,0,0,0,  2,0,0,0,0,0,0]
        if check_move(board, 1, 0, True): print("test check_move 4 - OK !")
        else: print("test check_move 4 - Problem in the check_move function output !")
        
        board = [1,0,0,0,0,0,0,  2,0,0,0,0,0,0,  1,0,0,0,0,0,0,  2,0,0,0,0,0,0,  1,0,0,0,0,0,0,  2,0,0,0,0,0,0]
        if not check_move(board, 2, 0, True): print("test check_move 5 - OK !")
        else: print("test check_move 5 - Problem in the check_move function output !")
        
        board = [0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        if not check_move(board, 1, 1, True): print("test check_move 6 - OK !")
        else: print("test check_move 6 - Problem in the check_move function output !")
        
        board = [1,0,0,0,0,0,0,  2,0,0,0,0,0,0,  1,0,0,0,0,0,0,  2,0,0,0,0,0,0]
        if not check_move(board, 1, 0, False): print("test check_move 7 - OK !")
        else: print("test check_move 7 - Problem in the check_move function output !")
    
        
        # ***************** apply_move ***************** #
        print()
        
        board = [1,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        board_result = [1,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        apply_move(board, 1, 0, False)
        if board == board_result: print("test apply_move 1 - OK !")
        else: print("test apply_move 1 - Problem in the apply_move function output !")
        
        board = [0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        board_result = [1,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        board_tmp = apply_move(board, 1, 0, False)
        if board_tmp == board_result: print("test apply_move 2 - OK !")
        else: print("test apply_move 2 - Problem in the apply_move function output !")
        
        board = [0,1,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        board_result = [0,1,0,0,0,0,0,  0,2,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        board_tmp = apply_move(board, 2, 1, False)
        if board_tmp == board_result: print("test apply_move 3 - OK !")
        else: print("test apply_move 3 - Problem in the apply_move function output !")
        
        board = [1,1,0,0,0,0,0,  2,2,0,0,0,0,0,  2,0,0,0,0,0,0,  1,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        board_result = [2,1,0,0,0,0,0,  2,2,0,0,0,0,0,  1,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        board_tmp = apply_move(board, 1, 0, True)
        if board_tmp == board_result: print("test apply_move 4 - OK !")
        else: print("test apply_move 4 - Problem in the apply_move function output !")
        
        board = [0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        board_result = [1,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        board_tmp = apply_move(board, 1, 0, False)
        if board_tmp == board_result: print("test apply_move 5 - OK !")
        else: print("test apply_move 5 - Problem in the apply_move function output !")
        
        board = [1,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        board_result = [1,0,0,0,0,0,0,  2,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        board_tmp = apply_move(board, 2, 0, False)
        if board_tmp == board_result: print("test apply_move 6 - OK !")
        else: print("test apply_move 6 - Problem in the apply_move function output !")
        
        
        # ***************** check_victory ***************** #
        print()
        
        board = [1,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        if check_victory(board, 1)==0: print("test check_victory 1 - OK !")
        else: print("test check_victory 1 - Problem in the check_victory function output !")
        
        board = [1,1,1,1,0,0,0,  2,0,0,0,0,0,0,  2,0,0,0,0,0,0,  2,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        if check_victory(board, 1)==1: print("test check_victory 2 - OK !")
        else: print("test check_victory 2 - Problem in the check_victory function output !")
        
        board = [2,1,1,1,0,0,0,  2,1,0,0,0,0,0,  2,0,0,0,0,0,0,  2,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        if check_victory(board, 2)==2: print("test check_victory 3 - OK !")
        else: print("test check_victory 3 - Problem in the check_victory function output !")
        
        board = [1,2,0,0,0,0,0,  1,2,0,0,0,0,0,  1,2,0,0,0,0,0,  1,2,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        if check_victory(board, 1)==2: print("test check_victory 4 - OK !")
        else: print("test check_victory 4 - Problem in the check_victory function output !")
        
        board = [1,2,2,2,0,0,0,  0,1,2,1,0,0,0,  0,0,1,2,0,0,0,  0,0,0,1,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        if check_victory(board, 1)==1: print("test check_victory 5 - OK !")
        else: print("test check_victory 5 - Problem in the check_victory function output !")
        
        board = [0,0,0,2,1,1,1,  0,0,0,1,1,2,1,  0,0,0,1,2,2,2,  0,0,0,2,2,1,1,  0,0,0,1,1,2,1,  0,0,0,2,2,1,0,  0,0,0,2,1,0,0,  0,0,0,1,0,0,0]
        if check_victory(board, 1)==1: print("test check_victory 6 - OK !")
        else: print("test check_victory 6 - Problem in the check_victory function output !")
        
        
        # ***************** computer_move ***************** #
        print()
        
        board = [1,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        board_result = [1,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        computer_move(board, 1, 1)
        computer_move(board, 1, 2)
        if board == board_result: print("test computer_move 1 - OK !")
        else: print("test computer_move 1 - Problem in the computer_move function output !")
        
        board = [1,1,1,0,0,0,0,  2,0,0,0,0,0,0,  2,0,0,0,0,0,0,  2,0,0,0,0,0,0,  0,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        if computer_move(board, 1, 2) in [(3, False)]: print("test computer_move 2 - OK !")
        else: print("test computer_move 2 - Problem in the computer_move function output !")
        
        board = [1,1,1,0,0,0,0,  2,0,0,0,0,0,0,  2,0,0,0,0,0,0,  2,0,0,0,0,0,0,  0,0,0,0,0,0,0]
        if computer_move(board, 1, 2) in [(3, False)]: print("test computer_move 3 - OK !")
        else: print("test computer_move 3 - Problem in the computer_move function output !")
    
   
test()

