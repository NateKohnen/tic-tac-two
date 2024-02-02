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

import pygame
import sys

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

def draw_grid():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 15)
        pygame.draw.line(screen, WHITE, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 15)

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

# This function returns True if playable moves remain
# It returns False otherwise
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
        if b[row][0] == b[row][1] and b[row][1] == b[row][2]:
            if b[row][0] == PLAYER:
                return -10
            elif b[row][0] == BOT:
                return 10

    # Check all columns for winning sequence
    for col in range(GRID_SIZE):
        if b[0][col] == b[1][col] and b[1][col] == b[2][col]:
            if b[0][col] == PLAYER:
                return -10
            elif b[0][col] == BOT:
                return 10

    # Check both diagonals for winning sequence
    if b[0][0] == b[1][1] and b[1][1] == b[2][2]:
        if b[1][1] == PLAYER:
            return -10
        elif b[1][1] == BOT:
            return 10

    if b[0][2] == b[1][1] and b[1][1] == b[2][0]:
        if b[1][1] == PLAYER:
            return -10
        elif b[1][1] == BOT:
            return 10

    # If no winning sequence is detected, return 0
    return 0

# Evaluates all viable resulting positions from the current board state
def minimax(b, depth, is_max, alpha, beta):
    global analysis_count
    score = evaluate(b)

    # Return score if the BOT has won
    # Subtract depth to encourage winning as quickly as possible
    if score == 10:
        return score - depth

    # Return score if the PLAYER has won
    # Add depth to encourage losing as slowly as possible
    if score == -10:
        return score + depth

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
                    best = max(best, minimax(b, depth + 1, not is_max, alpha, beta))

                    # Undo the move
                    b[i][j] = '_'

                    # Perform alpha-beta pruning
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break

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
                    best = min(best, minimax(b, depth + 1, not is_max, alpha, beta))

                    # Undo the move
                    b[i][j] = '_'

                    # Perform alpha-beta pruning
                    beta = min(beta, best)
                    if beta <= alpha:
                        break

        return best

# Returns the best possible move for the BOT
def find_best_move(b):
    best_val = -1000
    best_move = (-1, -1)

    # Evaluate all legal moves, return cell with optimal minimax value
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):

            # Check if this is a legal move
            if b[i][j] == '_':

                # Make the move
                b[i][j] = BOT

                # Store the minimax value of the move
                move_val = minimax(b, 0, False, -float('inf'), float('inf'))

                # Undo the move
                b[i][j] = '_'

                # If the value of the move just analyzed is greater than
                # the best value, update best_val and store the move coordinates
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move

def main():
    # Initialize gamestate and other variables
    player_turn = True  # True if it's the player's turn, False if it's the BOT's turn
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
            best_move = find_best_move(board)
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

if __name__ == "__main__":
    main()
