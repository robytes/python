import json
from map.map_generator import generate_map_data

# Generate map using your auto-discovered subfolders and 45% clustering
grid = generate_map_data(width=7, height=7)

map_data = {
    "width": len(grid[0]),
    "height": len(grid),
    "tiles": grid
}

# Write directly to root (where index.html sits)
with open("map_data.json", "w") as f:
    json.dump(map_data, f, indent=4)

print("Successfully generated updated map_data.json!")