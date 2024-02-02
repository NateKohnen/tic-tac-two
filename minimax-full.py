# This is the final version of my tic-tac-toe algorithm for now.
# Minimax, a/b pruning, and transposition tables all seem to be working properly.
# This iteration also incorporates some slight randomness, to keep the bot from playing the same thing every time.

# DEFAULT MINIMAX SEARCH
# First move: Plays at 0, 0, 549936 positions
# Edge start: 63896 positions
# Corner start: 59696 positions
# Center start: 55496 positions

# WITH ALPHA-BETA PRUNING
# First move: Plays at 0, 0, 85908 positions
# Edge start: 17606/19412/23730/25533 positions
# Corner start: 17129/17836/19648/21042 positions
# Center start: 19471 positions

# WITH TRANSPOSITION TABLE
# First move: Plays at 2, 0, 11012 positions
# Edge start: 3417/3441/3844/3953 positions
# Corner start: 3315/3442/3483/3603 positions
# Center start: 3407 positions

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
PLAYER, BOT = 'X', 'O'
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Pygame window setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Displays the empty game grid
def draw_grid():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 15)
        pygame.draw.line(screen, WHITE, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 15)

# Marks down player and bot movements on the game board
def draw_board(board):
    font = pygame.font.Font(None, 200)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == PLAYER:
                text = font.render('X', True, WHITE)
            elif board[i][j] == BOT:
                text = font.render('O', True, WHITE)
            else:
                continue  # Skip empty cells

            # Calculate the position to center the text in the cell
            text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
            screen.blit(text, text_rect.topleft)

# Returns True if playable moves remain
def remaining_moves(b):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if b[i][j] == "_":
                return True
    return False

# Evaluates the board for winning sequences
def evaluate(b):
    # Check all rows for winning sequence
    for row in range(GRID_SIZE):
        if all(cell == PLAYER for cell in b[row]):
            return -10
        elif all(cell == BOT for cell in b[row]):
            return 10

    # Check all columns for winning sequence
    for col in range(GRID_SIZE):
        if all(b[row][col] == PLAYER for row in range(GRID_SIZE)):
            return -10
        elif all(b[row][col] == BOT for row in range(GRID_SIZE)):
            return 10

    # Check both diagonals for winning sequence
    if all(b[i][i] == PLAYER for i in range(GRID_SIZE)):
        return -10
    elif all(b[i][i] == BOT for i in range(GRID_SIZE)):
        return 10

    if all(b[i][GRID_SIZE - 1 - i] == PLAYER for i in range(GRID_SIZE)):
        return -10
    elif all(b[i][GRID_SIZE - 1 - i] == BOT for i in range(GRID_SIZE)):
        return 10

    # If no winning sequence is detected, return 0
    return 0

# Transposition table to store computed minimax values
transposition_table = {}

# Evaluates all viable resulting positions from the current board state
def minimax(b, depth, is_max, alpha, beta, max_depth):
    global analysis_count
    score = evaluate(b)

    # Check if the current board position is in the transposition table
    board_key = tuple(map(tuple, b))
    if board_key in transposition_table:
        return transposition_table[board_key]

    # Return score if the BOT has won or if the maximum depth is reached
    if score == 10 or depth == max_depth:
        return score - depth + random.uniform(-0.01, 0.01)  # Add random adjustment

    # Return score if the PLAYER has won or if the maximum depth is reached
    if score == -10 or depth == max_depth:
        return score + depth + random.uniform(-0.01, 0.01)  # Add random adjustment

    # Return 0 if there are no moves remaining AND no winner
    if not remaining_moves(b):
        return 0

    # When it is the BOT's move...
    if is_max:
        best = -1000

        # Traverse all cells
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):

                # Check if this is a legal move
                if b[i][j] == '_':

                    # Make the move
                    b[i][j] = BOT

                    # Increment analysis count
                    analysis_count += 1

                    # Call minimax recursively and store the best outcome
                    best = max(best, minimax(b, depth + 1, not is_max, alpha, beta, max_depth))

                    # Undo the move
                    b[i][j] = '_'

                    # Perform alpha-beta pruning
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break

        # Store the computed minimax value in the transposition table
        transposition_table[board_key] = best
        return best

    # When it is the PLAYER's move...
    else:
        best = 1000

        # Traverse all cells
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):

                # Check if this is a legal move
                if b[i][j] == '_':

                    # Make the move
                    b[i][j] = PLAYER

                    # Increment analysis count
                    analysis_count += 1

                    # Call minimax recursively and store the best outcome
                    best = min(best, minimax(b, depth + 1, not is_max, alpha, beta, max_depth))

                    # Undo the move
                    b[i][j] = '_'

                    # Perform alpha-beta pruning
                    beta = min(beta, best)
                    if beta <= alpha:
                        break

        # Store the computed minimax value in the transposition table
        transposition_table[board_key] = best
        return best

# Returns the best possible move for the BOT with a depth limit
def find_best_move_with_depth_limit(b, max_depth):
    best_val = -1000
    best_move = (-1, -1)

    # Evaluate all legal moves, return cell with optimal minimax value
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):

            # Check if this is a legal move
            if b[i][j] == '_':

                # Make the move
                b[i][j] = BOT

                # Store the minimax value of the move with depth limit
                move_val = minimax(b, 0, False, -float('inf'), float('inf'), max_depth)

                # Undo the move
                b[i][j] = '_'

                # If the value of the move just analyzed is greater than
                # the best value, update best_val and store the move coordinates
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move

max_depth = 9  # Adjust this as needed. On my PC, 3x3 can handle 9, 4x4 can handle 5, 5x5 can handle 3

# Initialize gamestate and other variables
player_turn = True  # True if it's the PLAYER's turn, False if it's the BOT's turn
board = [['_' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Begin counting the number of positions analyzed
global analysis_count
analysis_count = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
            x, y = event.pos
            col = x // CELL_SIZE
            row = y // CELL_SIZE
            if board[row][col] == '_':
                board[row][col] = PLAYER
                player_turn = False

    # Check for game over conditions or continue with BOT's move
    if not remaining_moves(board) or evaluate(board) != 0:

        # Handle game over
        if evaluate(board) > 0:
            victor = "the algorithm"
        elif evaluate(board) < 0:
            victor = "the player"
        else:
            victor = "neither player"
        print(f"Game over, {victor} wins")

        pygame.quit()
        sys.exit()

    if not player_turn:
        best_move = find_best_move_with_depth_limit(board, max_depth)
        board[best_move[0]][best_move[1]] = BOT
        player_turn = True

        # Print and reset the number of positions analyzed
        print(f"Positions analyzed: {analysis_count}")
        analysis_count = 0

    # Draw the board
    screen.fill(BLACK)
    draw_grid()
    draw_board(board)
    pygame.display.flip()
