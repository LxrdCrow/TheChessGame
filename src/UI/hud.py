import pygame as pg
from typing import Optional, Iterable, Tuple
from src.game.constants import TILE_SIZE, BOARD_WIDTH, BOARD_HEIGHT, WHITE_TILE_COLOR, BLACK_TILE_COLOR
from utils.assets import get_piece_images

class HUD:
    """
     HUD for chess board:
      - shows current player (turn)
      - shows a small legend of piece icons
      - highlights selected piece and its legal moves (if available)
      - lightweight and resilient (doesn't require board to have move_history/captured_pieces)
    """

    def __init__(self, board, font: Optional[pg.font.Font] = None, margin: int = 8):
        """
         board: instance of your Board class
        font: optional pygame Font, default system 20px
        margin: spacing for HUD elements
        """

        self.board = board
        self.font = font or pg.font.SysFont(None, 20)
        self.margin = margin

        # colors / surfaces for highlights
        self.highlight_color = (246, 246, 105, 120) # semi-transparent yellow
        self.move_color = (50, 200, 50, 140) # semi-transparent green
        self.selection_rect_surf = None
        self.move_rect_surf = None
        self._prepare_highlight_surfaces()

        # preload a small legend - will return None if missing, so handle gracefully
        self.legend_order = [
            ("wK", "bK"),  # Kings
            ("wQ", "bQ"),  # Queens
            ("wR", "bR"),  # Rooks
            ("wB", "bB"),  # Bishops
            ("wN", "bN"),  # Knights
            ("wP", "bP"),  # Pawns
        ]
        self.legend_images = {f"{c}_{p}": get_piece_images(c, p) for c, p in self.legend_order}

    def _prepare_highlight_surfaces(self):
        """ Create semi-transparent surfaces for highlighting squares """
        # selection highlight
        s = pg.Surface((TILE_SIZE, TILE_SIZE), flags=pg.SRCALPHA)
        s.fill(self.highlight_color)
        self.selection_rect_surf = s

        # move highlight
        m = pg.Surface((TILE_SIZE, TILE_SIZE), flags=pg.SRCALPHA)
        m.fill(self.move_color)
        self.move_rect_surf = m

    # -- Drawing methods -- #
    # Create drawing methods for HUD elements
    
    def draw (self, screen: pg.Surface):
        """ Main draw method. Call every frame after the board/renderer draws."""
        # draw current turn
        self._draw_current_turn(screen)

        # draw legend on the right
        self._draw_legend(screen)

        # draw selection and possible moves overlays
        self._draw_optional_info(screen)

    def _draw_turn(self, screen: pg.Surface):
        """ Draw the current player or turn"""
        try:
            color = self.board.current_player.color.capitalize()
        except Exception:
            color = "Unknown"

        text = f"Turn: {color}"
        surf = self.font.render(text, True, pg.Color('white'))
        screen.blit(surf, (self.margin, self.margin))

    # Next task: draw legend
