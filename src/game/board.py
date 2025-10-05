import pygame as pg
from src.game.constants import TILE_SIZE, BOARD_WIDTH, BOARD_HEIGHT, WHITE_TILE_COLOR, BLACK_TILE_COLOR
from src.game.piece import Piece
from src.game.player import Player
from utils.assets import load_image

class Board:
    def __init__(self):
        # Matrix representing the chessboard
        self.tiles = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.pieces = []
        self.selected_piece = None

        # Players and turn
        self.players = [Player("white"), Player("black")]
        self.current_player = self.players[0]  # White starts first

        # Dictionary to store preloaded piece images
        self.images = {}
        self.load_images()

        # Load all pieces on the board
        self.load_board()

    def load_images(self):
        """Load all piece images once."""
        for color in ["white", "black"]:
            for piece_type in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
                self.images[f"{color}_{piece_type}"] = load_image(f"{color}_{piece_type}.png")

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
                self.pieces.append(piece)
                self.tiles[pos[0]][pos[1]] = piece

    def draw(self, screen):
        """Draw the board and pieces on the screen."""
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                tile_color = WHITE_TILE_COLOR if (row + col) % 2 == 0 else BLACK_TILE_COLOR
                pg.draw.rect(screen, tile_color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

                piece = self.tiles[row][col]
                if piece:
                    screen.blit(self.images[f"{piece.color}_{piece.type}"], (col * TILE_SIZE, row * TILE_SIZE))

    def select_piece(self, position):
        """Select a piece on the board if it belongs to the current player."""
        row, col = position
        piece = self.tiles[row][col]
        if piece and piece.color == self.current_player.color:
            self.selected_piece = piece
        else:
            self.selected_piece = None

    def move_piece(self, start_pos, end_pos):
        """Move a piece if the move is valid and switch turn."""
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        piece = self.tiles[start_row][start_col]

        if piece and piece.color == self.current_player.color:
            if self.is_valid_move(piece, start_pos, end_pos):
                self.tiles[end_row][end_col] = piece
                self.tiles[start_row][start_col] = None
                piece.position = (end_row, end_col)
                self.selected_piece = None

                self.switch_turn()  # Switch turn after a valid move
                return True

        return False

    def switch_turn(self):
        """Switch the current player."""
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def is_valid_move(self, piece, start_pos, end_pos):
        """
        TODO: Aggiungere la logica per validare le mosse dei pezzi. (Placeholder per ora)
        TODO: Gestire catture, scacchi, arrocco, promozioni, ecc.
        TODO: Prima creare rules.py e spostare la logica lì.
        """
        return True


        