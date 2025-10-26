import pygame as pg
from src.game.pieces import Piece

# TODO: Check if this module is necessary
# TODO: Check for unused functions or classes
# TODO: Add docstrings to functions and classes
# TODO: Refactor code for better readability and efficiency


class Notation:

    @staticmethod
    def pos_to_notation(pos):
        """Convert board position (row, col) to chess notation (e.g., (0,0) -> 'a8')."""
        row, col = pos
        file = chr(col + ord('a'))  # 'a' to 'h'
        rank = str(8 - row)          # '8' to '1'
        return f"{file}{rank}"

    @staticmethod
    def notation_to_pos(notation):
        """Convert chess notation (e.g., 'a8') to board position (row, col)."""
        file = notation[0]
        rank = notation[1]
        col = ord(file) - ord('a')  # 'a' to 'h' -> 0 to 7
        row = 8 - int(rank)         # '8' to '1' -> 0 to 7
        return (row, col)
    
    @staticmethod
    def move_to_notation(piece: Piece, start_pos, end_pos, capture=False):
        """Convert a move to standard chess notation."""
        piece_symbol = {
            "pawn": "",
            "rook": "R",
            "knight": "N",
            "bishop": "B",
            "queen": "Q",
            "king": "K"
        }.get(piece.type.lower(), "")

        start_notation = Notation.pos_to_notation(start_pos)
        end_notation = Notation.pos_to_notation(end_pos)

        capture_symbol = "x" if capture else ""
        return f"{piece_symbol}{start_notation}{capture_symbol}{end_notation}"
    
    @staticmethod
    def parse_move(notation):
        """Parse a move from standard chess notation to piece type and positions."""
        piece_symbols = {
            "R": "rook",
            "N": "knight",
            "B": "bishop",
            "Q": "queen",
            "K": "king"
        }

        piece_type = "pawn"  # default
        if notation[0] in piece_symbols:
            piece_type = piece_symbols[notation[0]]
            notation = notation[1:]

        capture = 'x' in notation
        notation = notation.replace('x', '')

        start_notation = notation[:2]
        end_notation = notation[2:]

        start_pos = Notation.notation_to_pos(start_notation)
        end_pos = Notation.notation_to_pos(end_notation)

        return piece_type, start_pos, end_pos, capture

                
    
 # TODO: Implement additional functions as needed for full notation support
 # TODO: Check if is the structure is correct for the project and eventually bugfixs