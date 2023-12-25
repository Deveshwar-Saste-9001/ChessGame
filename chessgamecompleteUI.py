from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import Qt
import chess
from chess import Move

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

class ChessBoard(QWidget):
    def __init__(self):
        super().__init__()

        self.board = chess.Board()
        self.selected_square = None
        self.initUI()

    def initUI(self):
        gridLayout = QGridLayout()

        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row)
                piece = self.board.piece_at(square)
                label = str(piece) if piece else ''
                button = QPushButton(label)
                button.setFixedSize(50, 50)
                button.clicked.connect(lambda _, sq=square: self.handle_square_click(sq))
                button.setObjectName(f'button_{row}_{col}')
                gridLayout.addWidget(button, row, col)

        self.setLayout(gridLayout)
        self.setWindowTitle('Chess Board')
        self.setGeometry(100, 100, 400, 400)

    def handle_square_click(self, square):
        if self.selected_square is None:
            if self.board.piece_at(square) and self.board.piece_at(square).color == self.board.turn:
                self.selected_square = square
                self.highlight_legal_moves()
        else:
            move = Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.update_board()
                self.selected_square = None
                self.highlight_legal_moves()

    def highlight_legal_moves(self):
        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row)
                piece = self.board.piece_at(square)
                button = self.findChild(QPushButton, f'button_{row}_{col}')

                if button:
                    if any(move.from_square == square for move in self.board.legal_moves):
                        button.setStyleSheet("background-color: lightgreen;")
                    else:
                        button.setStyleSheet("background-color: None;")

    def update_board(self):
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if isinstance(widget, QPushButton):
                row, col, _, _ = self.layout().getItemPosition(i)
                square = chess.square(col, 7 - row)
                piece = self.board.piece_at(square)
                label = str(piece) if piece else ''
                widget.setText(label)
                widget.setStyleSheet("background-color: None;")

if __name__ == '__main__':
    app = QApplication([])
    chessBoard = ChessBoard()
    chessBoard.show()
    app.exec_()
