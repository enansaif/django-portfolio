import chess
import random
from .utils import minimax
from .utils import inference
from .utils.functions import get_game_state

def play(player1_move, board, predictor):
   '''
    Simulates the next move in the chess game, where the player makes a move,
    and the AI responds with its move. Returns the updated game state.

    Parameters:
    - player1_move (str): The move made by the human player in Universal Chess Interface (UCI) format.
    - board: The chess board representing the current state of the game.
    - predictor: The AI algorithm used for predicting the AI's move. Options: 'minimax', 'random'.

    Returns:
    dict: A dictionary containing information about the updated game state,
         including legal moves, promotions, current board position in Forsyth-Edwards Notation (FEN),
         game over status, and check status.
   '''
   
   board.push(chess.Move.from_uci(player1_move))
   if board.legal_moves:
      copy_board = chess.Board(board.fen())
      if predictor == 'minimax':
         move, _ = minimax.predict(copy_board, depth=2, is_ai=True)
      elif predictor == 'chessai':
         move = inference.predict(copy_board)
      else:
         move = random.choice(list(board.legal_moves))
      board.push(move)

   game_state = get_game_state(board)
   return game_state
