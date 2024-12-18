from ui import *
import pickle

SHIPS = [("Speedboat", 2), ("Destroyer", 4), ("Attacker", 3), ("Attacker", 3), ("Aircraft Carrier", 5), ]

def main():
    while True: # Load the menu and check for user input
        scoreboard = load_scoreboard()
        selected_menu_item = menu()
        if selected_menu_item == 1:
            winner = play_battleships()
            if winner:
                if winner not in scoreboard:    # Adds the winner to the scoreboard with score 1 if they're not in the scoreboard yet,
                    scoreboard[winner] = 1      # otherwide adds 1 to the score of the winner
                    save_scoreboard(scoreboard)
                else:
                    scoreboard[winner] += 1
                    save_scoreboard(scoreboard)

        elif selected_menu_item == 2:
            display_headline("SCOREBOARD BATTLESHIPS")
            display_scoreboard(scoreboard)
            prompt("Press ENTER to return to the menu")

        elif selected_menu_item == 3:
            return None

def menu():
    """
    This function displays the menu and asks for a user input repeadedly until a valid input is given
    """
    display_headline("MENU BATTLESHIPS")
    menu_items = ["Play Battleships", "Scoreboard", "Exit"]
    display_menu(menu_items)
    while True:
        selected_menu_item = prompt("Enter the number of your choice").strip()
        if selected_menu_item.isdigit() and int(selected_menu_item) > 0 and int(selected_menu_item) <= len(menu_items): # Checks for the datatype and lenghts of the user input
            return int(selected_menu_item)

def get_player_names(): 
    """
    This function will get the player's names and check that they are valid and different from each other.
    """
    display_headline("enter player names")
    while True:
        player_a = prompt("Enter the name of player A").strip()
        if len(player_a) >= 1:
            break
            
    while True:
        player_b = prompt("Enter the name of player B").strip()
        if len(player_b) < 1:
            continue
        elif player_b.lower() != player_a.lower():
            break

    return player_a, player_b

def create_grid(rows, cols):
    """
    This function creates an empty grid with a given size rows, cols
    """
    grid = []
    for i in range(rows):
        row = []
        for i in range(cols):
            row.append(None)
        grid.append(row)
    return grid

def save_scoreboard(scoreboard):
    """
    This function saves the scoreboard by using pickle.dump. It first removes any players with score 0
    """
    new_scoreboard = {}
    for name, score in scoreboard.items():
        if score > 0:
            new_scoreboard[name] = score

    with open("scoreboard.dat", "wb") as scoreboard_file:
        pickle.dump(new_scoreboard, scoreboard_file)
    return None
    
def load_scoreboard():
    """
    This function loads the scoreboard from the file scoreboard.dat using pickle.load. It will check for the
    correct data type for the name (str) and score (int), for any invalid type it returns an empty dicitonary.
    """
    try: 
        with open("scoreboard.dat", "rb") as scoreboard_file:
            scoreboard = pickle.load(scoreboard_file)

            if isinstance(scoreboard, dict) != True:
                raise ValueError
        
            for name, score in scoreboard.items():
                if isinstance(name, str) != True or isinstance(score, int) != True:
                    raise ValueError
            
        return scoreboard
    except (FileNotFoundError, EOFError, ValueError, pickle.UnpicklingError):
        return {}

def is_game_won(grid):
    """
    This function checks if the game is won by returning False if there is any "True" left in the grid, otherwise returning True (e.g. the game is won)
    """
    for i in range(len(grid)):
        for col in grid[i]:
            if col == True:
                return False
    return True

def play_turn(grid_a, grid_b, player_name, is_player_a):
    """
    This function will execute one turn in the game. It displays the current game and asks for the target position of the player.
    It checks for a correct input and executes the input if it's valid. 
    The function will return True if a ship was hit, otherwise False.
    """
    display_turn_start(player_name, is_player_a)
    if is_player_a == True:
        grid = grid_b
    else:
        grid = grid_a
    display_game(grid_a, grid_b)

    valid_input = False
    while valid_input == False:
        try:
            target_position = prompt("Please select a row and a column")
            target_coordinates = target_position.split()
            row, col = int(target_coordinates[0]), int(target_coordinates[1])
            if len(target_coordinates) != 2:
                raise ValueError
            elif row < 1 or row > len(grid_a):
                raise ValueError
            elif col < 1 or col > len(grid_a):
                raise ValueError
            
            valid_input = True
        except (ValueError, IndexError):
            continue

    if grid[row - 1][col - 1] == True:  # Applying the target coordinates to the grid
        grid[row - 1][col - 1] = False
        return True
    elif grid[row - 1][col - 1] == None:
        grid[row - 1][col - 1] = 'miss'
        return False

def is_ship_position_possible(length, start_row, start_col, end_row, end_col, grid):
    """
    This function will check if a ship position the user asked for is possible.
    It checks for the correct lenght of the ship and whether there is space for that ship.
    """
    if start_row == end_row:
        if (abs(start_col - end_col) + 1) != length:    # Check for correct lenght
            return False
        for i in range(min(start_col, end_col) - 1, max(start_col, end_col)):   # Check if the position is occupied by another ship
            if grid[start_row - 1][i] == True:
                return False
    
    elif start_col == end_col:
        if (abs(start_row - end_row) + 1) != length:    
            return False
        for i in range(min(start_row, end_row) - 1, max(start_row, end_row)):
            if grid[i][start_col - 1] == True:
                return False
        
    if start_row > len(grid) or start_col > len(grid[0]) or start_row < 1 or end_row < 1:   # Checks that the input is insde of the grid
        return False
    
    if end_row > len(grid) or end_col > len(grid[0]) or end_row < 1 or end_col < 1:
        return False
    
    else:
        return True

def position_ships(player, rows, cols, ships):
    """
    This function will have both players position their ships. It will check for the validity of the position,
    and adjust the grid accordingly.
    """
    grid = create_grid(rows, cols)
    for i in range(len(ships)):
        display_headline(f"{player} position the ship {ships[i][0]} - length {ships[i][1]}")
        display_grid(grid)
        valid_input = False
        while valid_input == False:
            ship_placement = prompt("Select beginning and end cell")
            points = ship_placement.split(',')

            if len(points) != 2:
                continue

            start_cell = points[0].split()
            end_cell = points[1].split()
            try:    # Check for the correct datatype of the positioned ship
                start_cell[0] = int(start_cell[0])
                start_cell[1] = int(start_cell[1])
                end_cell[0] = int(end_cell[0])
                end_cell[1] = int(end_cell[1])
            except (IndexError, ValueError):
                continue

            if len(start_cell) != 2 or len(end_cell) != 2:
                continue

            if is_ship_position_possible(ships[i][1], start_cell[0], start_cell[1], end_cell[0], end_cell[1], grid) == False:
                continue

            for i in range((min(start_cell[1], end_cell[1]) - 1), max(start_cell[1], end_cell[1])): # Applies the positioned ship to the grid        
                grid[start_cell[0] - 1][i] = True

            for i in range((min(start_cell[0], end_cell[0]) - 1), max(start_cell[0], end_cell[0])):
                grid[i][start_cell[1] - 1] = True 
            
            valid_input = True
    return grid             
        
def play_battleships(ships=SHIPS):
    player_a, player_b = get_player_names()

    grid_a = position_ships(player_a, 8, 8, ships)
    grid_b = position_ships(player_b, 8, 8, ships)

    a_wins = is_game_won(grid_b)
    b_wins = is_game_won(grid_a)
    while a_wins != True and b_wins != True:
        play_turn(grid_a, grid_b, player_a, True)
        a_wins = is_game_won(grid_b)
        if a_wins == True:  # This makes sure that player_b doesn't get another turn if a won
            break
        play_turn(grid_a, grid_b, player_b, False)
        b_wins = is_game_won(grid_a)

    display_headline("The game is over!")
    display_game(grid_a, grid_b)

    if a_wins == True:
        display_message(f"{player_a} won the game!")
        winner = player_a   
    if b_wins == True:
        display_message(f"{player_b} won the game!")
        winner = player_b

    prompt("Press ENTER to return to the menu")
    return winner

if __name__ == '__main__':
    main()
