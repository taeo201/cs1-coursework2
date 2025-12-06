# Othello Game Engine with AI (Flask)

## Overview

This project is a web-based Othello/Reversi game built using Flask. It supports:

* Two-player games (Human vs Human)
* Single-player games (Human vs AI)
* Configurable board size and turn limits
* RESTful API endpoints to interact with the game

The code is modular, separating game logic, AI decision-making, and web server handling.

## Module Breakdown

### components.py

Handles all core Othello game rules:

* `initialize_board(size)`: Creates the starting board
* `legal_move(player, coord, board, output)`: Checks if a move is legal
* `check_if_any_legal(board, player)`: Checks if the player has any legal moves
* `play_move(board, coord, player, endpoints)`: Executes a move and flips the tiles
* `count_tiles(board)`: Counts tiles for each player
* `switch_player(player)`: Returns the opposing player

Reasoning: Centralizes game logic to make it reusable for both AI and human play.

### ai.py

Handles AI decision-making:

* `get_best_move(board, ai_col, depth, aiCol)`: Implements a minimax or heuristic-based decision
* Optional helper functions to evaluate board states and simulate moves

Reasoning: AI logic is separated so it can evolve independently of the web interface.

### flask_game_engine.py

Flask server for two-player mode:

* `new_game(board_size, max_turns)`: Starts a new game and initializes session variables
* `/move`: Handles player moves via query parameters `(x, y)`, validates legality, updates board
* `/reset`: Resets the game state
* `finish_game(board)`: Determines winner and returns final state

Flow Diagram (Two-Player Mode):

```
User clicks -> /move endpoint -> Validate move
   |-> Move legal? -> Yes -> Play move -> switch player
   |-> Move legal? -> No -> Return error
Check for game end -> return board state
```

### flask_game_engine_ai.py

Flask server for AI mode:

* Works similarly to the two-player server but integrates AI moves
* After human move, server evaluates AI moves automatically
* Uses `get_best_move` to choose AI moves

Flow Diagram (Human vs AI):

```
User clicks -> /move endpoint -> Validate move
   |-> Move legal? -> Yes -> Play human move
Check AI legal moves:
   |-> AI has legal move -> get_best_move -> Play AI move -> switch back to human
Check game end -> return board state
```

## Session Management

* Each session stores:

  * `board`: Current board state
  * `current_player`: Whose turn it is
  * `move_count`: Remaining moves
  * `ai_colour`: Color the AI plays (if any)
* `SERVER_INSTANCE_ID` ensures stale sessions are reset

Reasoning: Keeps game state independent per user, allowing multiple concurrent sessions.

## Design Choices

* Separation of Concerns: Game logic, AI, and web server are modular for maintainability
* RESTful Endpoints: Allows future GUI or mobile clients to integrate easily
* Session-based State: Simplifies user state management without a database
* AI Depth Limit: Depth-limited search keeps response times fast

## Dependencies

* Python 3.11+
* Flask (`pip install flask`)
