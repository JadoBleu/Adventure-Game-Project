import random
# Clear the screen
def clear_screen():
    print("\033c", end="")

# Returns True or False randomly based off a probability
def rng(rate = 50, max = 100):
    result = random.randint(0,max)
    if result < rate:
        return True
    else:
        return False  

# Returns a rarity value based off the chances. Default to 80:15:5
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

# Selects a random damage type out of the 4 available:"slash", "impact", "magic", "spirit"
def new_damage_type():
    if rng(1,4) == True:
        damage_type = "slash"
    elif rng(1,3) == True:
        damage_type = "impact"
    elif rng(1,2) == True:
        damage_type = "magic"
    else:
        damage_type = "spirit"
    return damage_type

# Generates a weapon name based on the damage type
def new_weapon_name(weapon_rarity, damage_type):
    name = weapon_rarity.capitalize()
    #Slash damage type weapon names
    if damage_type == "slash":
        if rng(1,4) == True:
            name += " War Axe"
        elif rng(1,3) == True:
            name += " Twin Daggers"
        elif rng(1,2) == True:
            name += " Rapier"
        else:
            name += " Long Swprd"
    #Impact damage type weapon names
    elif damage_type == "impact":
        if rng(1,3) == True:
            name += " Mace"
        elif rng(1,2) == True:
            name += " War Hammer"
        else:
            name += " Flail"
    #Magic damage type weapon names
    elif damage_type == "magic":
        if rng(1,3) == True:
            name += " Wand"
        elif rng(1,2) == True:
            name += " Staff"
        else:
            name += " Magic Sword"
    #Spirit damage type weapon names
    elif damage_type == "spirit":
        if rng(1,3) == True:
            name += " Scepter"
        elif rng(1,2) == True:
            name += " Crystal Ball"
        else:
            name += " Holy Sword"
    return name

# Generates a new weapon based on the player's level
def new_weapon(player_level, common = 80, uncommon = 15, rare = 5):
    weapon_rarity = new_rarity(common, uncommon, rare)
    weapon_type = new_damage_type()
    weapon_name = new_weapon_name(weapon_rarity, weapon_type)
    #Generate Attack values with a minimum range of 2
    weapon_attack_min = int(10 + (player_level * 0.6) * (random.randrange(80,120)/100))
    weapon_attack_max = int((weapon_attack_min * (random.randrange(100,120)/100)) + 2)
    weapon_energy_regen = int(weapon_attack_min * (random.randrange(50,60)/100))
    #Packs the data into a dictionary to return
    weapon_data = {"rarity": weapon_rarity,"type": weapon_type, "name": weapon_name, "min": weapon_attack_min, "max": weapon_attack_max, "energy": weapon_energy_regen}
    return weapon_data

# Takes the data returned from new_weapon() and prints it in a readable format
def print_weapon_info(weapon1):
    #print for troubleshooting
    print("Weapon:\t\t\t",weapon1.get("name"))
    print("Attack:\t\t\t",weapon1.get("min"),"-", weapon1.get("max"))
    print("Energy Regen:\t",weapon1.get("energy"))

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
    weapon1 = new_weapon(player_level)
    print_weapon_info(weapon1)
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
