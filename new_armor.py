import random
import math
# Clear the screen
# Repeated
def clear_screen():
    print("\033c", end="")

# Returns True or False randomly based off a probability
# Repeated
def rng(rate = 50, max = 100):
    result = random.randint(0,max)
    if result < rate:
        return True
    else:
        return False  

# Returns a rarity value based off the chances. Default to 80:15:5
# Repeated
def new_rarity(common = 80, uncommon = 15, rare = 5):
    # 0 = common
    # 1 = uncommon
    # 2 = rare
    
    if rng(common) == True:
        rarity = "common"
    elif rng(uncommon,(uncommon + rare)) == True:
        rarity = "uncommon"
    else:
        rarity = "rare"
    return rarity

# Selects a random damage type out of the 4 available:"plate", "leather", "chain", "robe"
def new_armor_type():
    if rng(1,4) == True:
        armor_type = "plate"
    elif rng(1,3) == True:
        armor_type = "leather"
    elif rng(1,2) == True:
        armor_type = "chain"
    else:
        armor_type = "robe"
    return armor_type

# Generates a armor name based on the damage type
def new_armor_name(armor_rarity, armor_type):
    name = armor_rarity.capitalize()
    #Plate damage type armor names
    if armor_type == "plate":
        if rng(1,3) == True:
            name += " Copper Plate"
        elif rng(1,2) == True:
            name += " Dragon Breastplate"
        else:
            name += " Gladiator Plate"
    #Leather damage type armor names
    elif armor_type == "leather":
        if rng(1,3) == True:
            name += " Brigadine"
        elif rng(1,2) == True:
            name += " Jerkin"
        else:
            name += " Thief's Garb"
    #Chain damage type armor names
    elif armor_type == "chain":
        if rng(1,3) == True:
            name += " Crusader Chainmail"
        elif rng(1,2) == True:
            name += " Battle Lamellar"
        else:
            name += " Scale hauberk"
    #Robe damage type armor names
    elif armor_type == "robe":
        if rng(1,3) == True:
            name += " Blessed Robe"
        elif rng(1,2) == True:
            name += " Regalia"
        else:
            name += " Holy Silks"
    return name

# Generates a new armor based on the player's level
def new_armor(player_level, common = 80, uncommon = 15, rare = 5):
    armor_rarity = new_rarity(common, uncommon, rare)
    armor_type = new_armor_type()
    armor_name = new_armor_name(armor_rarity, armor_type)
    #Generate Resistance values within a range.
    armor_resistance = (int(math.sqrt(player_level)*20) + 5)
    #Generate the amount of additional stats
    if armor_rarity == "common":
        stat_amount = 1
    elif armor_rarity == "uncommon":
        stat_amount = random.randint(2,3)
    elif armor_rarity == "rare":
        stat_amount = 4
    #Generate the stats 
    bonus_health = 0
    bonus_energy = 0
    bonus_dexterity = 0
    for x in range(stat_amount):
        if rng(1,3) == True:
            bonus_health = bonus_health + (int(math.sqrt(player_level)*5) + 10)
        elif rng(1,2) == True:
            bonus_energy = bonus_energy + (int(math.sqrt(player_level)*1.5) + 1)
        else:
            bonus_dexterity = bonus_dexterity + (int(math.sqrt(player_level)) + 5)
    

    #Packs the data into a dictionary to return
    armor_data = {"level": player_level, "rarity": armor_rarity,"type": armor_type, "name": armor_name, "resistance": armor_resistance, "health": bonus_health, "energy": bonus_energy, "dexterity": bonus_dexterity,}
    return armor_data

# Takes the data returned from new_armor() and prints it in a readable format
def print_armor_info(armor1):
    #print for troubleshooting
    print("Armor:\t\t\t",armor1.get("name"))
    print("Type:\t\t\t",armor1.get("type").capitalize())
    print("Resistance:\t\t",armor1.get("resistance"))
    if armor1.get("health") != 0:
        print("Health:\t\t\t",armor1.get("health"))
    if armor1.get("energy") != 0:
        print("Energy:\t\t\t",armor1.get("energy"))
    if armor1.get("dexterity") != 0:
        print("Dexterity:\t\t",armor1.get("dexterity"))

# Input level and checks for type 
def input_level():
    player_level = input("\nInput Player Level: ")
    # Try if type is integer
    try:
        player_level = int(player_level)
        print()
    # Clear screen and loop back to main if not integer
    except:
        clear_screen()
        print("\'",player_level,"\'is not a valid input. Please enter a number.")
        main()
    return player_level

#Main program loop
def main():
    running = ""
    player_level = int(input_level())
    armor1 = new_armor(player_level)
    print_armor_info(armor1)
    running = input("\nEnter anything to try again or 'X' to stop.\n")
    print("\033c", end="")
    print("You have terminated the program.")
    if running.lower() != "x":
        clear_screen()
        main()
    else:
        print("\033c", end="")
        print("You have terminated the program.")
        exit()

#Initiates the main() function
main()
