import os
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Target strictly the terrain subfolder
TERRAIN_TILES_DIR = PROJECT_ROOT / "assets" / "tiles" / "terrain"

def get_biome_registry():
    """
    Scans assets/tiles/terrain/ exclusively and builds a dictionary:
    {
       "SwampForest": ["SwampForest_0", "SwampForest_1"],
       "GrassyHills": ["GrassyHills_0", "GrassyHills_1"],
       ...
    }
    """
    if not TERRAIN_TILES_DIR.exists():
        print(f"[MapGenerator] Warning: Directory '{TERRAIN_TILES_DIR}' does not exist!")
        return {}
    
    registry = {}
    
    # Scan only the files inside assets/tiles/terrain/
    for filename in os.listdir(TERRAIN_TILES_DIR):
        if filename.endswith(".png"):
            clean_name = filename.rsplit(".", 1)[0]
            
            # Extract family name by splitting before the variant index
            if "_" in clean_name:
                family = clean_name.rsplit("_", 1)[0]
            else:
                family = clean_name

            if family not in registry:
                registry[family] = []
                
            registry[family].append(clean_name)
            
    return registry

def generate_map_data(width=5, height=5, cluster_chance=0.45):
    """
    Generates a 2D map grid using ONLY terrain biome families.
    """
    registry = get_biome_registry()
    biome_families = list(registry.keys())
    
    if not biome_families:
        print("[MapGenerator] Error: No terrain tiles found in assets/tiles/terrain/")
        return [["base" for _ in range(width)] for _ in range(height)]
        
    print(f"[MapGenerator] Active Terrain Families: {biome_families}")

    family_grid = []
    variant_grid = []

    for y in range(height):
        family_row = []
        variant_row = []
        
        for x in range(width):
            # Collect connected neighbors (Left & Top)
            neighbor_families = []
            if x > 0:
                neighbor_families.append(family_row[x - 1])
            if y > 0:
                neighbor_families.append(family_grid[y - 1][x])

            # 45% chance to inherit connected neighbor family
            if neighbor_families and random.random() < cluster_chance:
                chosen_family = random.choice(neighbor_families)
            else:
                chosen_family = random.choice(biome_families)

            # Pick a random variant within the terrain family
            available_variants = registry[chosen_family]
            chosen_variant = random.choice(available_variants)

            family_row.append(chosen_family)
            variant_row.append(chosen_variant)

        family_grid.append(family_row)
        variant_grid.append(variant_row)

    return variant_grid