from flask import Flask, render_template, request, jsonify
from figures import white_pieces, white_locations, black_pieces, black_locations
from moves import *

app = Flask(__name__)

turn = 'white'

def get_board_state():
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
        board[location[1]][location[0]] = piece_symbols[piece].upper()

    for i, location in enumerate(black_locations):
        piece = black_pieces[i]
        board[location[1]][location[0]] = piece_symbols[piece].lower()

    return board

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/init', methods=['GET'])
def init():
    return jsonify({'status': 'success', 'board': get_board_state(), 'turn': turn})

@app.route('/move', methods=['POST'])
def move():
    global turn
    data = request.get_json()
    start_pos = (data['start'][0], data['start'][1])
    end_pos = (data['end'][0], data['end'][1])

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
            return jsonify({'status': 'error', 'message': 'Invalid move. Try again.'})
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
            return jsonify({'status': 'error', 'message': 'Invalid move. Try again.'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid move. It\'s not your turn or invalid piece.'})

    turn = 'black' if turn == 'white' else 'white'
    return jsonify({'status': 'success', 'board': get_board_state(), 'turn': turn})

if __name__ == "__main__":
    app.run(debug=True)
