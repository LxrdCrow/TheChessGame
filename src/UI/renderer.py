import os
import pygame as pg
from src.game.constants import TILE_SIZE, BOARD_WIDTH, BOARD_HEIGHT
from src.game.pieces import Piece
from src.game.board import Board
from typing import List, Tuple

def get_piece_image(color: str, type_: str) -> pg.Surface:
    """Load and return a scaled piece image for the given color and type.

    Looks for images in an 'assets' folder using common filename patterns
    (e.g. 'assets/white_pawn.png'). Raises FileNotFoundError if none found.
    """
    c = str(color).lower()
    t = str(type_).lower()
    candidates = [
        os.path.join("assets", f"{c}_{t}.png"),
        os.path.join("assets", f"{t}_{c}.png"),
        os.path.join("assets", f"{c}{t}.png"),
    ]
    for path in candidates:
        if os.path.exists(path):
            surf = pg.image.load(path)
            surf = pg.transform.scale(surf, (TILE_SIZE, TILE_SIZE))
            return surf
    raise FileNotFoundError(f"No piece image found for {color} {type_}")

class Renderer:
    def __init__(self, board: Board):
        self.board = board
        # light / dark tile colors (you can also import from constants)
        self.colors = [(235, 209, 166), (165, 117, 81)]

    def draw_board(self, screen: pg.Surface, board) -> None:
        """Draw the chess board squares."""
        
        # --- Draw board squares ---
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                color = self.colors[(row + col) % 2]
                pg.draw.rect(
                    screen,
                    color,
                    pg.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

        # --- Draw pieces ---
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                piece = board.tiles[row][col]
                if not piece:
                    continue

                # Try to get preloaded piece image
                surf = getattr(piece, "image", None)
                if not surf or not isinstance(surf, pg.Surface):
                    # fallback: use your asset loader
                    try:
                        surf = get_piece_image(piece.color, piece.type)
                        piece.image = surf  # cache it for next frames
                    except Exception:
                        continue

                screen.blit(surf, (col * TILE_SIZE, row * TILE_SIZE))


    def highlight_square(self, screen: pg.Surface, row: int, col: int, color: Tuple[int, int, int]) -> None:
        """Draw a semi-transparent highlight over a single square"""
        highlight_surface = pg.Surface((TILE_SIZE, TILE_SIZE), pg.SRCALPHA)
        highlight_surface.fill((*color, 100))  # RGBA with alpha
        screen.blit(highlight_surface, (col * TILE_SIZE, row * TILE_SIZE))

    def draw_highlights(self, screen: pg.Surface, highlights: List[Tuple[int, int]], color: Tuple[int, int, int]) -> None:
        """Draw multiple highlights (e.g., selected square, last move squares)"""
        for row, col in highlights:
            self.highlight_square(screen, row, col, color)

    def draw_move_indicators(self, screen: pg.Surface, moves: List[Tuple[int, int]]) -> None:
        """Draw small circles to indicate legal move targets."""
        indicator_color = (0, 180, 0)
        radius = max(4, TILE_SIZE // 8)
        for row, col in moves:
            center_x = col * TILE_SIZE + TILE_SIZE // 2
            center_y = row * TILE_SIZE + TILE_SIZE // 2
            pg.draw.circle(screen, indicator_color, (center_x, center_y), radius)

    def draw_selected_piece(self, screen: pg.Surface, piece: Piece, mouse_pos: Tuple[int, int]) -> None:
        """If implementing drag, draw the dragged piece at mouse position."""
        if not piece:
            return
        surf = getattr(piece, "image", None)
        if surf is None:
            try:
                surf = pg.image.load(piece.image_path)
                surf = pg.transform.scale(surf, (TILE_SIZE, TILE_SIZE))
                piece.image = surf
            except Exception:
                return
        screen.blit(surf, (mouse_pos[0] - TILE_SIZE // 2, mouse_pos[1] - TILE_SIZE // 2))

    def draw_game_over(self, screen: pg.Surface, winner: str) -> None:
        """Draw a game over banner in the middle of the board."""
        font = pg.font.SysFont(None, 72)
        text = font.render(f"{winner} Wins!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(BOARD_WIDTH * TILE_SIZE // 2, BOARD_HEIGHT * TILE_SIZE // 2))
        screen.blit(text, text_rect)


