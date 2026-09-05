"""
Map Package
Handles procedural grid generation and isometric Pygame rendering.
"""

# 1. Python reads map_generator.py and creates a pointer to generate_map_data
from map.map_generator import generate_map_data

# 2. Python reads map_renderer.py and creates a pointer to MapRenderer
from map.map_renderer import MapRenderer

# Package constants
DEFAULT_GRID_SIZE = (10, 10)
TILE_SIZE = (64, 128)

__all__ = ["generate_map_data", "MapRenderer", "DEFAULT_GRID_SIZE", "TILE_SIZE"]