import re
import chess
import numpy as np
from .config import piece_weights, position_weights
from .config import ltr_to_num, num_to_ltr


def get_game_state(board):
    """
    Get the current state of the chess game.

    Parameters:
    - board (chess.Board): The chess board representing the current state of the game.

    Returns:
    dict: A dictionary containing information about the game state, including legal moves,
          promotions, current board position in Forsyth-Edwards Notation (FEN),
          game over status, and check status.
    """
    all_legal_moves = [str(move) for move in board.legal_moves]
    legal_moves, promotions = set(), set()

    for move in all_legal_moves:
        if len(move) == 5:
            promotions.add(move[:4])
        legal_moves.add(move[:4])

    game_state = {
        "legal_moves": ",".join(legal_moves),
        "promotions": ",".join(promotions),
        "curr_board": board.fen(),
        "is_game_over": board.is_game_over(),
        "is_check": board.is_check(),
    }

    return game_state


def get_pieces(board, color):
    """
    Get the positions of pieces on the chess board for a specific color.

    Parameters:
    - board (chess.Board): The chess board representing the current state of the game.
    - color (chess.Color): The color for which to get the piece positions.

    Returns:
    list: A list of tuples containing piece type and position for the specified color.
    """
    positions = board.piece_map()
    white_positions = []
    black_positions = []
    for pos, piece in positions.items():
        piece_str = str(piece)
        if piece_str.isupper():
            white_positions.append((piece_str.lower(), 63 - pos))
        else:
            black_positions.append((piece_str, pos))
    if color == chess.WHITE:
        return white_positions
    return black_positions


def calculate_score(board, color):
    """
    Calculate the overall score for a player in the chess game.

    Parameters:
    - board (chess.Board): The chess board representing the current state of the game.
    - color (chess.Color): The color for which to calculate the score.

    Returns:
    int: The calculated score based on material, piece positions, and check status.
    """
    board_fen = board.board_fen()
    material_score = 0
    for piece, weight in piece_weights.items():
        if color == chess.WHITE:
            piece = piece.upper()
        material_score += board_fen.count(piece) * weight

    board_pieces = get_pieces(board, color)
    position_score = 0
    for piece, pos in board_pieces:
        position_score += position_weights[piece][pos]

    check_score = 0
    if color != board.turn:
        if board.is_check():
            check_score += 200
        if board.is_checkmate():
            check_score += 1500

    return material_score + position_score + check_score

def get_mapping(board, piece):
    s = str(board)
    s = re.sub(f"[^{piece}{piece.upper()} \n]", ".", str(board))
    s = re.sub(f"{piece}", "-1", s)
    s = re.sub(f"{piece.upper()}", "1", s)
    s = re.sub(f"\.", "0", s)

    matrix = []
    for row in s.split("\n"):
        row = row.split(" ")
        row = [int(x) for x in row]
        matrix.append(row)
    return matrix


def board_repr(board):
    pieces = ["p", "r", "n", "b", "q", "k"]
    layers = []
    for piece in pieces:
        layers.append(get_mapping(board, piece))
    np_arr = np.array(layers, dtype=np.float32)
    np_arr = np.expand_dims(np_arr, axis=0)
    return np_arr


def move_gen(pred, board):
    # Create a chess board object from the given FEN string

    # Initialize variables for the starting position
    max_score = -1 * float("inf")
    from_x, from_y = 0, 0

    # Loop through all legal moves on the board
    for move in board.legal_moves:
        move = str(move)

        # Extract row and column from the move string
        row = 8 - int(move[1])
        col = ltr_to_num[move[0]]

        # Get the score from the prediction for the current move
        cur_score = float(pred[0, row, col])

        # Update the maximum score and corresponding position if the current score is higher
        if cur_score > max_score:
            max_score = cur_score
            from_x = num_to_ltr[col]
            from_y = 8 - row

    # Build the starting position in chess notation (e.g., 'e2')
    start = from_x + str(from_y)

    # Reset max_score for the destination position
    max_score = -1 * float("inf")
    to_x, to_y = 0, 0

    # Loop through all legal moves again
    for move in board.legal_moves:
        move = str(move)

        # Check if the move starts from the previously determined starting position
        if move[:2] == start:
            # Extract row and column for the destination position
            row = 8 - int(move[3])
            col = ltr_to_num[move[2]]

            # Get the score from the prediction for the current move
            cur_score = float(pred[1, row, col])

            # Update the maximum score and corresponding position if the current score is higher
            if cur_score > max_score:
                max_score = cur_score
                to_x = num_to_ltr[col]
                to_y = 8 - row

    # Build the ending position in chess notation (e.g., 'e4')
    end = to_x + str(to_y)

    # Return the concatenated string representing the move (e.g., 'e2e4')
    return start + end
