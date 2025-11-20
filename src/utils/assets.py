import pygame as pg
import os
from typing import Dict

SQUARE_SIZE = 80

THIS_DIR = os.path.dirname(__file__)
IMAGES_PATH = os.path.join(THIS_DIR, "images")

PIECE_TYPES = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
COLORS = ['white', 'black']

# dizionario globale con tutte le immagini caricate
PIECE_IMAGES: Dict[str, pg.Surface] = {}

_initialized = False

def _make_placeholder(color: str, piece: str, size: int) -> pg.Surface:
    surf = pg.Surface((size, size), pg.SRCALPHA)
    bg = (240, 240, 240) if color == 'white' else (60, 60, 60)
    surf.fill(bg)
    pg.draw.circle(surf, (0, 0, 0), (size // 2, size // 2), size // 3, 2)
    font = pg.font.SysFont(None, max(12, size // 4))
    text = font.render(piece[0].upper(), True, (0, 0, 0))
    text_rect = text.get_rect(center=(size // 2, size // 2))
    surf.blit(text, text_rect)
    return surf

def init_assets(square_size: int = SQUARE_SIZE) -> None:
    """Carica e scala tutte le immagini dei pezzi in PIECE_IMAGES."""
    global PIECE_IMAGES, _initialized, SQUARE_SIZE
    if _initialized:
        return
    SQUARE_SIZE = square_size

    if not pg.get_init():
        pg.init()
    if not pg.font.get_init():
        pg.font.init()

    for color in COLORS:
        for piece in PIECE_TYPES:
            key = f"{color}_{piece}"
            filename = f"{key}.png"
            path = os.path.join(IMAGES_PATH, filename)
            try:
                image = pg.image.load(path)
                try:
                    image = image.convert_alpha()
                except Exception:
                    image = image.convert()
                image = pg.transform.smoothscale(image, (SQUARE_SIZE, SQUARE_SIZE))
                PIECE_IMAGES[key] = image
            except Exception:
                PIECE_IMAGES[key] = _make_placeholder(color, piece, SQUARE_SIZE)
                print(f"[assets] Warning: missing image '{filename}', using placeholder.")

    _initialized = True

def get_piece_image(color: str, piece: str) -> pg.Surface:
    """Restituisce l'immagine già caricata dei pezzi dal dizionario PIECE_IMAGES."""
    key = f"{color.lower()}_{piece.lower()}"
    if key in PIECE_IMAGES:
        return PIECE_IMAGES[key]
    else:
        # fallback generico
        return _make_placeholder(color, piece, SQUARE_SIZE)

