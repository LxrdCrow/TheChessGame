import pygame as pg
from constants import TILE_SIZE, BOARD_WIDTH, BOARD_HEIGHT
from utils.assets import get_piece_image

class Piece:
    def __init__(self, piece_type, color, position):
        self.type = piece_type  # 'pawn', 'rook', 'knight', 'bishop', 'queen', 'king'
        self.color = color      # 'white' or 'black'
        self.position = position  # (row, col)
        self.has_moved = False
        self.image = get_piece_image(color, piece_type)

    def _is_on_board(self, r, c):
        # Check if the position is within the board boundaries
        return 0 <= r < BOARD_HEIGHT and 0 <= c < BOARD_WIDTH

    def get_valid_moves(self, board):
        # Return a list of valid moves for this piece
        moves = []
        row, col = self.position

        if self.type == 'pawn':
            direction = -1 if self.color == 'white' else 1
            # Move forward one square
            if self._is_on_board(row + direction, col) and board.tiles[row + direction][col] is None:
                moves.append((row + direction, col))
                # Move forward two squares from starting position
                if not self.has_moved and self._is_on_board(row + 2 * direction, col) and board.tiles[row + 2 * direction][col] is None:
                    moves.append((row + 2 * direction, col))
            # Capture diagonally
            for dc in [-1, 1]:
                r, c = row + direction, col + dc
                if self._is_on_board(r, c):
                    target = board.tiles[r][c]
                    if target and target.color != self.color:
                        moves.append((r, c))

        elif self.type == 'rook':
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while self._is_on_board(r, c):
                    target = board.tiles[r][c]
                    if target is None:
                        moves.append((r, c))
                    elif target.color != self.color:
                        moves.append((r, c))
                        break
                    else:
                        break
                    r += dr
                    c += dc

        elif self.type == 'knight':
            knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                            (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for dr, dc in knight_moves:
                r, c = row + dr, col + dc
                if self._is_on_board(r, c):
                    target = board.tiles[r][c]
                    if target is None or target.color != self.color:
                        moves.append((r, c))

        elif self.type == 'bishop':
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while self._is_on_board(r, c):
                    target = board.tiles[r][c]
                    if target is None:
                        moves.append((r, c))
                    elif target.color != self.color:
                        moves.append((r, c))
                        break
                    else:
                        break
                    r += dr
                    c += dc

        elif self.type == 'queen':
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                          (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                while self._is_on_board(r, c):
                    target = board.tiles[r][c]
                    if target is None:
                        moves.append((r, c))
                    elif target.color != self.color:
                        moves.append((r, c))
                        break
                    else:
                        break
                    r += dr
                    c += dc

        elif self.type == 'king':
            king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1),
                          (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in king_moves:
                r, c = row + dr, col + dc
                if self._is_on_board(r, c):
                    target = board.tiles[r][c]
                    if target is None or target.color != self.color:
                        moves.append((r, c))
            # Castling moves can be added here

        return moves
