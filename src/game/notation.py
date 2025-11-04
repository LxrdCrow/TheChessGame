import pygame as pg
from src.game.pieces import Piece


class Notation:
    """
    Utility class for converting board positions and moves 
    into standard chess notation (e.g., e4, Nf3, exd5).
    """

    # POSITION CONVERSIONS

    @staticmethod
    def pos_to_notation(pos):
        """
        Convert a board position (row, col) into standard chess notation.
        Example: (0, 0) -> 'a8', (7, 7) -> 'h1'
        """
        row, col = pos
        file = chr(col + ord('a'))  # Convert column index to letter
        rank = str(8 - row)         # Convert row index to rank number
        return f"{file}{rank}"

    @staticmethod
    def notation_to_pos(notation):
        """
        Convert a chess notation string into a board position tuple.
        Example: 'a8' -> (0, 0), 'h1' -> (7, 7)
        """
        file, rank = notation[0], notation[1]
        col = ord(file) - ord('a')
        row = 8 - int(rank)
        return (row, col)

    # MOVE CONVERSIONS

    @staticmethod
    def move_to_notation(piece: Piece, start_pos, end_pos, capture=False, special=None):
        """
        Convert a move to standard chess notation.
        Handles captures, castling, promotions, and special cases.
        
        Args:
            piece (Piece): The moving piece
            start_pos (tuple): (row, col) start position
            end_pos (tuple): (row, col) end position
            capture (bool): True if the move is a capture
            special (str): Optional special tag ('O-O', 'O-O-O', '=Q', etc.)
        """
        # Handle castling explicitly
        if special in ("O-O", "O-O-O"):
            return special

        piece_symbol = {
            "pawn": "",
            "rook": "R",
            "knight": "N",
            "bishop": "B",
            "queen": "Q",
            "king": "K"
        }.get(piece.type.lower(), "")

        start_not = Notation.pos_to_notation(start_pos)
        end_not = Notation.pos_to_notation(end_pos)

        capture_symbol = "x" if capture else ""

        # Pawn captures show origin file (e.g. exd5)
        if piece.type.lower() == "pawn" and capture:
            start_file = start_not[0]
            return f"{start_file}x{end_not}"

        # Promotion (e.g. e8=Q)
        if special and special.startswith("="):
            return f"{end_not}{special}"

        # Regular move
        return f"{piece_symbol}{capture_symbol}{end_not}"

    @staticmethod
    def parse_move(notation):
        """
        Parse a move in standard notation and extract its components.
        Supports:
          - Basic moves (e4, Nf3, Bb5)
          - Captures (exd5, Qxh7)
          - Castling (O-O, O-O-O)
          - Promotions (e8=Q)
        """
        piece_symbols = {
            "R": "rook",
            "N": "knight",
            "B": "bishop",
            "Q": "queen",
            "K": "king"
        }

        # Castling
        if notation in ("O-O", "O-O-O"):
            return {
                "piece_type": "king",
                "special": notation,
                "capture": False
            }

        # Promotion
        promotion = None
        if "=" in notation:
            notation, promotion = notation.split("=")
            promotion = promotion.upper()

        # Identify capture
        capture = "x" in notation
        notation = notation.replace("x", "")

        # Determine piece type
        piece_type = "pawn"
        if notation and notation[0] in piece_symbols:
            piece_type = piece_symbols[notation[0]]
            notation = notation[1:]

        # Extract start and end squares
        if len(notation) == 4:
            start_not = notation[:2]
            end_not = notation[2:]
        else:
            start_not = None
            end_not = notation[-2:]

        move_data = {
            "piece_type": piece_type,
            "start_pos": Notation.notation_to_pos(start_not) if start_not else None,
            "end_pos": Notation.notation_to_pos(end_not),
            "capture": capture,
            "promotion": promotion,
            "special": None
        }
        return move_data

    # UTILITY HELPERS

    @staticmethod
    def format_move_number(move_number, color):
        """
        Return a formatted move number (e.g., '1. e4' for white, '1... e5' for black)
        """
        if color == "white":
            return f"{move_number}. "
        else:
            return f"{move_number}... "

    @staticmethod
    def log_move(log_list, move_text, move_number, color):
        """
        Append a move to the move log in algebraic format.
        Keeps moves in pairs (e.g., '1. e4 e5', '2. Nf3 Nc6')
        """
        if color == "white":
            log_list.append(f"{move_number}. {move_text}")
        else:
            log_list[-1] += f" {move_text}"

