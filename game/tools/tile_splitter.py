import os
import re
from pathlib import Path
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "assets" / "raw"
TILES_BASE_DIR = PROJECT_ROOT / "assets" / "tiles"

# Target tile dimensions in your exported sheets
TILE_WIDTH = 64
TILE_HEIGHT = 128

def parse_terrain_category(filename):
    """
    Extracts everything before '_Set' (case-insensitive).
    E.g. 'SwampForest_Set01_Panel01.png' -> 'SwampForest'
    """
    name = filename.rsplit('.', 1)[0]
    
    # Split at '_Set' or '_set'
    match = re.split(r'_Set', name, flags=re.IGNORECASE)
    if match:
        clean_name = match[0]
        # Clean any accidental leading/trailing underscores
        return clean_name.strip('_')
    
    # Fallback if '_Set' is not present in filename
    return name.split('_')[0]

def resolve_target_subdirectory(category_name):
    """
    Routes categories into specific subdirectories based on keyword match.
    Returns (Subfolder_Path, Relative_Folder_Name)
    """
    cat_lower = category_name.lower()
    
    # Check special rules (Case-insensitive)
    if "road" in cat_lower:
        subfolder = "roads"
    elif "ocean" in cat_lower or "river" in cat_lower:
        subfolder = "water"  # Route oceans and rivers to a dedicated directory
    elif any(keyword in cat_lower for keyword in ["blighted", "burnt", "infected"]):
        subfolder = "special"
    else:
        subfolder = "terrain"  # Standard terrain tiles
        
    target_dir = TILES_BASE_DIR / subfolder
    return target_dir, subfolder

def slice_all_sheets():
    if not RAW_DIR.exists():
        print(f"[Slicer] Error: Directory '{RAW_DIR}' does not exist.")
        return

    processed_sheets = 0
    total_tiles_sliced = 0

    for filename in os.listdir(RAW_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            category = parse_terrain_category(filename)
            target_dir, subfolder = resolve_target_subdirectory(category)
            
            # Ensure the specific output directory exists
            target_dir.mkdir(parents=True, exist_ok=True)
            
            sheet_path = RAW_DIR / filename
            print(f"[Slicer] '{filename}' -> Category: '{category}' -> Saved to: 'assets/tiles/{subfolder}/'")
            
            try:
                sheet = Image.open(sheet_path).convert("RGBA")
            except Exception as e:
                print(f"[Slicer] Failed to open '{filename}': {e}")
                continue

            sheet_width, sheet_height = sheet.size
            cols = sheet_width // TILE_WIDTH
            rows = sheet_height // TILE_HEIGHT

            count = 0
            for row in range(rows):
                for col in range(cols):
                    left = col * TILE_WIDTH
                    upper = row * TILE_HEIGHT
                    right = left + TILE_WIDTH
                    lower = upper + TILE_HEIGHT

                    tile = sheet.crop((left, upper, right, lower))
                    
                    # Save into target subfolder with clean naming
                    out_name = f"{category}_{count}.png"
                    tile.save(target_dir / out_name)
                    count += 1
                    
            processed_sheets += 1
            total_tiles_sliced += count

    print(f"\n[Slicer] Done! Processed {processed_sheets} sheets into {total_tiles_sliced} total tiles.")

if __name__ == "__main__":
    slice_all_sheets()