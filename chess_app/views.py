import json
import chess
from django.shortcuts import render
from django.http import JsonResponse
from .utils import functions
from .game import play

def home(request):
    """
    View function for rendering the home page of the chess application.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    HttpResponse: Rendered HTML page with the current game state.
    """
    request.session['prev_state'] = ""
    game_state = functions.get_game_state(chess.Board())
    return render(request, 'chess_app/index.html', context=game_state)

def play_step(request):
    """
    View function for processing a player's move and updating the game state.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    JsonResponse: JSON response containing the updated game state after the player's move.
    """
    board = chess.Board(json.loads(request.body).get('curr_board'))
    move = json.loads(request.body).get('move')
    model = json.loads(request.body).get('model')
    request.session['prev_state'] = board.fen()
    game_state = play(move, board, model)
    return JsonResponse(game_state)

def reset_game(request):
    """
    View function for resetting the chess game to the initial state.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    JsonResponse: JSON response containing the updated game state after resetting the game.
    """
    board = chess.Board(json.loads(request.body).get('curr_board'))
    request.session['prev_state'] = board.fen()
    game_state = functions.get_game_state(chess.Board())
    return JsonResponse(game_state)

def undo_move(request):
    prev_state = request.session['prev_state']
    board = chess.Board(json.loads(request.body).get('curr_board'))
    if prev_state != "":
        board = chess.Board(prev_state)
    game_state = functions.get_game_state(board)
    return JsonResponse(game_state)
