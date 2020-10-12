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


# Generates a ring name
def new_ring_name(ring_rarity):
    name = ring_rarity.capitalize()
    #Ring names
    if rng(1,8) == True:
        name += " Coral Ring"
    elif rng(1,7) == True:
        name += " Sapphire Ring"
    elif rng(1,6) == True:
        name += " Opal Ring"
    elif rng(1,5) == True:
        name += " Amethyst Ring"
    elif rng(1,4) == True:
        name += " Topaz Ring"
    elif rng(1,3) == True:
        name += " Ruby Ring"
    elif rng(1,2) == True:
        name += " Diamond Ring"
    else:
        name += " Gold Ring"
    return name

# Generates a new ring based on the player's level
def new_ring(player_level, common = 70, uncommon = 20, rare = 10):
    ring_rarity = new_rarity(common, uncommon, rare)
    ring_name = new_ring_name(ring_rarity)
    #Generate Resistance values within a range.
    #Generate the amount of additional stats
    if ring_rarity == "common":
        stat_amount = 2
    elif ring_rarity == "uncommon":
        stat_amount = random.randint(3,4)
    elif ring_rarity == "rare":
        stat_amount = random.randint(5,6)
    #Generate the stats 
    bonus_attack = 0
    bonus_health = 0
    bonus_energy = 0
    bonus_dexterity = 0
    for x in range(stat_amount):
        if rng(1,4) == True:
            bonus_attack = bonus_attack + (int(math.sqrt(player_level)) + 2)
        elif rng(1,3) == True:
            bonus_health = bonus_health + (int(math.sqrt(player_level)*3) + 1)
        elif rng(1,2) == True:
            bonus_energy = bonus_energy + (int(math.sqrt(player_level)*1.5) + 1)
        else:
            bonus_dexterity = bonus_dexterity + (int(math.sqrt(player_level)) + 1)
    
    #Packs the data into a dictionary to return
    ring_data = {"level": player_level, "rarity": ring_rarity, "name": ring_name, "health": bonus_health, "energy": bonus_energy, "dexterity": bonus_dexterity, "attack": bonus_attack}
    return ring_data

# Takes the data returned from new_ring() and prints it in a readable format
def print_ring_info(ring1):
    #print for troubleshooting
    print("ring:\t\t\t",ring1.get("name"))
    print("Resistance:\t\t",ring1.get("resistance"))
    if ring1.get("attack") != 0:
        print("Attack:\t\t\t",ring1.get("attack"))
    if ring1.get("health") != 0:
        print("Health:\t\t\t",ring1.get("health"))
    if ring1.get("energy") != 0:
        print("Energy:\t\t\t",ring1.get("energy"))
    if ring1.get("dexterity") != 0:
        print("Dexterity:\t\t",ring1.get("dexterity"))

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
    ring1 = new_ring(player_level)
    print_ring_info(ring1)
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
