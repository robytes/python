import os
import pygame

class MapRenderer:
    def __init__(self, tiles_dir="assets/tiles"):
        self.tile_width = 64
        self.tile_height = 128
        self.diamond_height = 32
        self.tileset = self._load_tiles(tiles_dir)
    
    def _load_tiles(self, tiles_dir):
        tiles = {"swamp": [], "swamp_forest": []}
        for i in range(4):
            swamp_tile_path = os.path.join(tiles_dir, f"swamp_{i}.png")
            swamp_forest_tile_path = os.path.join(tiles_dir, f"swamp_forest_{i}.png")

            if os.path.exists(swamp_tile_path):
                tiles["swamp"].append(pygame.image.load(swamp_tile_path).convert_alpha())
            if os.path.exists(swamp_forest_tile_path):
                tiles["swamp_forest"].append(pygame.image.load(swamp_forest_tile_path).convert_alpha())
        return tiles
    
    def render_map(self, screen, map_grid, origin_x, origin_y):
        half_width = self.tile_width // 2
        for grid_y, row in enumerate(map_grid):
            for grid_x, tile_type in enumerate(row):
                screen_x = origin_x + (grid_x - grid_y) * half_width
                screen_y = origin_y + (grid_x + grid_y) * (self.diamond_height // 2)

                # Calculate the isometric position
                iso_x = origin_x + (grid_x - grid_y) * half_width
                iso_y = origin_y + (grid_x + grid_y) * self.diamond_height

                variant = (grid_x * 3 + grid_y * 7) % len(self.tileset[tile_type])  # Simple variant selection
                tile_surface = self.tileset[tile_type][variant]

                draw_x = screen_x - half_width
                draw_y = screen_y - (self.tile_height - self.diamond_height)
                screen.blit(tile_surface, (draw_x, draw_y))