from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QInputDialog
import chess
from chess import Move

class ChessBoard(QWidget):
    def __init__(self):
        super().__init__()

        self.board = chess.Board()
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
                gridLayout.addWidget(button, row, col)

        self.setLayout(gridLayout)
        self.setWindowTitle('Chess Board')
        self.setGeometry(100, 100, 400, 400)

    def handle_square_click(self, square):
        if self.board.turn == chess.WHITE:
            move = self.get_user_move()
        else:
            move = self.get_random_move()

        if move in self.board.legal_moves:
            self.board.push(move)
            self.update_board()

    def get_user_move(self):
        move_text, okPressed = QInputDialog.getText(self, "Enter Move", "Enter your move in UCI notation (e.g., e2e4):")
        if okPressed:
            return Move.from_uci(move_text)

    def get_random_move(self):
        legal_moves = list(self.board.legal_moves)
        return legal_moves[0] if legal_moves else None

    def update_board(self):
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if isinstance(widget, QPushButton):
                row, col, _, _ = self.layout().getItemPosition(i)
                square = chess.square(col, 7 - row)
                piece = self.board.piece_at(square)
                label = str(piece) if piece else ''
                widget.setText(label)

if __name__ == '__main__':
    app = QApplication([])
    chessBoard = ChessBoard()
    chessBoard.show()
    app.exec_()
