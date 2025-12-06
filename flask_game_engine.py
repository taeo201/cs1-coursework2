"""DOCSTRING: Flask-based Othello game engine."""

import uuid
from flask import Flask, render_template, request, jsonify, session
from components import (
    initialize_board,
    check_if_any_legal,
    legal_move,
    flip_tiles_between,
    count_tiles,
    switch_player
)

app = Flask(__name__)
app.secret_key = "secret"

SERVER_INSTANCE_ID = str(uuid.uuid4())


def session_is_stale():
    return session.get("server_id") != SERVER_INSTANCE_ID


def new_game(board_size=10, max_turns=60):
    session["board"] = initialize_board(board_size)
    session["current_player"] = "Dark"
    session["move_count"] = max_turns
    session["board_size"] = board_size
    session["game_over"] = False
    session["server_id"] = SERVER_INSTANCE_ID


@app.route("/")
def index():
    if "board" not in session or session_is_stale():
        new_game()
    return render_template("index.html", game_board=session["board"])


@app.route("/move")
def move():
    if "board" not in session or session_is_stale():
        new_game()
    board = session["board"]
    move_count = session["move_count"]
    current_player = session["current_player"]

    try:
        x = int(request.args.get("x"))
        y = int(request.args.get("y"))
    except ValueError:
        return jsonify({"status": "fail", "message": "Invalid coordinates."})

    if not check_if_any_legal(board, current_player):
        msg = f"{current_player} has no legal moves."
        current_player = switch_player(current_player)
        if not check_if_any_legal(board, current_player):
            return finish_game(board)
        session["current_player"] = current_player
        return jsonify({"status": "fail", "message": msg})

    legal, end_points_list = legal_move(current_player, (x, y), board, output=True)
    if not legal:
        session["current_player"] = current_player
        return jsonify({
            "status": "fail",
            "message": f"Illegal move at ({x},{y})."
        })

    board[y][x] = current_player
    for ep in end_points_list:
        flip_tiles_between(board, (x, y), ep)

    move_count -= 1
    session["board"] = board
    session["move_count"] = move_count

    new_player = switch_player(current_player)
    session["current_player"] = new_player

    if move_count <= 0:
        return finish_game(board)

    return jsonify({
        "status": "success",
        "player": new_player,
        "board": board
    })


def finish_game(board):
    dark_tiles, light_tiles = count_tiles(board)

    if light_tiles > dark_tiles:
        result = "Light Wins!"
    elif dark_tiles > light_tiles:
        result = "Dark Wins!"
    else:
        result = "Tie!"

    message = f"Game Over!\nDark: {dark_tiles}\nLight: {light_tiles}\n{result}"
    session["game_over"] = True

    return jsonify({
        "finished": message,
        "board": board
    })


@app.route("/reset")
def reset():
    new_game()
    return jsonify({
        "status": "success",
        "board": session["board"],
        "player": session["current_player"]
    })


if __name__ == "__main__":
    app.run(debug=True)
