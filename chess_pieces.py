class Piece:
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return self.symbol
    
    def is_valid_move(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def valid_moves(self, board, row, col):
        pass

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "K"
        self.has_moved = False

    def valid_moves(self, board, row, col):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if self.is_valid_move(r, c) and (board[r][c] is None or board[r][c].color != self.color):
                moves.append((r, c))

        # Add castling moves
        if not self.has_moved and self.color == "black" and board[7][7] and not board[7][7].has_moved:
            if board[7][5] is None and board[7][6] is None:
                moves.append((7, 6))
        if not self.has_moved and self.color == "black" and board[7][0] and not board[7][0].has_moved:
            if board[7][1] is None and board[7][2] is None and board[7][3] is None:
                moves.append((7, 2))
        
        if not self.has_moved and self.color == "white" and board[0][7] and not board[0][7].has_moved:
            if board[0][5] is None and board[0][6] is None:
                moves.append((0, 6))
        if not self.has_moved and self.color == "white" and board[0][0] and not board[0][0].has_moved:
            if board[0][1] is None and board[0][2] is None and board[0][3] is None:
                moves.append((0, 2))

        return moves



class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "Q"

    def valid_moves(self, board, row, col):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while self.is_valid_move(r, c):
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc
        return moves


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "R"
        self.has_moved = False

    def valid_moves(self, board, row, col):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while self.is_valid_move(r, c):
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc

        # Add castling moves
        if not self.has_moved and self.color == "white" and board[7][7] and not board[7][7].has_moved:
            if all(board[7][col] is None for col in range(5, 7)):
                moves.append((7, 6))
        elif not self.has_moved and self.color == "white" and board[7][0] and not board[7][0].has_moved:
            if all(board[7][col] is None for col in range(1, 4)):
                moves.append((7, 2))

        if not self.has_moved and self.color == "black" and board[0][7] and not board[0][7].has_moved:
            if all(board[0][col] is None for col in range(5, 7)):
                moves.append((0, 6))
        elif not self.has_moved and self.color == "black" and board[0][0] and not board[0][0].has_moved:
            if all(board[0][col] is None for col in range(1, 4)):
                moves.append((0, 2))

        return moves



class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "B"

    def valid_moves(self, board, row, col):
        moves = []
        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while self.is_valid_move(r, c):
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc
        return moves


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "N"

    def valid_moves(self, board, row, col):
        moves = []
        knight_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if self.is_valid_move(r, c) and (board[r][c] is None or board[r][c].color != self.color):
                moves.append((r, c))
        return moves

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.symbol = "P"

    def valid_moves(self, board, row, col, en_passant_target=None):
        moves = []

        direction = 1 if self.color == "white" else -1
        new_row = row + direction

       # Moving one step forward
        if self.is_valid_move(new_row, col) and board[new_row][col] is None:
            moves.append((new_row, col))

        # Moving two steps forward from starting position
        starting_row = 1 if self.color == "white" else 6
        if row == starting_row and self.is_valid_move(new_row, col) and board[new_row][col] is None and board[new_row + direction][col] is None:
            moves.append((new_row + direction, col))

        # Capturing diagonally
        for d_col in [-1, 1]:
            new_col = col + d_col
            if self.is_valid_move(new_row, new_col) and board[new_row][new_col] and board[new_row][new_col].color != self.color:
                moves.append((new_row, new_col))

        # En passant capture
        if en_passant_target is not None:
            target_row, target_col = en_passant_target
            if new_row == target_row and abs(col - target_col) == 1:
                moves.append((target_row, target_col))

        return moves
