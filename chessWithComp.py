from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QTimer
import chess
from chess import Move
import os
import random

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
        self.engine = ChessEngine(max_depth=3)  # Adjust depth as needed
        self.initUI()

    def initUI(self):
        gridLayout = QGridLayout()

        for row in range(8):
            for col in range(8):
                square = chess.square(col, 7 - row)
                piece = self.board.piece_at(square)
                button = QPushButton()
                button.setFixedSize(100, 80)
                button.clicked.connect(lambda _, sq=square: self.handle_square_click(sq))
                button.setObjectName(f'button_{row}_{col}')
                self.set_piece_icon(button, piece)

                if (row + col) % 2 == 0:
                    button.setStyleSheet("background-color: white;")
                else:
                    button.setStyleSheet("background-color: gray;")

                gridLayout.addWidget(button, row, col)

        self.setLayout(gridLayout)
        self.setWindowTitle('Chess Board')
        self.setGeometry(50, 30, 400, 400)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.make_random_move)
        self.timer.start(2000)  # Adjust the interval (milliseconds) as needed

    def make_random_move(self):
        if self.board.turn == chess.BLACK:
            legal_moves = list(self.board.legal_moves)
            if legal_moves:
                random_move = random.choice(legal_moves)
                self.board.push(random_move)
                self.update_board()
                print(f"White's move: {random_move}")

    def handle_square_click(self, square):
        print(f"Selected Square: {square}")

        if self.selected_square is None:
            if self.board.piece_at(square) and self.board.piece_at(square).color == self.board.turn:
                self.selected_square = square
                self.highlight_legal_moves()
        else:
            move = Move(self.selected_square, square)
            print(f"Attempted Move: {move}")
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
                    if any(m.from_square == square for m in self.board.legal_moves):
                        button.setStyleSheet("background-color: lightgreen;")
                    else:
                        if (row + col) % 2 == 0:
                            button.setStyleSheet("background-color: white;")
                        else:
                            button.setStyleSheet("background-color: gray;")

    def update_board(self):
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if isinstance(widget, QPushButton):
                row, col, _, _ = self.layout().getItemPosition(i)
                square = chess.square(col, 7 - row)
                piece = self.board.piece_at(square)
                self.set_piece_icon(widget, piece)

    def set_piece_icon(self, button, piece):
        if piece:
            color = 'w' if piece.color == chess.WHITE else 'b'
            piece_type = piece.symbol().lower()
            image_name = f"{color}_{piece_type}.png"

            current_directory = os.getcwd()
            relative_path = os.path.join('images', image_name)
            image_path = os.path.join(current_directory, relative_path)

            try:
                pixmap = QPixmap(image_path)
                if pixmap.isNull():
                    print(f"Image not loaded: {image_path}")
                else:
                    button.setIcon(QIcon(pixmap))
                    button.setIconSize(pixmap.size())
            except Exception as e:
                print(f"Error loading image: {e}")
        else:
            button.setIcon(QIcon())

if __name__ == '__main__':
    app = QApplication([])
    chessBoard = ChessBoard()
    chessBoard.show()
    app.exec_()
