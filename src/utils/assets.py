import pygame
import os

# Dimensions for resizing images
SQUARE_SIZE = 80  

IMAGES_PATH = os.path.join(os.path.dirname(__file__), "images")

# list of piece types and colors
PIECE_TYPES = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
COLORS = ['white', 'black']

# Dictionary to hold loaded images
PIECE_IMAGES = {}

def load_all_images():
    """Load all piece images into the PIECE_IMAGES dictionary."""
    for color in COLORS:
        for piece in PIECE_TYPES:
            filename = f"{color}_{piece}.png"
            path = os.path.join(IMAGES_PATH, filename)
            try:
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
                PIECE_IMAGES[f"{color}_{piece}"] = image
            except pygame.error as e:
                print(f"Error loading image {filename}: {e}")
                PIECE_IMAGES[f"{color}_{piece}"] = None  # placeholder None if image fails to load

# Initial load of all images
load_all_images()

def get_piece_image(color, piece_type):
    """Return the pygame image for a given color and piece type."""
    return PIECE_IMAGES.get(f"{color}_{piece_type}")
