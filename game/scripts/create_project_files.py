from pathlib import Path
import argparse

files = {
    "main.py": "# Main game entry point\n",
    "gameworld.py": "# GameWorld class\n",
    "terrain.py": "# Terrain definitions\n",
    "tile.py": "# Tile definitions\n",
    "tilemap.py": "# TileMap class\n",
    "dicebag.py": "# Dice rolling utilities\n",
    "character.py": "# Character class\n",
    "npc.py": "# NPC class\n",
    "quest.py": "# Quest class\n",
    "commandhandler.py": "# Terminal commands\n",
}


def create_project(project_name, destination_path):
    project_path = Path(destination_path) / project_name

    project_path.mkdir(parents=True, exist_ok=True)

    for filename, content in files.items():
        file_path = project_path / filename

        if file_path.exists():
            print(f"Skipped existing file: {file_path}")
            continue

        file_path.write_text(content, encoding="utf-8")
        print(f"Created: {file_path}")

    print(f"\nProject created successfully:")
    print(project_path.resolve())


def main():
    parser = argparse.ArgumentParser(
        description="Create an RPG project structure."
    )

    parser.add_argument(
        "--name",
        help="Project name"
    )

    parser.add_argument(
        "--path",
        default=".",
        help="Destination folder"
    )

    args = parser.parse_args()

    project_name = args.name
    destination_path = args.path

    if not project_name:
        project_name = input(
            "Enter project name: "
        ).strip()

    create_project(project_name, destination_path)


if __name__ == "__main__":
    main()