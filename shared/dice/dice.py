import random

def roll(dice, modifier=0):
    dice_list = dice.split("d")
    if not dice_list[0]:
        number_of_dice = 1
    else:
        number_of_dice = int(dice_list[0])
    result_dice = dice_list[1]
    # result = sum(
    #     random.randint(1, int(result_dice)) 
    #     for _ in range(number_of_dice)
    # ) + modifier
    
    # This is better if you need to perform operations on a per roll basis.
    result = 0
    for _ in range(number_of_dice):
        result += random.randint(1, int(result_dice))
    result += modifier

    return result

final_result = roll("d6", -2)

# Using a below pattern to build encounter tables.
# Exapnding out from just counting the frequency of results, to adding specific encounters within those ranges. 
# This will allow for more specific encounters to be rolled, and for the frequency of those encounters to be adjusted as needed.
# def test_d100_frequency(number_of_rolls):
#     rolls = 0
#     result_frequency = {
#         "1-25": 0,
#         "26-50": 0,
#         "51-75": 0,
#         "76-100": 0
#     }
#     while rolls < number_of_rolls:
#         rolls += 1        
#         result = roll("d100")
#         if result <= 25:
#             result_frequency["1-25"] += 1
#         if result > 25 and result <= 50:
#             result_frequency["26-50"] += 1
#         if result > 50 and result <= 75:
#             result_frequency["51-75"] += 1
#         if result > 75:
#             result_frequency["76-100"] += 1
#     return result_frequency
