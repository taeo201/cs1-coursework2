# Stage 3 Technical Documentation

This README contains the required Stage 3 technical details for:

- `components.py`
- `ai.py`
- `game_engine_ai.py`

Only the major non-trivial functions are included.  
All referenced flowcharts correspond to PNG files located alongside this document.  
Each flowchart filename matches the function name (e.g., `legal_move.png`, `get_best_move.png`).

---

## 1. components.py

### 1.1 `initialize_board`
**Flowchart:** `initialize_board.png`

**Description:**  
Creates the starting Othello board with the initial 4 tiles in the centre.

**Reasoning:**  
Centralising the board creation ensures a consistent initial game state and simplifies resetting or testing.

---

### 1.2 `legal_move`
**Flowchart:** `legal_move.png`

**Description:**  
Checks whether a move at coordinate `(x, y)` is legal for a given colour.  
Scans in all 8 directions to verify if a continuous line of opposing tiles ends with a tile of the same colour.

**Reasoning:**  
Validates moves according to Othello rules while avoiding unnecessary board mutations.  
Other modules rely on this to confirm legality before execution.

---

### 1.3 `play_move`
**Flowchart:** `play_move.png`

**Description:**  
Executes a legal move by placing a tile and flipping captured tiles returned by `legal_move`.

**Reasoning:**  
Separates validation from execution to avoid duplicated logic and ensure predictable tile flipping.

---

### 1.4 `flip_tiles_between`
**Flowchart:** `flip_tiles_between.png`

**Description:**  
Flips all tiles in a line between two points. Called by `play_move` after a move is confirmed legal.

**Reasoning:**  
Encapsulates the flipping logic in one function to keep `play_move` concise and maintainable.

---

### 1.5 `check_line`
**Flowchart:** `check_line.png`

**Description:**  
Scans a specific line in one direction to determine if tiles can be captured. Returns endpoints if valid.

**Reasoning:**  
Keeps directional scanning modular. `legal_move` can iterate over directions without duplicating scanning logic.

---

### 1.6 `check_if_any_legal`
**Flowchart:** `check_if_any_legal.png`

**Description:**  
Checks whether there are any legal moves for a player on the current board.  

**Reasoning:**  
Used by both AI and game loop to determine turn availability. Separating this check prevents repeated full board scans.

---

### 1.7 `count_tiles`
**Flowchart:** `count_tiles.png`

**Description:**  
Counts tiles of each colour and returns a dictionary.

**Reasoning:**  
Used for both scoring and AI evaluation heuristics. Keeping it simple ensures recursive minimax in `get_best_move` runs efficiently.

---

## 2. ai.py

### 2.1 `ai_turn`
**Flowchart:** `ai_turn.png`

**Description:**  
Wrapper for AI play. Calls `get_best_move` and executes the move using `play_move`.

**Reasoning:**  
Encapsulates AI behaviour in one function, simplifying integration with CLI or other interfaces.

---

### 2.2 `get_best_move`
**Flowchart:** `get_best_move.png`

**Description:**  
Recursive minimax-like search:

1. Finds legal moves via `find_all_legal`.
2. Recursively evaluates successor boards.
3. Maximises/minimises based on the current player.
4. Uses tile count difference as a heuristic.
5. Returns the best move and its score.

**Reasoning:**  
Provides AI decision-making for perfect-information two-player games. Board copies prevent mutation during recursion.

---

### 2.3 `find_all_legal`
**Flowchart:** `find_all_legal.png`

**Description:**  
Generates all legal moves and their resulting boards by simulating each move on a copied board.

**Reasoning:**  
Allows minimax to explore future states without affecting the actual board.

---

## 3. game_engine_ai.py (CLI Game Engine)

### 3.1 `cli_coords_input`
**Flowchart:** `cli_coords_input.png`

**Description:**  
Handles CLI input for move coordinates. Validates formatting, type, and bounds.

**Reasoning:**  
Prevents invalid input and crashes. Encapsulation avoids repeated input checks in the game loop.

---

### 3.2 `simple_game_loop`
**Flowchart:** `simple_game_loop.png`

**Description:**  
Main CLI driver. Handles:

- Board initialization
- Player and AI turns
- Legal move checking
- AI decision logic
- Player input and validation
- Turn count and game end

**Reasoning:**  
Separation of concerns between game state, AI, and input ensures maintainability and makes it easier to port to GUI/web interfaces.

---

## Flowcharts

Each major function has a corresponding PNG flowchart. Place them in the same directory as this README or in a `/flowcharts` folder. Filenames should match function names:

- initialize_board.png  
- legal_move.png  
- play_move.png  
- flip_tiles_between.png  
- check_line.png  
- check_if_any_legal.png  
- count_tiles.png  
- ai_turn.png  
- get_best_move.png  
- find_all_legal.png  
- cli_coords_input.png  
- simple_game_loop.png  

To embed images in the README:

```markdown
![Flowchart: legal_move](legal_move.png)
```
