import chess
from .functions import calculate_score

def predict(board, depth, is_ai):
    '''
    Recursively predicts the best move for the AI using the minimax algorithm.

    Parameters:
    - board: The chess board representing the current state of the game.
    - depth (int): The depth of the minimax search tree.
    - is_ai (bool): Indicates whether the current player is the AI (True) or the opponent (False).

    Returns:
    tuple: A tuple containing the best move (chess.Move) and its corresponding evaluation score.
           The evaluation score is based on the current board position and the specified depth.
    '''
    if depth == 0 or board.is_game_over():
        chessai_score = calculate_score(board, chess.BLACK)
        player1_score = calculate_score(board, chess.WHITE)
        return None, chessai_score - player1_score
    
    eval = -1*float('inf') if is_ai else float('inf')
    best_move = None
    for move in board.legal_moves:
        board.push(move)
        _, curr_eval = predict(board, depth - 1, not is_ai)
        board.pop()
        if is_ai:
            if curr_eval > eval:
                eval = curr_eval
                best_move = move
        else:
            if curr_eval < eval:
                eval = curr_eval
                best_move = move
    return best_move, eval
