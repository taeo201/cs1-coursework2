"""DOCSTRING: AI logic for Othello game."""

from time import sleep
from components import (
    initialize_board,
    print_board,
    legal_move,
    play_move,
    count_tiles,
)
from game_engine_ai import cli_coords_input


def ai_turn(board, colour, ai_depth):
    best_move = get_best_move(board, colour, ai_depth, colour)[0]
    play_move(board, best_move, colour)


def get_best_move(board, colour, depth, ai_colour):
    if colour == "Dark":
        player_colour = "Light"
    else:
        player_colour = "Dark"

    legal_list = find_all_legal(board, colour)

    if depth == 0 or not legal_list:
        score_dict = count_tiles(board)
        return None, score_dict[colour] - score_dict[player_colour]

    best_move = None

    if colour == ai_colour:
        max_score = float('-inf')
        for move, new_board in legal_list:
            score = get_best_move(new_board, player_colour, depth - 1, ai_colour)[1]
            if score > max_score:
                max_score = score
                best_move = move
        return best_move, max_score
    min_score = float('inf')
    for move, new_board in legal_list:
        score = get_best_move(new_board, ai_colour, depth - 1, ai_colour)[1]
        if score < min_score:
            min_score = score
            best_move = move
    return best_move, min_score


def copy_board(board):
    return [row[:] for row in board]


def find_all_legal(board, colour):
    legal_moves = []
    for y in range(len(board)):
        for x in range(len(board)):
            temp_board = copy_board(board)
            is_legal, end_points_list = legal_move(colour, (x, y), temp_board)
            if is_legal:
                play_move(temp_board, (x, y), colour, end_points_list)
                legal_moves.append([(x, y), temp_board])
    return legal_moves


if __name__ == "__main__":
    BOARD = initialize_board()
    while True:
        print_board(BOARD)
        X, Y = cli_coords_input(BOARD)
        BOARD[Y][X] = "Dark"
        print_board(BOARD)
        ai_turn(BOARD, "Light", ai_depth=1)
        sleep(0.5)
        print("-----------------------")
