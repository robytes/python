from items.inventory import (
    calculate_total_encumbrance,
    get_encumbrance_status
)

# Test movement rates
assert get_encumbrance_status(0)["movement_rate"] == 120
assert get_encumbrance_status(400)["movement_rate"] == 120
assert get_encumbrance_status(401)["movement_rate"] == 90
assert get_encumbrance_status(800)["movement_rate"] == 90
assert get_encumbrance_status(801)["movement_rate"] == 60
assert get_encumbrance_status(2401)["movement_rate"] == 0

# Test categories
assert get_encumbrance_status(650)["category"] == "light"
assert get_encumbrance_status(1500)["category"] == "heavy"

print("All inventory tests passed!")