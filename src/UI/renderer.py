# TODO: Work in progress


import pygame as pg
from src.game.constants import TILE_SIZE, BOARD_WIDTH, BOARD_HEIGHT
from src.game.pieces import Piece
from src.game.board import Board

class Renderer:
    def __init__(self, board: Board):
        self.board = board
        self.colors = [(235, 209, 166), (165, 117, 81)]  # Light and dark tile colors

    def draw_board(self, screen: pg.Surface, board: Board):
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                color = self.colors[(row + col) % 2]
                pg.draw.rect(screen, color, pg.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def draw_pieces(self, screen: pg.Surface, board: Board):
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                piece: Piece | None = board.get_piece_at(row, col)
                if piece:
                    piece_image = pg.image.load(piece.image_path)
                    piece_image = pg.transform.scale(piece_image, (TILE_SIZE, TILE_SIZE))
                    screen.blit(piece_image, (col * TILE_SIZE, row * TILE_SIZE))

    def highlight_square(self, screen: pg.Surface, row: int, col: int, color: tuple[int, int, int]):
        highlight_surface = pg.Surface((TILE_SIZE, TILE_SIZE), pg.SRCALPHA)
        highlight_surface.fill((*color, 100))  # Semi-transparent highlight
        screen.blit(highlight_surface, (col * TILE_SIZE, row * TILE_SIZE))

    def draw_highlights(self, screen: pg.Surface, highlights: list[tuple[int, int]], color: tuple[int, int, int]):
        for row, col in highlights:
            self.highlight_square(screen, row, col, color)

    def draw_move_indicators(self, screen: pg.Surface, moves: list[tuple[int, int]]):
        indicator_color = (0, 255, 0)
        for row, col in moves:
            center_x = col * TILE_SIZE + TILE_SIZE // 2
            center_y = row * TILE_SIZE + TILE_SIZE // 2
            pg.draw.circle(screen, indicator_color, (center_x, center_y), TILE_SIZE // 8)

    def draw_selected_piece(self, screen: pg.Surface, piece: Piece, mouse_pos: tuple[int, int]):
        piece_image = pg.image.load(piece.image_path)
        piece_image = pg.transform.scale(piece_image, (TILE_SIZE, TILE_SIZE))
        screen.blit(piece_image, (mouse_pos[0] - TILE_SIZE // 2, mouse_pos[1] - TILE_SIZE // 2))

    def draw_game_over(self, screen: pg.Surface, winner: str):
        font = pg.font.SysFont(None, 72)
        text = font.render(f"{winner} Wins!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(BOARD_WIDTH * TILE_SIZE // 2, BOARD_HEIGHT * TILE_SIZE // 2))
        screen.blit(text, text_rect)


