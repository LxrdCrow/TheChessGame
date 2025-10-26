import pygame as pg
from src.game.pieces import Piece

class Rules:

    @staticmethod
    def is_valid_move(board, piece: Piece, start_pos, end_pos):
        """Check if a move is valid based on piece type and game rules."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # General checks
        if start_pos == end_pos:
            return False  
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False  # out of bounds
        
        target = board.tiles[end_row][end_col]
        if target and target.color == piece.color:
            return False  # No capturing own pieces

        # Mapping for each piece type
        move_rules = {
            "pawn": Rules._is_valid_pawn_move,
            "rook": Rules._is_valid_rook_move,
            "knight": Rules._is_valid_knight_move,
            "bishop": Rules._is_valid_bishop_move,
            "queen": Rules._is_valid_queen_move,
            "king": Rules._is_valid_king_move
        }

        rule_func = move_rules.get(piece.type.lower())
        if not rule_func:
            return False

        return rule_func(board, piece, start_pos, end_pos)


    # PIECES MOVEMENT RULES

    @staticmethod
    def _is_valid_pawn_move(board, piece, start_pos, end_pos):
        """Rules for pawn movement, including en passant."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        direction = -1 if piece.color == "white" else 1  
        start_rank = 6 if piece.color == "white" else 1  # pawn starting rank 

        # Movement forward
        if start_col == end_col:
            if end_row == start_row + direction and board.tiles[end_row][end_col] is None:
                return True
            # Initial two-square move
            if start_row == start_rank and end_row == start_row + 2 * direction:
                if (board.tiles[start_row + direction][start_col] is None and 
                    board.tiles[end_row][end_col] is None):
                    return True
            return False

        # Capturing diagonally
        if abs(start_col - end_col) == 1 and end_row == start_row + direction:
            target = board.tiles[end_row][end_col]
            if target and target.color != piece.color:
                return True
            # En passant
            if hasattr(board, "en_passant_target") and board.en_passant_target == (end_row, end_col):
                return True

        return False


    @staticmethod
    def _is_valid_rook_move(board, piece, start_pos, end_pos):
        """Rules for rook movement."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if start_row != end_row and start_col != end_col:
            return False

        return Rules.is_path_clear(board, start_pos, end_pos)


    @staticmethod
    def _is_valid_knight_move(board, piece, start_pos, end_pos):
        """Rules for knight movement."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)

        # L-shape move 
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    

    @staticmethod
    def _is_valid_bishop_move(board, piece, start_pos, end_pos):
        """Rules for bishop movement."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if abs(start_row - end_row) != abs(start_col - end_col):
            return False

        return Rules.is_path_clear(board, start_pos, end_pos)
    

    @staticmethod
    def _is_valid_queen_move(board, piece, start_pos, end_pos):
        """Rules for queen movement."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)

        if row_diff != col_diff and start_row != end_row and start_col != end_col:
            return False

        return Rules.is_path_clear(board, start_pos, end_pos)
    

    @staticmethod
    def _is_valid_king_move(board, piece, start_pos, end_pos):
        """Rules for king movement, including castling."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)

        # Normal one-square move
        if max(row_diff, col_diff) == 1:
            return True

        # Castling
        if row_diff == 0 and col_diff == 2:
            if piece.has_moved:
                return False  # King has moved before

            rook_col = 0 if end_col < start_col else 7
            rook = board.tiles[start_row][rook_col]
            if not rook or rook.type.lower() != "rook" or rook.color != piece.color or rook.has_moved:
                return False  # Invalid rook for castling

            # Check clear path between king and rook
            step = 1 if rook_col == 7 else -1
            for col in range(start_col + step, rook_col, step):
                if board.tiles[start_row][col] is not None:
                    return False  # Path not clear

            # TODO: Check if king is in check before, during, or after castling
            return True

        return False


    # UTILITY FUNCTIONS

    @staticmethod
    def is_path_clear(board, start_pos, end_pos):
        """Checks if the path between start_pos and end_pos is clear (no pieces in between)."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        row_step = (end_row - start_row)
        col_step = (end_col - start_col)

        # Normalize steps to -1, 0, or 1
        row_step = 0 if row_step == 0 else (1 if row_step > 0 else -1)
        col_step = 0 if col_step == 0 else (1 if col_step > 0 else -1)

        row, col = start_row + row_step, start_col + col_step

        while (row, col) != (end_row, end_col):
            if board.tiles[row][col] is not None:
                return False
            row += row_step
            col += col_step

        return True


    # SPECIAL RULES AND CHECK LOGIC

    @staticmethod
    def check_pawn_promotion(board, piece):
        """Promote pawn if it reaches the last rank."""
        if piece.type.lower() == "pawn":
            row, _ = piece.position
            if (piece.color == "white" and row == 0) or (piece.color == "black" and row == 7):
                piece.type = "queen"  # TODO: Allow player to choose promotion piece
                print(f"{piece.color.capitalize()} pawn promoted to {piece.type}!")


    @staticmethod
    def is_in_check(board, color):
        """Return True if the given color's king is under attack."""
        # TODO: Implement check detection logic
        return False


    @staticmethod
    def is_checkmate(board, color):
        """Return True if the given color is in checkmate."""
        # TODO: Implement checkmate detection logic
        return False


    