import tkinter as tk
from tkinter import PhotoImage
from chess_pieces import King, Queen, Rook, Bishop, Knight, Pawn
import math

class ChessGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.selected_piece = None
        self.selected_piece_row = None
        self.selected_piece_col = None
        self.highlighted_cells = []

        self.title("Chess")

        self.board = [[None for _ in range(8)] for _ in range(8)]

        # Initialize the board with pieces
        self.board[7][0] = Rook("black")
        self.board[7][1] = Knight("black")
        self.board[7][2] = Bishop("black")
        self.board[7][3] = Queen("black")
        self.board[7][4] = King("black")
        self.board[7][5] = Bishop("black")
        self.board[7][6] = Knight("black")
        self.board[7][7] = Rook("black")

        self.board[0][0] = Rook("white")
        self.board[0][1] = Knight("white")
        self.board[0][2] = Bishop("white")
        self.board[0][3] = Queen("white")
        self.board[0][4] = King("white")
        self.board[0][5] = Bishop("white")
        self.board[0][6] = Knight("white")
        self.board[0][7] = Rook("white")

        for col in range(8):
            self.board[1][col] = Pawn("white")
            self.board[6][col] = Pawn("black")

        self.canvas = tk.Canvas(self, width=800, height=800)
        self.canvas.pack()

        self.draw_board()
        self.draw_pieces()

        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        colors = ["white", "light grey"]
        for row in range(8):
            for col in range(8):
                color_index = (row + col) % 2
                color = colors[color_index]
                x0, y0 = col * 100, row * 100
                x1, y1 = x0 + 100, y0 + 100
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def draw_pieces(self):
        self.piece_images = {}  # Store PhotoImage instances for each piece
        piece_images_dir = "./pieces-png"  # Replace with the actual path
        square_size = 100  # Size of each square
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    image_path = f"{piece_images_dir}/{piece.color}/{piece.symbol.lower()}.png"
                    self.piece_images[piece] = self.resize_image(image_path)
                    x, y = col * square_size + square_size // 2, row * square_size + square_size // 2
                    piece_item = self.canvas.create_image(x, y, image=self.piece_images[piece], tags="piece")
                    piece.canvas_item = piece_item
    
    def resize_image(self, image_path):
        # width = 40
        # height = 40
        # resized_image = image.subsample(width, height)
        # resized_image = image.subsample(width, height)
        image = PhotoImage(file=image_path)
        return image

    def on_click(self, event):
        col = event.x // 100
        row = event.y // 100
        print(f"Clicked on row {row}, col {col}")

        if self.selected_piece:
            if (row, col) in self.highlighted_cells:
                self.move_piece(row, col)
                self.draw_board()
                self.draw_pieces()
            self.clear_highlight()
            self.selected_piece = None
        else:
            self.selected_piece = self.board[row][col]
            if self.selected_piece:
                self.selected_piece_row, self.selected_piece_col = row, col
                moves = self.selected_piece.valid_moves(self.board, row, col)
                print(f"Valid moves: {moves}")
                self.highlighted_cells = moves
                self.draw_highlight()

    def clear_highlight(self):
        for r, c in self.highlighted_cells:
            self.canvas.delete("highlight")
        self.highlighted_cells = []

    def clear_selection(self):
        self.selected_piece = None
        self.clear_highlight()

    def move_piece(self, dest_row, dest_col):
        src_row, src_col = self.selected_piece_row, self.selected_piece_col
        piece_to_move = self.board[src_row][src_col]
        
        # Check for castling move
        if isinstance(piece_to_move, King) and abs(dest_col - src_col) == 2:
            if dest_col > src_col:
                rook_col = 7
                new_rook_col = dest_col - 1
            else:
                rook_col = 0
                new_rook_col = dest_col + 1

            
            rook_to_move = self.board[src_row][rook_col]
            self.board[src_row][new_rook_col] = rook_to_move
            self.board[src_row][rook_col] = None
            self.board[src_row][new_rook_col].has_moved = True

        if isinstance(piece_to_move, King):
            piece_to_move.has_moved = True
        
        if isinstance(piece_to_move, Rook):
            piece_to_move.has_moved = True


        # Move the selected piece
        self.board[dest_row][dest_col] = piece_to_move
        self.board[src_row][src_col] = None

    def draw_highlight(self):
        # self.clear_highlight()
        for r, c in self.highlighted_cells:
            x0, y0 = c * 100, r * 100
            x1, y1 = x0 + 100, y0 + 100
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="", outline="blue", width=3, tags="highlight")


if __name__ == "__main__":
    game = ChessGame()
    game.mainloop()
