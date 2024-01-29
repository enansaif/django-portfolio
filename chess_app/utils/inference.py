import numpy as np
from onnxruntime import InferenceSession
from .functions import board_repr, move_gen

def predict(board):
    for move in board.legal_moves:
        board.push(move)
        if board.is_checkmate():
            return board.pop()
        board.pop()
    path = "chess_app/static/chess_app/models/chess_model.onnx"
    session = InferenceSession(path, providers=["CPUExecutionProvider"])
    inputs = {session.get_inputs()[0].name: board_repr(board)}
    outs = session.run(None, inputs)
    pred = np.squeeze(outs[0])
    move = move_gen(pred, board)
    board.push_uci(move)
    return board.pop()
