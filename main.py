import os
from figures import white_pieces, white_locations, black_pieces, black_locations
from moves import *
from colorama import init, Fore, Back, Style


turn_step = 0
valid_moves = []

counter = 0
game_over = False

# Funktion zum Drucken des Schachbretts

def print_board(white_locations, black_locations, white_pieces, black_pieces):
    init(autoreset=True)

    board = [[' ' for _ in range(8)] for _ in range(8)]

    piece_symbols = {
        'pawn': 'P',
        'rook': 'R',
        'knight': 'N',
        'bishop': 'B',
        'queen': 'Q',
        'king': 'K'
    }

    for i, location in enumerate(white_locations):
        piece = white_pieces[i]
        board[location[1]][location[0]] = piece_symbols[piece].upper()  # white pieces in uppercase

    for i, location in enumerate(black_locations):
        piece = black_pieces[i]
        board[location[1]][location[0]] = piece_symbols[piece].lower()  # black pieces in lowercase

    red = Fore.RED
    reset = Style.RESET_ALL
    black_square = Back.BLACK
    gray_square = Back.LIGHTBLACK_EX  # Grau verwenden

    # Schachbrett ausdrucken
    print("   " + f"{red}A  B  C  D  E  F  G  H{reset}")
    for i in range(8):
        print(f"{red}{8 - i}{reset} ", end="")
        for j in range(8):
            if (i + j) % 2 == 0:
                square_color = gray_square
            else:
                square_color = black_square
            print(f"{square_color} {board[7 - i][j]} {reset}", end="")
        print(f" {red}{8 - i}{reset}")
    print("   " + f"{red}A  B  C  D  E  F  G  H{reset}")



def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_error_message(message):
    print(f"\033[91m{message}\033[0m")

def main():
    global turn_step, game_over
    turn = 'white'
    
    while not game_over:
        print_board(white_locations, black_locations, white_pieces, black_pieces)
        print(f"{turn.capitalize()}'s turn. Enter the position to move (Syntax: e2 e4):")
        move = input().strip()
        
        clear_screen()
        
        if len(move) != 5 or move[2] != ' ':
            print_error_message("Invalid input. Please enter in the format 'e2 e4'.")
            continue
        
        start_pos = (ord(move[0]) - ord('a'), int(move[1]) - 1)
        end_pos = (ord(move[3]) - ord('a'), int(move[4]) - 1)
        
        if turn == 'white' and start_pos in white_locations:
            idx = white_locations.index(start_pos)
            piece = white_pieces[idx]
            valid_moves = check_options([piece], [start_pos], turn)[0]
            
            if end_pos in valid_moves:
                white_locations[idx] = end_pos
                if end_pos in black_locations:
                    capture_idx = black_locations.index(end_pos)
                    black_locations.pop(capture_idx)
                    black_pieces.pop(capture_idx)
            else:
                print_error_message("Invalid move. Try again.")
                continue
        elif turn == 'black' and start_pos in black_locations:
            idx = black_locations.index(start_pos)
            piece = black_pieces[idx]
            valid_moves = check_options([piece], [start_pos], turn)[0]
            
            if end_pos in valid_moves:
                black_locations[idx] = end_pos
                if end_pos in white_locations:
                    capture_idx = white_locations.index(end_pos)
                    white_locations.pop(capture_idx)
                    white_pieces.pop(capture_idx)
            else:
                print_error_message("Invalid move. Try again.")
                continue
        else:
            print_error_message("Invalid move. It's not your turn or invalid piece.")
            continue
        
        turn = 'black' if turn == 'white' else 'white'
        turn_step += 1

if __name__ == "__main__":
    main()

