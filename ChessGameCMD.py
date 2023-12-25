#please type this before running the code "  pip install pyhton-chess   "
import chess
class ChessEngine:
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.transposition_table = {}

    PIECE_VALUES = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 100
    }

    def evaluate_board(self, board):
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                score += self.PIECE_VALUES[piece.piece_type]
        return score

    def alphabeta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        fen = board.fen()
        if fen in self.transposition_table:
            return self.transposition_table[fen]

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.alphabeta(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[fen] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.alphabeta(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[fen] = min_eval
            return min_eval

    def make_move(self, board):
        best_move = None
        max_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in board.legal_moves:
            board.push(move)
            eval = self.alphabeta(board, self.max_depth, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)

        return best_move

# Initialize the chess engine
engine = ChessEngine(max_depth=5)  # Adjust depth as needed

# Initialize the chessboard
board = chess.Board()

# Game loop
while not board.is_game_over():
    print(board)

    move = None

    if board.turn == chess.WHITE:
        # Human player's move
        move_uci = input("Enter your move in UCI notation (e.g. e2e4): ").lower()

        if len(move_uci) == 4 and move_uci[0] in chess.FILE_NAMES and move_uci[2] in chess.FILE_NAMES \
                and move_uci[1] in chess.RANK_NAMES and move_uci[3] in chess.RANK_NAMES:
            from_square = chess.square(ord(move_uci[0]) - ord('a'), int(move_uci[1]) - 1)
            to_square = chess.square(ord(move_uci[2]) - ord('a'), int(move_uci[3]) - 1)
            move = chess.Move(from_square, to_square)

            if move in board.legal_moves:
                board.push(move)
            else:
                print("Illegal move, try again.")
        else:
            print("Invalid move format, try again.")
    else:
        # Engine's move
        best_move = engine.make_move(board)
        board.push(best_move)

print("Game Over")
print("Result: ", board.result())
