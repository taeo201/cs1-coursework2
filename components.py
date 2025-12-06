"""DOCSTRING: Components for Orthello Game Logic"""

def initialize_board(size: int=10):
    if size % 2 == 1:
        size += 1
    board = []
    center1 = size // 2 -1
    center2  = size // 2
    for i in range(size):
        row = []
        for _ in range(size):
            row.append("None")
        if i == center1:
            row[center1] = "Light"
            row[center2] = "Dark"
        if i == center2:
            row[center1] = "Dark"
            row[center2] = "Light"
        board.append(row)

    return board


def get_board_display(board):
    size = len(board)
    display_board = []
    for i in range(size):
        row = ""
        for j in range(size):
            if board[i][j] == "Light":
                row += "L "
            elif board[i][j] == "Dark":
                row += "D "
            else:
                row += "- "
        display_board.append(row)
    return display_board


def print_board(board: list):
    display_board = get_board_display(board)
    for row in display_board:
        print(row)


def legal_move(colour: str, coordinate: tuple, board, output=False, debug=False):
    x = coordinate[0]
    y = coordinate[1]
    if debug:
        print(f"For coords ({x}, {y})")
    if board[y][x] != "None":
        if debug:
            print("Space Occupied")
        if output:
            print("Move not legal, enter another.")
        return False, []
    opp_tile_coords = check_surrounding_tiles(board, colour, x, y)
    #print("Coords:", oppTileCoords)
    if not opp_tile_coords:
        if debug:
            print("No Surrounding Tiles")
        if output:
            print("Move not legal, enter another.")
        return False, []
    bool_list, end_points_list = check_line(board, colour, x, y, opp_tile_coords)
    if True not in bool_list:
        if debug:
            print("No Line")
        if output:
            print("Move not legal, enter another.")
        return False , []
    return True, end_points_list

def check_if_any_legal(board, colour):
    size = len(board)
    for i in range(size):
        for j in range(size):
            is_legal = legal_move(colour, (j, i), board)[0]
            if is_legal:
                return True
    return False

def check_surrounding_tiles(board, colour, x, y):
    board_size = len(board)
    opp_tile_coords = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nx = x + j
            ny = y + i
            if not (0 <= nx < board_size and 0 <= ny < board_size):
                continue
            if board[ny][nx] not in [colour, "None"]:
                opp_tile_coords.append([nx, ny])

    return opp_tile_coords

def check_line(board, colour, x, y, opp_tile_coords):
    board_size = len(board)
    bool_list = []
    end_points_list = []

    for opp_x, opp_y in opp_tile_coords:
        dx = opp_x - x
        dy = opp_y - y
        nx, ny = opp_x, opp_y
        between = 0
        end = False

        while 0 <= nx < board_size and 0 <= ny < board_size:
            if board[ny][nx] == colour:
                break
            if board[ny][nx] == "None":
                end = True
                break
            between += 1
            nx += dx
            ny += dy


        if (not end and 0 <= nx < board_size and 0 <= ny < board_size and
                board[ny][nx] == colour and between >= 1):
            bool_list.append(True)
            end_points_list.append((nx, ny))
        else:
            bool_list.append(False)

    return bool_list, end_points_list

def count_tiles(board):
    size = len(board)
    light_tiles = 0
    dark_tiles = 0
    for i in range(size):
        for j in range(size):
            tile = board[j][i]
            if tile == "Dark":
                dark_tiles += 1
            elif tile == "Light":
                light_tiles += 1
    return {"Dark": dark_tiles, "Light": light_tiles}


def switch_player(current_player):
    if current_player == "Dark":
        return "Light"
    return "Dark"


def flip_tile(board, x, y):
    if board[y][x] == "Light":
        board[y][x] = "Dark"
    else:
        board[y][x] = "Light"

def flip_tiles_between(board, start_coords:tuple, end_coords:tuple):
    x_change = end_coords[0] - start_coords[0]
    y_change = end_coords[1] - start_coords[1]
    x_temp = start_coords[0]
    y_temp = start_coords[1]
    x_delta = y_delta = 0
    if x_change != 0:
        x_delta = int(x_change / abs(x_change))
    if y_change != 0:
        y_delta = int(y_change / abs(y_change))
    while True:
        x_temp += x_delta
        y_temp += y_delta
        if (x_temp, y_temp) == end_coords:
            break
        flip_tile(board, x_temp, y_temp)

def play_move(board, coords, colour, end_points_list=None):
    if not end_points_list:
        end_points_list = legal_move(colour, coords, board)[1]
    board[coords[1]][coords[0]] = colour
    for end_point in end_points_list:
        flip_tiles_between(board, coords, end_point)

if __name__ == "__main__":
    BOARD = initialize_board(10)
    BOARD[9][9] = "Dark"
    BOARD[8][8] = "Light"
    print_board(BOARD)
    print(legal_move("Dark", (7, 7), BOARD))
