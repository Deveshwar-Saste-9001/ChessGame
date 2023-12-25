from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import chess
from chess import Move
import os

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
                button = QPushButton()
                button.setFixedSize(100, 80)  
                button.clicked.connect(lambda _, sq=square: self.handle_square_click(sq))
                button.setObjectName(f'button_{row}_{col}')
                self.set_piece_icon(button, piece)
                # gridLayout.addWidget(button, row, col)

                if (row + col) % 2 == 0:
                    button.setStyleSheet("background-color: white;")
                else:
                    button.setStyleSheet("background-color: gray;")

                gridLayout.addWidget(button, row, col)

        self.setLayout(gridLayout)
        self.setWindowTitle('Chess Board')
        self.setGeometry(50, 30, 400, 400)


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
                        # button.setStyleSheet("background-color: None;")

    def update_board(self):
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            if isinstance(widget, QPushButton):
                row, col, _, _ = self.layout().getItemPosition(i)
                square = chess.square(col, 7 - row)
                piece = self.board.piece_at(square)
                self.set_piece_icon(widget, piece)

            if (row + col) % 2 == 0:
                widget.setStyleSheet("background-color: white;")
            else:
                widget.setStyleSheet("background-color: gray;")

    
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
