import pygame as pg
from typing import Tuple, Optional
from src.game.board import Board
from src.game.pieces import Piece
from src.game.rules import Rules

Position = Tuple[int, int]


class Move:
    def __init__(self, board: Board, start_pos: Position, end_pos: Position):
        self.board = board
        self.start_pos = start_pos  # (row, col)
        self.end_pos = end_pos      # (row, col)
        self.piece_moved: Optional[Piece] = board.tiles[start_pos[0]][start_pos[1]]
        self.piece_captured: Optional[Piece] = board.tiles[end_pos[0]][end_pos[1]]

    def is_valid(self) -> bool:
        """Checks whether the move is valid."""
        if not self.piece_moved:
            return False

        # check that the correct color is moving
        if self.piece_moved.color != self.board.current_player.color:
            return False

        # use the centralized Rules class to validate the move
        return Rules.is_valid_move(self.board, self.piece_moved, self.start_pos, self.end_pos)

    def execute(self) -> bool:
        """
        Executes the move on the board if it is valid.
        Note: this does NOT switch the turn — that is handled by GameState.apply_move.
        """
        if not self.is_valid():
            # debug log
            print(f"Move not valid: {self.start_pos} -> {self.end_pos}")
            return False

        start_r, start_c = self.start_pos
        end_r, end_c = self.end_pos

        # handle en-passant capture or normal capture (Rules should have already allowed the move)
        captured = self.board.tiles[end_r][end_c]

        # if the move is en-passant, Rules.is_valid_move may have set board.en_passant_target
        if (self.piece_moved.type.lower() == "pawn"
                and self.board.en_passant_target == (end_r, end_c)
                and captured is None):
            # capture the pawn "behind" the landing square
            if self.piece_moved.color == "white":
                capture_row = end_r + 1
            else:
                capture_row = end_r - 1
            captured = self.board.tiles[capture_row][end_c]
            if captured:
                self.board.tiles[capture_row][end_c] = None
                self.board.captured_pieces.append(captured)

        # normal capture
        if captured is not None and captured is not self.piece_moved:
            # remove the captured piece from the board and store it
            self.board.captured_pieces.append(captured)

        # move the piece
        self.board.tiles[end_r][end_c] = self.piece_moved
        self.board.tiles[start_r][start_c] = None
        self.piece_moved.position = (end_r, end_c)
        self.piece_moved.has_moved = True

        # handle pawn promotion (Rules provides the routine)
        if self.piece_moved.type.lower() == "pawn":
            Rules.check_pawn_promotion(self.board, self.piece_moved)

        # update en passant target (Board.update_en_passant is preferred)
        if hasattr(self.board, "update_en_passant"):
            self.board.update_en_passant(self.piece_moved, self.start_pos, self.end_pos)
        else:
            # fallback: simple handling if the method is missing
            if abs(end_r - start_r) == 2 and self.piece_moved.type.lower() == "pawn":
                mid_row = (start_r + end_r) // 2
                self.board.en_passant_target = (mid_row, start_c)
            else:
                self.board.en_passant_target = None

        # record last_move on the board for HUD/debug
        self.board.last_move = {
            "piece": self.piece_moved,
            "start": self.start_pos,
            "end": self.end_pos,
            "captured": captured
        }

        # do NOT switch turns here: GameState.apply_move() handles that
        print(f"Move executed: {self.piece_moved.type} {self.start_pos} -> {self.end_pos}")
        return True
