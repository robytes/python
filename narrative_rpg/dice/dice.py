import random

def roll(dice, modifier=0):
    result_dice = dice[1:]
    result = random.randint(1, int(result_dice)) + modifier

    return result

def test_d100_frequency(number_of_rolls):
    rolls = 0
    result_frequency = {
        "1-25": 0,
        "26-50": 0,
        "51-75": 0,
        "76-100": 0
    }
    while rolls < number_of_rolls:
        rolls += 1        
        result = roll("d100")
        if result <= 25:
            result_frequency["1-25"] += 1
        if result > 25 and result <= 50:
            result_frequency["26-50"] += 1
        if result > 50 and result <= 75:
            result_frequency["51-75"] += 1
        if result > 75:
            result_frequency["76-100"] += 1
    return result_frequency
