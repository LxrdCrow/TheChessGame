import pygame as pg
from src.game.costants import (
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
        self.en_passant_target = None  # position where en passant is allowed
        self.last_move = None  # store last move for en passant logic

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
        piece = self.tiles[row][col]
        if piece and piece.color == self.current_player.color:
            self.selected_piece = piece
        else:
            self.selected_piece = None

    def move_piece(self, start_pos, end_pos):
        """Move a piece if the move is valid and handle special rules."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        piece = self.tiles[start_row][start_col]
        target = self.tiles[end_row][end_col]

        if not piece or piece.color != self.current_player.color:
            return False

        # Validate move using Rules
        if not Rules.is_valid_move(self, piece, start_pos, end_pos):
            return False

        # Handle en passant capture
        if piece.type == "pawn" and self.en_passant_target == (end_row, end_col):
            capture_row = start_row if piece.color == "white" else start_row
            capture_row += -1 if piece.color == "white" else 1
            self.tiles[capture_row][end_col] = None

        # Move the piece
        self.tiles[end_row][end_col] = piece
        self.tiles[start_row][start_col] = None
        piece.position = (end_row, end_col)
        piece.has_moved = True

        # Handle pawn promotion
        Rules.check_pawn_promotion(self, piece)

        # Handle castling (move the rook as well)
        if piece.type == "king" and abs(start_col - end_col) == 2:
            rook_start_col = 0 if end_col < start_col else 7
            rook_end_col = 3 if end_col < start_col else 5
            rook = self.tiles[start_row][rook_start_col]
            self.tiles[start_row][rook_start_col] = None
            self.tiles[start_row][rook_end_col] = rook
            rook.position = (start_row, rook_end_col)
            rook.has_moved = True

        # Update en passant target square
        self.update_en_passant(piece, start_pos, end_pos)

        # Switch turn
        self.switch_turn()

        # Store last move
        self.last_move = (piece, start_pos, end_pos)
        self.selected_piece = None

        return True

    def update_en_passant(self, piece, start_pos, end_pos):
        """Set en passant target if a pawn moved two squares."""
        self.en_passant_target = None  # reset by default
        if piece.type == "pawn":
            start_row, start_col = start_pos
            end_row, _ = end_pos
            if abs(end_row - start_row) == 2:
                mid_row = (start_row + end_row) // 2
                self.en_passant_target = (mid_row, start_col)

    def switch_turn(self):
        """Switch the current player."""
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def is_valid_move(self, piece, start_pos, end_pos):
        """Wrapper for checking if a move is valid via Rules."""
        return Rules.is_valid_move(self, piece, start_pos, end_pos)
