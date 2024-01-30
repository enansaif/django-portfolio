/**
 * Generates the URL for the image of a chess piece based on the piece code.
 *
 * @param {string} piece - The code representing the chess piece.
 * @returns {string} - The URL for the image of the chess piece.
 */
function pieceTheme(piece) {
  var pieces = {
    "bB" : "https://i.ibb.co/WDd0Mfb/bB.png",
    "bK" : "https://i.ibb.co/YWXYQQx/bK.png",
    "bN" : "https://i.ibb.co/2jXmX0S/bN.png",
    "bP" : "https://i.ibb.co/9m0TYr0/bP.png",
    "bQ" : "https://i.ibb.co/bWsMVms/bQ.png",
    "bR" : "https://i.ibb.co/dJ2hR5C/bR.png",
    "wB" : "https://i.ibb.co/k9PRDf6/wB.png",
    "wK" : "https://i.ibb.co/zVgcmzW/wK.png",
    "wN" : "https://i.ibb.co/9h9d7Vx/wN.png",
    "wP" : "https://i.ibb.co/J7bnzVh/wP.png",
    "wQ" : "https://i.ibb.co/vBf011T/wQ.png",
    "wR" : "https://i.ibb.co/ZSGf8JX/wR.png"
  }
  return pieces[piece]
}

/**
 * Updates the game interface based on the provided JSON data.
 *
 * @param {object} json_data - The JSON data containing information about the game state.
 */
function updateGame(json_data) {
  legal_moves = json_data["legal_moves"].split(",");
  promotions = json_data["promotions"].split(",");
  curr_board = json_data["curr_board"];
  is_game_over = json_data["is_game_over"];
  is_check = json_data["is_check"];

  let status = document.getElementById("status");
  if (is_game_over) {
    status.innerHTML =
      '<span class="bg-danger pb-1 px-2 rounded">Game Over</span>';
  } else if (is_check) {
    status.innerHTML =
      '<span class="bg-warning pb-1 px-2 rounded">Check</span>';
  } else {
    status.innerHTML =
      '<span class="bg-success pb-1 px-2 rounded">Active</span>';
  }
}

/**
 * Sends an XMLHttpRequest to a specified URL and updates the game based on the response.
 *
 * @param {string} url - The URL to send the request to.
 */
function hitURL(url, move) {
  const xhttp = new XMLHttpRequest();
  xhttp.onload = function () {
    let json_data = JSON.parse(this.responseText);
    updateGame(json_data);
    setTimeout(() => {
      board.position(curr_board);
      isMoveComplete = true;
    }, 100);
  };
  isMoveComplete = false;
  let model = document.querySelector('input[name="model"]:checked').value;
  xhttp.open("POST", url, true);
  xhttp.setRequestHeader("Content-Type", "application/json");
  xhttp.setRequestHeader("X-CSRFToken", csrf_token);
  xhttp.send(JSON.stringify({ curr_board, move, model }));
}

/**
 * Handles the drop event when a chess piece is moved on the board.
 *
 * @param {string} source - The source square of the move.
 * @param {string} target - The target square of the move.
 * @returns {string} - Returns "snapback" if the move is not legal.
 */
function onDrop(source, target) {
  let move = source + target;
  if (!legal_moves.includes(move)) {
    return "snapback";
  }

  if (promotions.includes(move)) {
    let selectedOption = document.querySelector('input[name="piece"]:checked');
    if (confirm("Promote pawn to " + selectedOption.id + "?") == false) {
      return "snapback";
    }
    move += selectedOption.value;
  }

  if (isMoveComplete) {
    hitURL(game_url, move);
  }
}

/**
 * Resets the chess game if the current move is complete.
 */
function resetGame() {
  if (isMoveComplete) {
    hitURL(reset_url, null);
  }
}

var config = {
  position: "start",
  pieceTheme: pieceTheme,
  onDrop: onDrop,
  draggable: true,
  showNotation: false,
};
var isMoveComplete = true;
var board = Chessboard("board", config);
$(window).resize(board.resize);
