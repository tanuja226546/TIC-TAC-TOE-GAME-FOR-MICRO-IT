import math
import random

def print_board(board):
    """Display the board."""
    print("\n")
    for i, row in enumerate(board):
        print(" | ".join(row))
        if i < 2:
            print("-" * 9)
    print("\n")

def check_win(board, player):
    """Check if player has won."""
    # Check rows and columns
    for i in range(3):
        if all([cell == player for cell in board[i]]):  # Check row
            return True
        if all([board[j][i] == player for j in range(3)]):  # Check column
            return True
    # Check diagonals
    if all([board[i][i] == player for i in range(3)]) or \
       all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def is_draw(board):
    """Return True if the board is full (draw)."""
    return all(cell != " " for row in board for cell in row)

def minimax(board, depth, is_maximizing):
    """Minimax algorithm to choose the best move for AI."""
    if check_win(board, "O"):
        return 10 - depth
    if check_win(board, "X"):
        return depth - 10
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    best_score = min(best_score, score)
        return best_score

def get_best_move(board):
    """Determine the best move for the AI."""
    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    # In rare cases if move is still None, pick a random empty space
    if move is None:
        empty = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
        move = random.choice(empty)
    return move

def player_move(board, player):
    """Get a valid move from the player."""
    while True:
        try:
            row = int(input(f"Player {player}, enter row (0-2): "))
            col = int(input(f"Player {player}, enter column (0-2): "))
            if row not in range(3) or col not in range(3):
                print("Invalid input! Please enter numbers between 0 and 2.")
                continue
            if board[row][col] != " ":
                print("This cell is already taken. Choose another.")
                continue
            board[row][col] = player
            break
        except ValueError:
            print("Please enter a valid number.")

def game_loop(mode):
    """Main game loop, mode '1' for single-player or '2' for two-player."""
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    print_board(board)

    while True:
        if mode == "2" or (mode == "1" and current_player == "X"):
            # Human move
            player_move(board, current_player)
        else:
            # AI move
            print("AI is making a move...")
            i, j = get_best_move(board)
            board[i][j] = "O"

        print_board(board)

        # Check win or draw
        if check_win(board, current_player):
            if mode == "1" and current_player == "O":
                print("AI wins!")
            else:
                print(f"Player {current_player} wins!")
            break
        if is_draw(board):
            print("It's a draw!")
            break

        # Switch turn
        current_player = "O" if current_player == "X" else "X"

def main():
    """Main function to select game mode and start the game loop."""
    print("Welcome to the Enhanced Tic-Tac-Toe Game!")
    while True:
        print("Select mode:")
        print("1. Single Player (You vs AI)")
        print("2. Two Players (Player X vs Player O)")
        mode = input("Enter 1 or 2: ").strip()
        if mode not in ["1", "2"]:
            print("Invalid selection. Please enter 1 or 2.")
            continue
        game_loop(mode)
        # Ask if the players want to play again
        replay = input("Do you want to play again? (y/n): ").strip().lower()
        if replay != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
