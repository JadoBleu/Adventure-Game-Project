import random
import math
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

''' Generate Weapon'''
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
        if rng(1,3) == True:
            name += " Great Sword"
        elif rng(1,2) == True:
            name += " Hunting Knife"
        else:
            name += " Long Sword"
    #Impact damage type weapon names
    elif damage_type == "impact":
        if rng(1,3) == True:
            name += " Spiked Mace"
        elif rng(1,2) == True:
            name += " War Hammer"
        else:
            name += " Heavy Flail"
    #Magic damage type weapon names
    elif damage_type == "magic":
        if rng(1,3) == True:
            name += " Engraved Wand"
        elif rng(1,2) == True:
            name += " Wizard's Staff"
        else:
            name += " Enchanted Sword"
    #Spirit damage type weapon names
    elif damage_type == "spirit":
        if rng(1,3) == True:
            name += " Divine Scepter"
        elif rng(1,2) == True:
            name += " Scrying Ball"
        else:
            name += " Sacred Chime"
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
    weapon_data = {"level": player_level, "rarity": weapon_rarity,"type": weapon_type, "name": weapon_name, "min": weapon_attack_min, "max": weapon_attack_max, "energy": weapon_energy_regen}
    return weapon_data

# Takes the data returned from new_weapon() and prints it in a readable format
def print_weapon_info(weapon):
    #print for troubleshooting
    print("Weapon:\t\t\t",weapon.get("name"))
    print("  Attack:\t\t  ",weapon.get("min"),"-", weapon.get("max"))
    print("  Energy Regen:\t\t  ",weapon.get("energy"))

''' Generate Armor'''
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
            name += " Scale Hauberk"
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
    for _ in range(stat_amount):
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
def print_armor_info(armor):
    #print for troubleshooting
    print("Armor:\t\t\t",armor.get("name"))
    print("  Type:\t\t\t  ",armor.get("type").capitalize())
    print("  Resistance:\t\t  ",armor.get("resistance"))
    if armor.get("health") != 0:
        print("  Health:\t\t  ",armor.get("health"))
    if armor.get("energy") != 0:
        print("  Energy:\t\t  ",armor.get("energy"))
    if armor.get("dexterity") != 0:
        print("  Dexterity:\t\t  ",armor.get("dexterity"))

''' Generate Rings'''
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
    for _ in range(stat_amount):
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
def print_ring_info(ring):
    #print for troubleshooting
    print("Ring:\t\t\t",ring.get("name"))
    if ring.get("attack") != 0:
        print("  Attack:\t\t  ",ring.get("attack"))
    if ring.get("health") != 0:
        print("  Health:\t\t  ",ring.get("health"))
    if ring.get("energy") != 0:
        print("  Energy:\t\t  ",ring.get("energy"))
    if ring.get("dexterity") != 0:
        print("  Dexterity:\t\t  ",ring.get("dexterity"))

''' Input Level'''
# Input level and checks for type 
def input_level():
    player_level = input("\nInput Player Level: ")
    # Try if type is integer
    try:
        player_level = int(player_level)
        print()
    # Clear screen and loop back to player_data if not integer
    except:
        clear_screen()
        print("\'",player_level,"\'is not a valid input. Please enter a number.")
        input_level()
    return player_level


# Generate a set of equipment for the player
def player_data(player_level):
    weapon1 = new_weapon(player_level)
    armor1 = new_armor(player_level)
    ring1 = new_ring(player_level)
    ring2 = new_ring(player_level) 
    player_data = {"weapon": weapon1, "armor": armor1, "ring1": ring1, "ring2": ring2}
    return player_data

# Generates an enemy name based on the weapon and armor type
def new_enemy_name(enemy_data):
    name = ""
    # Jobs based off armor type
    if enemy_data["armor"]["type"] == "plate":
        if rng(1,2) == True:
            name += "Ogre"
        else:
            name += "Troll"
    elif enemy_data["armor"]["type"] == "leather":
        if rng(1,2) == True:
            name += "Goblin"
        else:
            name += "Bandit"
    elif enemy_data["armor"]["type"] == "chain":
        if rng(1,2) == True:
            name += "Gremlin"
        else:
            name += "Kobold"
    elif enemy_data["armor"]["type"] == "robe":
        if rng(1,2) == True:
            name += "Vampire"
        else:
            name += "Draconian"
    # Jobs based off weapon type
    if enemy_data["weapon"]["type"] == "slash":
        if rng(1,2) == True:
            name += " Scout"
        else:
            name += " Hunter"
    elif enemy_data["weapon"]["type"] == "impact":
        if rng(1,2) == True:
            name += " Brute"
        else:
            name += " Warrior"
    elif enemy_data["weapon"]["type"] == "magic":
        if rng(1,2) == True:
            name += " Sorcerer"
        else:
            name += " Mage"
    elif enemy_data["weapon"]["type"] == "spirit":
        if rng(1,2) == True:
            name += " Witch Doctor"
        else:
            name += " Shaman"
    return name

# Generate a set of equipment for the enemy
def enemy_data(player_level):
    enemy_level = player_level - random.randrange(-3,3)
    if enemy_level <= 1:
        enemy_level = 1
    enemy_weapon = new_weapon(enemy_level)
    enemy_armor = new_armor(enemy_level)
    enemy_ring1 = new_ring(enemy_level)
    enemy_ring2 = new_ring(enemy_level)
    enemy_data = {"level": enemy_level, "weapon": enemy_weapon, "armor": enemy_armor, "ring1": enemy_ring1, "ring2": enemy_ring2}
    enemy_data["name"] = new_enemy_name(enemy_data)
    return enemy_data

# Function to print equipment data regardless of entity
def print_equipment_data(data):
    # Weapon Data
    print_weapon_info(data.get("weapon"))
    # Armor Data
    print_armor_info(data.get("armor"))
    # Ring1 Data
    print_ring_info(data.get("ring1"))
    # Ring2 Data
    print_ring_info(data.get("ring2"))
    
# Initiates the player_data() function
player_level = int(input_level())

# Generate a new player data based on input player level
player_data = player_data(player_level)

# Print player data
print("\nPlayer Equipment:\n")
print_equipment_data(player_data)


# Generate a new enemy data based on input player level
enemy_data = enemy_data(player_level)

# Print enemy data
print("\n\nEnemy Equipment:")
print("Name:\t\t\t",enemy_data["name"])
print("  Level:\t\t  ",enemy_data.get("level"))
print_equipment_data(enemy_data)