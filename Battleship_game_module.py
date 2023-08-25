# List of import
from random import randint
from time import sleep

# Game variable
CARRIER_SIZE = 4
SUBMARINE_SIZE = 3
list_AtoJ = [chr(c) for c in range(ord('A'), ord('J') + 1)]
list_1to10 = [chr(i) for i in range(ord('1'), ord('9') + 1)]
list_1to10.append('10')

num_of_rows = len(list_AtoJ)
num_of_cols = len(list_1to10)
cpu_surface = [[' '] * num_of_cols for i in range(num_of_rows)]  # creating boards via list comprehension
cpu_subsea = [[' '] * num_of_cols for i in range(num_of_rows)]
user_surface = [[' '] * num_of_cols for i in range(num_of_rows)]
user_subsea = [[' '] * num_of_cols for i in range(num_of_rows)]
gameover = False
player_turn = True
CPU_turn = False

### GAME DISPLAY ###

# Functionality: Prints the board headers to inform users which board is which
# Parameters:
#	cpu_or_player: a string; CPU or player’s boards
#	space: the number of whitespaces between the boards
# Author: Joel
def print_header(cpu_or_player, space):
    if cpu_or_player.upper() == 'CPU':
        print(cpu_or_player.upper(), 'surface', end=' ' * (space - 10))
    elif cpu_or_player.upper() == 'PLAYER':
        print(cpu_or_player.upper(), 'surface', end=' ' * (space - 14))
    print(cpu_or_player.upper(), 'subsea')


# Functionality: Display the Battleship boards, inclusive of headers identifying
# which board is which, and numbering of the x and y axes
# (resizable, default is 10x10)
# Parameters:
#	cpu_or_player: a string, to identify if the board belongs to CPU or player
# 	board0: 2D list of the first board (surface)
# 	board1: 2D list of the second board (subsea)
#	x = num_of_cols: Number of columns board has (default 10)
#	y = num_of_rows: Number of rows board has (default 10)
#	space = 2: number of whitespaces between the boards (default 2)
# Author: Joel
def display(cpu_or_player, board0, board1, x=num_of_cols, y=num_of_rows, space=2):
    numbers = [str(i) for i in range(1, x + 2)]
    letters = [chr(i) for i in range(ord('A'), ord('A') + y)]
    number_index = 0
    letter_index = 0
    board0_row = 0
    board0_col = 0
    board1_row = 0
    board1_col = 0
    space = 5*space + 3 
    height = 4 * y + 3
    width = 10*x + space + 4
    start_of_second_board = 5*x + 2 + space
    end_of_first_board = 5 * x + 2

    print_header(cpu_or_player, start_of_second_board)
    for i in range(height):
        if i == 0:
            for j in range(width):
                if end_of_first_board <= j < start_of_second_board:
                    print(" ", end="")
                    number_index = 0
                elif len(numbers[number_index]) < 2:
                    if j % 5 == 4 and j != 0:
                        print(numbers[number_index], end="")
                        number_index += 1
                    else:
                        print(" ", end="")
                else:
                    if j % 5 == 3:
                        print(numbers[number_index][0], end="")
                    elif j % 5 == 4:
                        print(numbers[number_index][1], end="")
                        number_index += 1
                    else:
                        print(" ", end="")
        elif i % 2 == 1:
            print("")
        elif i % 4 == 0:
            for j in range(width):
                if end_of_first_board < j < start_of_second_board:
                    print(" ", end="")
                elif j == 0:
                    print(letters[letter_index], end="")
                elif j == start_of_second_board:
                    print(letters[letter_index], end="")
                elif j % 5 == 1:
                    print("|", end="")
                elif j % 5 == 3 and j < end_of_first_board:
                    if cpu_or_player.upper() == "CPU":
                        if board0[board0_row][board0_col] == 'C' or board0[board0_row][board0_col] == 'S':
                            print(' ', end='')
                        else:
                            print(board0[board0_row][board0_col], end='')
                    else:
                        print(board0[board0_row][board0_col], end='')
                    board0_col += 1
                elif j % 5 == 3 and j > start_of_second_board:
                    if cpu_or_player.upper() == "CPU":
                        if board1[board1_row][board1_col] == 'C' or board1[board1_row][board1_col] == 'S':
                            print(' ', end='')
                        else:
                            print(board1[board1_row][board1_col], end='')
                    else:
                        print(board1[board1_row][board1_col], end='')
                    board1_col += 1
                else:
                    print(" ", end="")
            letter_index += 1
            board0_row += 1
            board0_col = 0
            board1_row += 1
            board1_col = 0
        elif i % 4 == 2:
            for j in range(width):
                if end_of_first_board  <= j <= start_of_second_board :
                    print(" ", end="")
                elif j == 0:
                    print(" ", end="")
                else:
                    print("-", end="")
    print("")

### GAME PLACEMENT ###

# Functionality: Determine where to place player ships based on player’s
# chosen coordinates
# Parameters:
#	board0 = user_surface: the 1st board (default user surface)
#	board1 = user_subsea: the 2nd board (default user subsea)
# Author: Joel and Haoyang
def user_set_piece(board0=user_surface, board1=user_subsea):
    row, col, rotation = get_coords(CARRIER_SIZE)
    set_piece(row, col, rotation, board0, "C", CARRIER_SIZE)
    board = choose_board("\n------PLACE SUBMARINE-------\nNow we will place the submarine. Remember it is only 3 units long.\nDo you want your submarine to be placed on subsea or surface?")
    row, col, rotation = get_coords(SUBMARINE_SIZE)
    if board:
        set_piece(row, col, rotation, board1, "S", SUBMARINE_SIZE)
    else:
        while check_overlap(row, col, rotation, board0, SUBMARINE_SIZE, "C"):
            row, col, rotation = get_coords(SUBMARINE_SIZE)
        else:
            set_piece(row, col, rotation, board0, "S", SUBMARINE_SIZE)
    display("Player", user_surface, user_subsea)

# Functionality: Determine where to place CPU ships based on CPU’s chosen
# coordinates
# Parameters:
#	board0 = cpu_surface: the 1st board (default CPU surface)
#	board1 = cpu_subsea: the 2nd board (default CPU subsea)
# Author: Joel and Haoyang
def cpu_set_piece(board0=cpu_surface, board1=cpu_subsea):
    # set carrier
    row, col, rotation = cpu_rand_coord(num_of_rows, num_of_cols, CARRIER_SIZE)
    set_piece(row, col, rotation, board0, "C", CARRIER_SIZE)
    # set submarine
    submarine_board = randint(0, 1)
    row, col, rotation = cpu_rand_coord(num_of_rows, num_of_cols, SUBMARINE_SIZE)
    if submarine_board == 1:
        set_piece(row, col, rotation, board1, "S", SUBMARINE_SIZE)
    else:
        while check_overlap(row, col, rotation, board0, SUBMARINE_SIZE, "C"):
            row, col, rotation = cpu_rand_coord(num_of_rows, num_of_cols, SUBMARINE_SIZE)
        else:
            set_piece(row, col, rotation, board0, "S", SUBMARINE_SIZE)

# Functionality: Check if ships overlap
# Parameters:
#	row: the row in which a unit of the ship occupies
#	column: the column in which a unit of the ship occupies
#	rotation: whether ship is horizontal or vertical
#	board: surface or subsea
#	size: size of ship aka number of units of the ship
#	ship: type of ship (carrier or submarine)
# Returns: True if ships overlap, False if ships do not overlap
# Author: Jackson
def check_overlap(row, col, rotation, board, size, ship):
    if rotation == 0:
        for i in range(size):
            if board[row][col + i] == ship:
                print("Your submarine overlapped with your carrier, please choose again!")
                return True
        return False
    if rotation == 1:
        for i in range(size):
            if board[row + i][col] == ship:
                print("Your submarine overlapped with your carrier, please choose again!")
                return True
        return False

# Functionality: Place ships on the board.
# Board will display location of ship based on the following:
# Parameters:
#	row: the row the ship occupies
#	col: the column the ship occupies
#	rotation: whether the ship is horizontal or vertical
#	board: which board to occupy (surface or subsea)
#	ship: type of ship (“C” for carrier, “S” for submarine)
#	size: size of ship aka number of units the ship occupies
# Author: Joel and Haoyang
def set_piece(row, col, rotation, board, ship, size):
    if rotation == 0:
        for i in range(size):
            board[row][col + i] = ship
    else:
        for i in range(size):
            board[row + i][col] = ship

### PLAYER INPUT ###

# Functionality: Get user to choose a board to place the submarine
# (surface or subsea)
# Parameters: description: The message to display
# Returns: False if surface is chosen or True if subsea is chosen.
# Author: Joel and Haoyang
def choose_board(description):
    while True:
        board = input("{}\nEnter 0 for surface, 1 for subsea\nPlease enter your choice: ".format(description))
        if board == '1':
            return True
        elif board == '0':
            return False
        else:
            print('invalid choice, please try again')
            continue

# Functionality: Get rotation of player’s ships to place on board
# Returns: int(rotation): 0 if ship is horizontal, 1 if vertical
# Author: Jackson and Joel
def player_rotation():
    while True:
        rotation = input("Do you want your ship to be placed vertically or horizontally?\nEnter 0 for horizontal, 1 for vertical\nPlease enter your choice: ")
        if rotation == '0' or rotation == '1':
            return int(rotation)
        else:
            print("You entered an invalid choice, please try again.")


# Functionality: After taking in input for rotation of ship, prompt player to
# enter coordinates of ship to place on board and check if input is valid
# Parameters: length: The length of the ship
# Returns:
#	list_AtoJ.index(guess[0].upper()): the row to place the ship in (A to J)
#	list_1to10.index(guess[2]): the column to place the ship in (1 to 10)
#	rotation: rotation of ship (horizontal or vertical)
# The following will only be returned if user chooses column 10:
#	list_1to10.index(guess[2:4]): the last column of the board to place the ship
# Author: Haoyang
def get_coords(length):
    rotation = player_rotation()
    while True:

        if rotation == 0:
            print('Note: For horizontal orientation, your ship can be placed between column 1 to {} only'.format(
                11 - length))
            guess = input("Enter coordinates e.g. A,1: ")
            if len(guess) == 3:
                if guess[0].upper() in list_AtoJ and guess[1] == ',' and guess[2] in list_1to10[:-length + 1]:
                    return list_AtoJ.index(guess[0].upper()), list_1to10.index(guess[2]), rotation

        elif rotation == 1:
            print('Note: For vertical orientation, your ship can be placed between column A to {} only'.format(
                chr(ord('J') + 1 - length)))
            guess = input("Enter coordinates e.g. A,1: ")
            if len(guess) == 4:
                if guess[2:4] == '10' and guess[1] == ',' and guess[0].upper() in list_AtoJ[:-length + 1]:
                    return list_AtoJ.index(guess[0].upper()), list_1to10.index(guess[2:4]), rotation
            elif len(guess) == 3:
                if guess[0].upper() in list_AtoJ[:-length + 1] and guess[1] == ',' and guess[2] in list_1to10:
                    return list_AtoJ.index(guess[0].upper()), list_1to10.index(guess[2]), rotation

        print("Invalid input. Please strictly follow format.")
        continue

### CPU INPUT ###

# Functionality: Generate a random coordinate and orientation to place CPU ships
# Parameters:
#		board_row: number of rows of board
#		board_col: number of columns of board
#		size: length of ship
# Returns:
#		row: the row the ship occupies
#		col: the column the ship occupies
#		rotation: whether ship is horizontal or vertical
# Author: Joel
def cpu_rand_coord(board_row, board_col, size):
    rotation = randint(0, 1)  # 0 means horizontal, 1 means vertical
    if rotation == 0:
        row = randint(0, board_row - 1)
        col = randint(0, board_col - size)
        return row, col, rotation
    else:
        row = randint(0, board_row - size)
        col = randint(0, board_col - 1)
        return row, col, rotation

### ATTACK FUNCTION ###

# Functionality: Ask player to choose a coordinate on the board to attack
# and checks if input is valid
# Returns: the chosen coordinates
#	list_AtoJ.index(guess[0].upper()): the row to attack (uppercase A to J)
#	list_1to10.index(guess[2]): the column to attack (1 to 10)
#	list_1to10.index(guess[2:4]): column 10 (if user chooses to attack column 10)
# Author: Jackson and Joel
def choose_target_coordinate():
    while True:
        guess = input("Enter coordinates e.g. A,1: ")
        if len(guess) == 4:
            if guess[2:4] == '10' and guess[1] == ',' and guess[0].upper() in list_AtoJ:
                return list_AtoJ.index(guess[0].upper()), list_1to10.index(guess[2:4])
        elif len(guess) == 3:
            if guess[0].upper() in list_AtoJ and guess[1] == ',' and guess[2] in list_1to10:
                return list_AtoJ.index(guess[0].upper()), list_1to10.index(guess[2])

        print("Invalid input. Please strictly follow format.")
        continue


# Functionality: Check if the surrounding 3x3 grid has been hit
# Parameters:
#	board: the board attacked (surface or subsea)
#	row: centre row of the 3x3 grid
#	col: centre column of the 3x3 grid
# Returns: hit (True if there is a ship in the 3x3 grid, else hit = False)
# Author: Haoyang
def area_damage(board, row, col):
    # top left corner
    hit = False
    if row == 0 and col == 0:
        for i in range(row, row + 2):
            for j in range(col, col + 2):
                if update_board(board, i, j):
                    hit = True
    # top right corner
    elif row == 0 and col == 9:
        for i in range(row, row + 2):
            for j in range(col, col - 2, -1):
                if update_board(board, i, j):
                    hit = True
    # bottom left corner
    elif row == 9 and col == 0:
        for i in range(row, row - 2, -1):
            for j in range(col, col + 2):
                if update_board(board, i, j):
                    hit = True
    # bottom right corner
    elif row == 9 and col == 9:
        for i in range(row, row - 2, -1):
            for j in range(col, col - 2, -1):
                if update_board(board, i, j):
                    hit = True
    # first row less corner
    elif row == 0:
        for i in range(row, row + 2):
            for j in range(col - 1, col + 2):
                if update_board(board, i, j):
                    hit = True
    # last row less corner
    elif row == 9:
        for i in range(row, row - 2, -1):
            for j in range(col - 1, col + 2):
                if update_board(board, i, j):
                    hit = True
    # first col less corner
    elif col == 0:
        for i in range(row - 1, row + 2):
            for j in range(col, col + 2):
                if update_board(board, i, j):
                    hit = True
    # last col less corner
    elif col == 9:

        for i in range(row - 1, row + 2):
            for j in range(col, col - 2, -1):
                if update_board(board, i, j):
                    hit = True
    # all other locations
    else:
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if update_board(board, i, j):
                    hit = True
    return hit

# Functionality: Update the board to show the result of an attack (hit or miss)
# The attacked location will show * for hit, X for miss
# Parameters:
#	board: which board to update (surface or subsea)
#	row: the row attacked
#	col: the col attacked
# Returns:  True if hit, False if missed.
# Author: Joel and Haoyang
def update_board(board, row, col):
    if board[row][col] == 'C' or board[row][col] == 'S':
        board[row][col] = '*'
        return True
    elif board[row][col] == ' ':
        board[row][col] = 'X'
        return False
    else:
        return False

# Functionality: Based on players’ chosen board and coordinates,
# reflect the result of the attack (hit/miss/already attacked) of chosen
# coordinate and surrounding 3x3 grid and end the turn
# Author: Jackson and Haoyang
def player_attack():
    global player_turn
    global cpu_turn
    while player_turn:
        board = choose_board("Choose the game board you want to attack?")
        if board:
            board = cpu_subsea
        else:
            board = cpu_surface
        row, col = choose_target_coordinate()
        if board[row][col] == ' ' or board[row][col] == 'C' or board[row][col] == 'S':
            hit = area_damage(board, row, col)
            display('cpu', cpu_surface, cpu_subsea)
            if hit:
                print('\nYou hit the cpu ship!')
            else:
                print('\nYou missed!')
            player_turn = False
            cpu_turn = True
            return
        else:
            print('You have attacked this area before, try one more time')
            continue


# Functionality: CPU chooses a random board and coordinate to attack.
# Players then informed if his/her ships are hit
# Finally, CPU ends turn
# Author: Jackson and Haoyang
def cpu_attack():
    global player_turn
    global cpu_turn

    while cpu_turn:

        board_can_be_attacked = False

        # cpu choose which board to attack
        board = randint(0, 1)
        if board:
            board = user_surface
        else:
            board = user_subsea
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == ' ' or board[i][j] == 'C' or board[i][j] == 'S':
                    board_can_be_attacked = True
                    break
            if board_can_be_attacked:
                break
        if not board_can_be_attacked:
            continue

        # cpu choose which row and col to attack
        row = randint(0, 9)
        col = randint(0, 9)
        if board[row][col] == 'X' or board[row][col] == '*':
            continue

        hit = area_damage(board, row, col)
        display('player', user_surface, user_subsea)
        if hit:
            print('\nYour ship has been hit!')
        else:
            print('\ncpu missed!')
        player_turn = True
        cpu_turn = False
        return

### RESULT ###

# Functionality: Check if there are still ships on the boards.
# If there are still ships on the board, the opposing player’s turn begins.
# Else, end the game
# Parameters:
#	board_0: The first board (surface)
#	board_1: The second board (subsea)
#	whose_turn: a string; "CPU" or "player" 's turn
# Author: Jackson and Joel
def check_board(board_0, board_1, whose_turn):
    global gameover

    for i in range(len(board_0)):  # since len(board_0) == len(board_1), can use either board

        for j in range(len(board_0[i])):
            if board_0[i][j] == 'S' or board_0[i][j] == 'C' or board_1[i][j] == 'C' or board_1[i][j] == 'S':
                input("Press Enter to continue.\n")
                print("-----{}'s Turn-----".format(whose_turn))
                return
    gameover = True
    return


# Functionality: Print the results (win or lose)
# Parameters: turns: The number of turns taken
# Author: Joel and Haoyang
def result(turns):
    global player_turn
    global cpu_turn
    try:
        if cpu_turn:
            print('You win! you have won in {} turns'.format(turns))
        elif player_turn:
            print('Sorry you lost, thanks for playing. you have lost in {} turns'.format(turns))
    except: # in the event program cannot determine winner for some reason
        print("Does it matter who wins? What matters most is the journey, not the end result.")

### GAME ###

# Functionality: Explain the game to users, mainly for abstraction purposes
# Author: Jackson
def explain_game():
    print("""
----------------------
~~~~~~~~~~~~~~~~~~~~
    BATTLESHIP+
~~~~~~~~~~~~~~~~~~~~
----------------------""")
    print("""Welcome to Battleship+! Battleship+ is a single-player game that reinvents the old-school board game.
You and your opponent (the CPU) have 2 ships to place in the board:

1x [C]ARRIER (length 4x1)
1x [S]UBMARINE (length 3x1)

You may place them anywhere in the board. However, in Battleship+, there are two boards:
-SEA SURFACE: both ships can be placed on this board.
-SUBSEA: only the submarine can be placed on this board.

In this game, after choosing a space, the surrounding spaces will be revealed to you as well in the form of a 3x3 grid.
If you can sink your opponent's ships first, you win! Otherwise, you lose.

With that out of the way, it's time to play Battleship+!
""")

    print("""Before we can target ships, we need to place ships first.
To place a ship, enter the coordinates of the START of the ship.
For example, if you want the ship placed like this:

                   1    2    3    4    5    6    7    8    9   10
                ----------------------------------------------------
               A| C  |    |    |    |    |    |    |    |    |    |
                ----------------------------------------------------
               B| C  |    |    |    |    |    |    |    |    |    |
                ----------------------------------------------------
               C| C  |    |    |    |    |    |    |    |    |    |
                ----------------------------------------------------
               D| C  |    |    |    |    |    |    |    |    |    |
                ----------------------------------------------------
               E|    |    |    |    |    |    |    |    |    |    |
                ----------------------------------------------------
               F|    |    |    |    |    |    |    |    |    |    |
                ----------------------------------------------------
               G|    |    |    |    |    |    |    |    |    |    |
                ----------------------------------------------------
               H|    |    |    |    |    |    |    |    |    |    |
                ----------------------------------------------------
               I|    |    |    |    |    |    |    |    |    |    |
                ----------------------------------------------------
               J|    |    |    |    |    |    |    |    |    |    |
                ----------------------------------------------------

First choose if you want to place it horizontally or vertically, then input the ship's starting coordinates: A,1
""")
    print("------PLACE CARRIER-------")
    print("We will first place the CARRIER. Remember that the carrier can only be placed on the sea surface and is 4 units long.\n")

# Functionality: Play the game (set up ships and attack boards)
# Returns: False if game has ended
# Author: Jackson and Haoyang
def game():
    global gameover
    global player_turn
    global cpu_turn
    total_turn = 0
    explain_game()
    #Pre-game execution
    user_set_piece()
    print("\nCPU placing ships...\n")
    cpu_set_piece()
    sleep(1)
    print("Game will start now!\n")
    #Game Execution
    while not gameover:
        if player_turn:
            total_turn+=1
            player_attack()
            check_board(cpu_subsea, cpu_surface, "CPU")
        elif cpu_turn:
            cpu_attack()
            check_board(user_subsea, user_surface, "Player")
    else:
        result(total_turn)
        return False
