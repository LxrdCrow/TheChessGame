import pygame as pg
from typing import Optional, Iterable, Tuple
from src.game.constants import TILE_SIZE, BOARD_WIDTH, BOARD_HEIGHT, WHITE_TILE_COLOR, BLACK_TILE_COLOR
from src.utils.assets import get_piece_image

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
        self.legend_images = {f"{c}_{p}": get_piece_image(c, p) for c, p in self.legend_order}

    def _prepare_highlight_surfaces(self):
        """ Create semi-transparent surfaces for highlighting squares"""
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
        """ Main draw method. Call every frame after the board/renderer draws"""
        # draw current turn
        self._draw_turn(screen)

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

    def _draw_legend(self, screen: pg.Surface):
        """Draw small piece icons and labels in a vertical legend at the right side of the board"""
        # position the legend at top-right 
        sw = screen.get_width()
        x = sw - (TILE_SIZE + self.margin)
        y = self.margin

        for key in self.legend_images:
            img = self.legend_images.get(key)
            if img:
                screen.blit(img, (x, y))
            else:
                # draw and empty placeholder rect if image missing
                pg.draw.rect(screen, (80, 80, 80), (x, y, TILE_SIZE, TILE_SIZE), 1)
            y += TILE_SIZE + 6 # spacing between icons

    def _draw_selection_and_moves(self, screen: pg.Surface):
        """If a piece is selected, highlight the tile and possible moves"""
        sel = getattr(self.board, 'selected_piece', None)
        if not sel:
            return
        
        # selected piece tile
        try:
            row, col = sel.position
        except Exception:
            return
        
        # draw selection overlay
        screen.blit(self.selection_rect_surf, (col * TILE_SIZE, row * TILE_SIZE))

        # draw possible moves if the piece implements get_valid_moves(board)
        moves = []
        if hasattr(sel, "get_valid_moves"):
            try:
                moves = sel.get_valid_moves(self.board) or []
            except Exception:
                moves = []

        for (r, c) in moves:
            if 0 <= r < BOARD_HEIGHT and 0 <= c < BOARD_WIDTH:
                screen.blit(self.move_rect_surf, (c * TILE_SIZE, r * TILE_SIZE))

    def _draw_optional_info(self, screen: pg.Surface):
        """ Draws optional stuff if the board exposes properties (move_history, captured_pieces, timer, etc.)"""
        x = self.margin
        y = screen.get_height() - 20 - self.margin # small status line at bottom-left

        # move history (if available)
        last_move = getattr(self.board, "last_move", None)
        if last_move:
            # pretty print last_move if it's a tuple (piece, start, end)
            text = f"Last: {getattr(last_move[0], 'type', '?')} {last_move[1]}→{last_move[2]}"
            surf = self.font.render(text, True, pg.Color("white"))
            screen.blit(surf, (x, y))
            return
        
        # captured pieces (if available)
        captured = getattr(self.board, "captured_pieces", None)
        if captured is not None:
            text = f"Captured: {len(captured)}"
            surf = self.font.render(text, True, pg.Color("white"))
            screen.blit(surf, (x, y))
            return
        
       
    
    def show_message(self, screen: pg.Surface, text: str, pos: Tuple[int, int] = (10, 40), ttl: float = 2.0):
            """ Display a temporary message on the HUD at given position for ttl seconds"""
            surf = self.font.render(text, True, pg.Color("yellow"))
            screen.blit(surf, pos)


    def handle_event(self, event: pg.event.Event):
            """ Handle events if needed (e.g., for clicking on HUD elements)"""
            pass