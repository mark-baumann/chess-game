# Chess/game_logic.py

from chessgame.figures import white_pieces, white_locations, black_pieces, black_locations
from chessgame.moves import check_options
import os


class ChessGame:
    def __init__(self):
        self.turn_step = 0
        self.valid_moves = []
        self.counter = 0
        self.game_over = False
        self.turn = 'white'
        self.white_locations = white_locations[:]
        self.black_locations = black_locations[:]
        self.white_pieces = white_pieces[:]
        self.black_pieces = black_pieces[:]

    def print_board(self):
        # Implementierung zum Erzeugen des Schachbretts als HTML
        board = [[' ' for _ in range(8)] for _ in range(8)]
        piece_symbols = {
            'pawn': 'P',
            'rook': 'R',
            'knight': 'N',
            'bishop': 'B',
            'queen': 'Q',
            'king': 'K'
        }
        for i, location in enumerate(self.white_locations):
            piece = self.white_pieces[i]
            board[location[1]][location[0]] = piece_symbols[piece].upper()
        for i, location in enumerate(self.black_locations):
            piece = self.black_pieces[i]
            board[location[1]][location[0]] = piece_symbols[piece].lower()

        return board

    def move_piece(self, start_pos, end_pos):
        if self.turn == 'white' and start_pos in self.white_locations:
            idx = self.white_locations.index(start_pos)
            piece = self.white_pieces[idx]
            valid_moves = check_options([piece], [start_pos], self.turn)[0]

            if end_pos in valid_moves:
                self.white_locations[idx] = end_pos
                if end_pos in self.black_locations:
                    capture_idx = self.black_locations.index(end_pos)
                    self.black_locations.pop(capture_idx)
                    self.black_pieces.pop(capture_idx)
                self.turn = 'black'
                self.turn_step += 1
                return True
        elif self.turn == 'black' and start_pos in self.black_locations:
            idx = self.black_locations.index(start_pos)
            piece = self.black_pieces[idx]
            valid_moves = check_options([piece], [start_pos], self.turn)[0]

            if end_pos in valid_moves:
                self.black_locations[idx] = end_pos
                if end_pos in self.white_locations:
                    capture_idx = self.white_locations.index(end_pos)
                    self.white_locations.pop(capture_idx)
                    self.white_pieces.pop(capture_idx)
                self.turn = 'white'
                self.turn_step += 1
                return True

        return False

    def get_state(self):
        return {
            'board': self.print_board(),
            'turn': self.turn
        }
