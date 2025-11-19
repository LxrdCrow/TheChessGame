import pygame as pg
from src.game.constants import (
    TILE_SIZE, BOARD_WIDTH, BOARD_HEIGHT,
    WHITE_TILE_COLOR, BLACK_TILE_COLOR
)
from src.game.pieces import Piece
from src.game.player import Player
from src.game.rules import Rules
from utils.assets import get_piece_image


class Board:
    def __init__(self):
        # Matrix representing the chessboard
        self.tiles = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.pieces = []
        self.selected_piece = None

        # Players and turn
        self.players = [Player("white"), Player("black")]
        self.current_player = self.players[0]  # White starts first

        # Special rule states
        self.en_passant_target = None  # position where en passant capture would land (row, col) or None
        self.last_move = None  # store last move (piece, start_pos, end_pos) for HUD/debug
        self.captured_pieces = []  # list of captured piece objects

        # optional: castling rights if you want to track them on Board
        self.castling_rights = {
            "white_k": True, "white_q": True,
            "black_k": True, "black_q": True
        }

        # Load all pieces on the board
        self.load_board()

    # INITIAL SETUP

    def load_board(self):
        """Place all pieces on the board in their starting positions."""
        piece_positions = {
            'rook': [(0, 0), (0, 7), (7, 0), (7, 7)],
            'knight': [(0, 1), (0, 6), (7, 1), (7, 6)],
            'bishop': [(0, 2), (0, 5), (7, 2), (7, 5)],
            'queen': [(0, 3), (7, 3)],
            'king': [(0, 4), (7, 4)],
            'pawn': [(1, i) for i in range(8)] + [(6, i) for i in range(8)]
        }

        for piece_type, positions in piece_positions.items():
            for pos in positions:
                color = 'white' if pos[0] < 2 else 'black'
                piece = Piece(piece_type, color, pos)
                piece.image = get_piece_image(color, piece_type)  # Load image from assets
                self.pieces.append(piece)
                self.tiles[pos[0]][pos[1]] = piece

    # DRAWING

    def draw(self, screen):
        """Draw the board and pieces on the screen."""
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                tile_color = WHITE_TILE_COLOR if (row + col) % 2 == 0 else BLACK_TILE_COLOR
                pg.draw.rect(screen, tile_color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

                piece = self.tiles[row][col]
                if piece and piece.image:
                    screen.blit(piece.image, (col * TILE_SIZE, row * TILE_SIZE))

    # GAME LOGIC

    def select_piece(self, position):
        """Select a piece on the board if it belongs to the current player."""
        row, col = position
        if not (0 <= row < BOARD_HEIGHT and 0 <= col < BOARD_WIDTH):
            self.selected_piece = None
            return

        piece = self.tiles[row][col]
        if piece and piece.color == self.current_player.color:
            self.selected_piece = piece
        else:
            self.selected_piece = None

    def move_piece(self, start_pos, end_pos):
        """Move a piece if the move is valid and handle special rules."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Basic bounds check
        if not (0 <= start_row < BOARD_HEIGHT and 0 <= start_col < BOARD_WIDTH):
            return False

        if not (0 <= end_row < BOARD_HEIGHT and 0 <= end_col < BOARD_WIDTH):
            return False

        piece = self.tiles[start_row][start_col]
        target = self.tiles[end_row][end_col]

        if not piece or piece.color != self.current_player.color:
            return False

        # Validate move using Rules
        if not Rules.is_valid_move(self, piece, start_pos, end_pos):
            return False

        # Prepare for history/last_move: record captured piece (normal capture)
        captured = target

        # Handle en passant capture:
        # If the pawn moves to en_passant_target, the captured pawn is on the same column
        # but on the row just behind the landing square.
        if piece.type.lower() == "pawn" and self.en_passant_target == (end_row, end_col) and target is None:
            if piece.color == "white":
                capture_row = end_row + 1
            else:
                capture_row = end_row - 1
            captured = self.tiles[capture_row][end_col]
            # remove captured pawn
            self.tiles[capture_row][end_col] = None
            if captured:
                self.captured_pieces.append(captured)

        # Normal capture: add to captured_pieces if present
        if target is not None:
            self.captured_pieces.append(target)

        # Move the piece
        self.tiles[end_row][end_col] = piece
        self.tiles[start_row][start_col] = None
        piece.position = (end_row, end_col)
        piece.has_moved = True

        # Handle pawn promotion (Rules.check_pawn_promotion may change piece.type)
        Rules.check_pawn_promotion(self, piece)

        # Handle castling (move the rook as well) and update castling rights
        castle_data = None
        if piece.type.lower() == "king" and abs(start_col - end_col) == 2:
            rook_start_col = 0 if end_col < start_col else 7
            rook_end_col = 3 if end_col < start_col else 5
            rook = self.tiles[start_row][rook_start_col]
            # move rook
            self.tiles[start_row][rook_start_col] = None
            self.tiles[start_row][rook_end_col] = rook
            if rook:
                rook.position = (start_row, rook_end_col)
                rook.has_moved = True
            # update castling rights for this color
            if piece.color == "white":
                self.castling_rights["white_k"] = False
                self.castling_rights["white_q"] = False
            else:
                self.castling_rights["black_k"] = False
                self.castling_rights["black_q"] = False
            castle_data = {"rook_start": rook_start_col, "rook_end": rook_end_col}

        # If a rook or king moved normally, clear appropriate castling rights
        if piece.type.lower() == "king":
            if piece.color == "white":
                self.castling_rights["white_k"] = False
                self.castling_rights["white_q"] = False
            else:
                self.castling_rights["black_k"] = False
                self.castling_rights["black_q"] = False
        if piece.type.lower() == "rook":
            if start_row == 7 and start_col == 0:  # white queenside rook initial pos
                self.castling_rights["white_q"] = False
            if start_row == 7 and start_col == 7:  # white kingside rook initial pos
                self.castling_rights["white_k"] = False
            if start_row == 0 and start_col == 0:  # black queenside rook initial pos
                self.castling_rights["black_q"] = False
            if start_row == 0 and start_col == 7:  # black kingside rook initial pos
                self.castling_rights["black_k"] = False

        # Update en passant target square
        self.update_en_passant(piece, start_pos, end_pos)

        # Store last move with useful metadata
        self.last_move = {
            "piece": piece,
            "start": start_pos,
            "end": end_pos,
            "captured": captured,
            "castle": castle_data
        }

        # Deselect
        self.selected_piece = None

        return True

    def update_en_passant(self, piece, start_pos, end_pos):
        """Set en passant target if a pawn moved two squares."""
        self.en_passant_target = None  # reset by default
        if piece.type.lower() == "pawn":
            start_row, start_col = start_pos
            end_row, end_col = end_pos
            # if pawn moved two squares, store the square it jumped over
            if abs(end_row - start_row) == 2:
                mid_row = (start_row + end_row) // 2
                self.en_passant_target = (mid_row, start_col)
            else:
                # otherwise reset
                self.en_passant_target = None

    def switch_turn(self):
        """Switch the current player."""
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def is_valid_move(self, piece, start_pos, end_pos):
        """Wrapper for checking if a move is valid via Rules."""
        return Rules.is_valid_move(self, piece, start_pos, end_pos)
