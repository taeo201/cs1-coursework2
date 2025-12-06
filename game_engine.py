"""DOCSTRING: Game engine for Othello/Reversi using AI components."""

from components import (initialize_board, legal_move, switch_player,
                        play_move, print_board, check_if_any_legal, count_tiles)
#pylint doesn't like me to use import *

def cli_coords_input(board):
    size = len(board)
    valid = False
    coords_tuple = ()
    while not valid:
        coords = input("Input Coordinates For Your Move, In Format \"x,y\": ")
        coords = coords.replace(" ", "")
        coords = coords.split(",")
        if len(coords) != 2:
            print("Incorrect Format. \nCoordinates Must Be Formatted As \"x,y\"")
            continue
        try:
            for i in range(len(coords)):
                coords[i] = int(coords[i])
                if coords[i] not in range(0, size):
                    raise IndexError("Out of Range")
        except TypeError:
            print(f"Coordinates Must Be Integers between 0 and {size-1}")
            continue
        except IndexError:
            print(f"Coordinates Must Be Integers between 0 and {size-1}")
            continue
        coords_tuple = (coords[0], coords[1])
        valid = True
    return coords_tuple

def simple_game_loop(board_size, max_turns):
    print("Welcome To Othello!")
    board = initialize_board(board_size)
    move_count = max_turns
    current_player = "Light"
    coords = ()
    end_points_list = []
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
        legal = False
        while not legal:
            coords = cli_coords_input(board)
            legal, end_points_list = legal_move(current_player, coords, board, output=True)
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
    #print(cli_coords_input())
    BOARDSIZE = 10
    MAXTURNS = 60
    simple_game_loop(BOARDSIZE, MAXTURNS)
