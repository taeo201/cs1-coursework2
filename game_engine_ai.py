"""DOCSTRING: Game engine for Othello with AI integration (CLI version)."""

#from time import sleep
from components import (
    initialize_board,
    print_board,
    switch_player,
    check_if_any_legal,
    legal_move,
    play_move,
    count_tiles,
)
from ai import ai_turn


def cli_coords_input(board):
    size = len(board)
    valid = False
    while not valid:
        coords = input('Input Coordinates For Your Move, In Format "x,y": ')
        coords = coords.replace(" ", "").split(",")
        if len(coords) != 2:
            print('Incorrect Format. Coordinates Must Be Formatted As "x,y"')
            continue
        try:
            for i, val in enumerate(coords):
                coords[i] = int(val)
                if coords[i] not in range(size):
                    raise ValueError
        except ValueError:
            print(f"Coordinates Must Be Integers between 0 and {size-1}")
            continue
        coords_tuple = (coords[0], coords[1])
        valid = True
    return coords_tuple


def simple_game_loop(board_size, max_turns, player_col, ai_depth):
    print("Welcome To Othello!")
    board = initialize_board(board_size)
    move_count = max_turns
    current_player = "Light"

    while move_count > 0:
        print_board(board)
        current_player = switch_player(current_player)

        if not check_if_any_legal(board, current_player):
            print(f"{current_player} Has No Valid Moves")
            current_player = switch_player(current_player)

        if not check_if_any_legal(board, current_player):
            print("No more legal moves. Game over.")
            break

        print(f"Current player: {current_player}")

        if current_player != player_col:
            ai_colour = switch_player(player_col)
            ai_turn(board, ai_colour, ai_depth)
            # sleep(0.5)
        else:
            legal = False
            while not legal:
                coords = cli_coords_input(board)
                legal, end_points_list = legal_move(
                    current_player, coords, board, output=True
                )
            play_move(board, coords, current_player, end_points_list)

        move_count -= 1

    if move_count == 0:
        print("Out of moves. Game Over")

    score_dict = count_tiles(board)
    if score_dict["Light"] > score_dict["Dark"]:
        print("Light Wins!")
    elif score_dict["Dark"] > score_dict["Light"]:
        print("Dark Wins!")
    else:
        print("Tie!")

    print(f"Dark Tiles: {score_dict['Dark']} \nLight Tiles: {score_dict['Light']}")


if __name__ == "__main__":
    BOARD_SIZE = 10
    MAX_TURNS = 60
    PLAYER_COL = "Dark"
    AI_DEPTH = 4
    simple_game_loop(BOARD_SIZE, MAX_TURNS, PLAYER_COL, AI_DEPTH)