import pygame as pg
from src.game.board import Board
from src.game.pieces import Pawn
from src.game.rules import Rules


class Move:
    def __init__(self, board: Board, start_pos: tuple, end_pos: tuple):
        self.board = board
        self.start_pos = start_pos  # (row, col)
        self.end_pos = end_pos      # (row, col)
        self.piece_moved = board.tiles[start_pos[0]][start_pos[1]]
        self.piece_captured = board.tiles[end_pos[0]][end_pos[1]]

    def is_valid(self):
        """Check if the move is valid or not."""
        if not self.piece_moved:
            return False  

        if self.piece_moved.color != self.board.current_player.color:
            return False  # The piece does not belong to the current player

        # Use the Rules class to validate the move
        return Rules.is_legal_move(self.board, self.piece_moved, self.start_pos, self.end_pos)

    def execute(self):
        """Execute the move if it's valid."""
        if not self.is_valid():
            print(f"Move not valid: {self.start_pos} → {self.end_pos}")
            return False

        # If a piece is captured, add it to the captured pieces list
        if self.piece_captured:
            self.board.captured_pieces.append(self.piece_captured)

        # Update board state
        self.board.tiles[self.end_pos[0]][self.end_pos[1]] = self.piece_moved
        self.board.tiles[self.start_pos[0]][self.start_pos[1]] = None
        self.piece_moved.position = self.end_pos

        # Promote pawn if it reaches the last rank
        if isinstance(self.piece_moved, Pawn):
            if (self.piece_moved.color == "white" and self.end_pos[0] == 0) or \
               (self.piece_moved.color == "black" and self.end_pos[0] == 7):
                Rules.promote_pawn(self.board, self.piece_moved)

        # Switch turn to the other player
        self.board.current_player = (
            self.board.players[1]
            if self.board.current_player == self.board.players[0]
            else self.board.players[0]
        )

        print(f"Move executed: {self.piece_moved} {self.start_pos} → {self.end_pos}")
        return True
