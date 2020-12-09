'''Generates new weapons, armor, ring, and relevant functions '''
# Imports
import random
import math
from housekeeping import rng


def new_rarity(common=80, uncommon=15, rare=5):
    '''Returns a rarity value based off the chances. Default to 80:15:5'''
    if rng(common):
        rarity = "common"
    elif rng(uncommon, (uncommon + rare)):
        rarity = "uncommon"
    else:
        rarity = "rare"
    return rarity


def new_method_type():
    '''Selects a random damage type out of the 2 available:"single", "splash"'''
    damage_type = "single", "splash"
    return damage_type[random.randrange(0, len(damage_type))]


def new_ability():
    '''Generates a new ability based on the type and method
    returns dict ability'''
    ability = {}
    # generate new method and damage type
    ability["method"] = new_method_type()
    ability["type"] = new_damage_type()
    # generate a new name for the ability
    if ability["method"] == "single":
        ability["energy"] = 10
        if ability["type"] == "slash":
            name = "Rising Fury"
        elif ability["type"] == "impact":
            name = "Heavy Blow"
        elif ability["type"] == "magic":
            name = "Fire Ball"
        elif ability["type"] == "spirit":
            name = "Nether Smite"
    elif ability["method"] == "splash":
        ability["energy"] = 15
        if ability["type"] == "slash":
            name = "Whirling Slash"
        elif ability["type"] == "impact":
            name = "Meteor Strike"
        elif ability["type"] == "magic":
            name = "Chain Lightning"
        elif ability["type"] == "spirit":
            name = "Arcane Blast"
    ability["name"] = name
    ability["level"] = 1
    ability["experience"] = 0
    return ability


def print_ability_info(ability):
    print("\tAbility:\t"+ability["name"])
    print("\t Level:\t\t", ability["level"])
    print("\t Energy Cost:\t", ability["energy"])
    if ability["method"] == "single":
        print("\t Description:\t This ability deals a large amount of\n\t\t\t",
            ability["type"],"damage to a single target\n")
    elif ability["method"] == "splash":
        print("\t Description:\t This ability deals an increased amount of\n\t\t\t",
            ability["type"],"damage to a single enemy, \n\t\t\t"
            " and reduced damage to all other enemies\n")


# Generate Weapon
def new_damage_type():
    '''Selects a random damage type out of the 4 available:"slash", "impact", "magic", "spirit"'''
    damage_type = "slash", "impact", "magic", "spirit"
    return damage_type[random.randrange(0, len(damage_type))]


def new_weapon_name(weapon_rarity, damage_type):
    '''Generates a weapon name based on the damage type'''
    name = weapon_rarity.capitalize()+" "
    # Damage type weapon names
    slash_names = "Great Sword", "Hunting Knife", "Long Sword"
    impact_names = "Spiked Mace", "War Hammer", "Heavy Flail"
    magic_names = "Engraved Wand", "Wizard Staff", "Enchanted Sword"
    spirit_names = "Divine Scepter", "Scrying Ball", "Sacred Chime"
    if damage_type == "slash":
        name += slash_names[random.randrange(0, len(slash_names))]
    elif damage_type == "impact":
        name += impact_names[random.randrange(0, len(impact_names))]
    elif damage_type == "magic":
        name += magic_names[random.randrange(0, len(magic_names))]
    elif damage_type == "spirit":
        name += spirit_names[random.randrange(0, len(spirit_names))]
    return name


def new_weapon(common=80, uncommon=15, rare=5, level=1):
    '''Generates a new weapon based on the player's level'''
    weapon_rarity = new_rarity(common, uncommon, rare)
    weapon_type = new_damage_type()
    weapon_name = new_weapon_name(weapon_rarity, weapon_type)
    # Generate Attack values with a minimum range of 2
    try:
        weapon_attack_min = int((10 + math.pow(level, 0.91) * 2)
                                + (level * (random.randrange(-100, 100, 1)/1000)))
    except:
        weapon_attack_min = int((12) + (random.randrange(-1, 2, 1)))
    weapon_attack_max = int((weapon_attack_min * (random.randrange(100, 110)/100)) + 5)
    weapon_energy_regen = int(weapon_attack_min * (random.randrange(50, 60)/100))
    # Calculate weapon cost
    weapon_value = math.floor(level/10)*3 + 50 + random.randrange(-3, 3)
    # Packs the data into a dictionary to return
    weapon_data = {
        "item": "weapon",
        "level": level,
        "rarity": weapon_rarity,
        "type": weapon_type,
        "name": weapon_name,
        "min": weapon_attack_min,
        "max": weapon_attack_max,
        "energy": weapon_energy_regen,
        "value": weapon_value
        }
    return weapon_data


def print_weapon_info(weapon):
    '''Takes the data returned from new_weapon() and prints it in a readable format'''
    if weapon["name"] == "":
        print("\tWeapon:\t\t", "None Equipped")
    else:
        print("\tWeapon:\t\t", weapon["name"], "("+str(weapon["value"])+"g)")
        print("\t  Attack:\t\t  ", weapon["min"], "-", weapon["max"])
        print("\t  Energy Regen:\t\t  ", weapon["energy"])


# Generate Armor
def new_armor_type():
    '''Selects a random damage type out of the 4 available:"plate", "leather", "chain", "robe"'''
    armor_type = "plate", "leather", "chain", "robe"
    return armor_type[random.randrange(0, len(armor_type))]


def new_armor_name(armor_rarity, armor_type):
    '''Generates a armor name based on the damage type'''
    name = armor_rarity.capitalize()+" "
    plate_names = "Dragonscale Plate", "Dragon Breastplate", "Gladiator Plate"
    leather_names = "Dragonskin Vest", "Leather Jerkin", "Thief's Garb"
    chain_names = "Crusader Chainmail", "Battle Lamellar", "Scale Hauberk"
    robe_names = "Blessed Robe", "Enchanted Regalia", "Holy Silks"
    # Plate damage type armor names
    if armor_type == "plate":
        name += plate_names[random.randrange(0, len(plate_names))]
    # Leather damage type armor names
    elif armor_type == "leather":
        name += leather_names[random.randrange(0, len(leather_names))]
    # Chain damage type armor names
    elif armor_type == "chain":
        name += chain_names[random.randrange(0, len(chain_names))]
    # Robe damage type armor names
    elif armor_type == "robe":
        name += robe_names[random.randrange(0, len(robe_names))]
    return name


def new_armor(common=80, uncommon=15, rare=5, level=1):
    '''Generates a new armor based on the player's level'''
    armor_rarity = new_rarity(common, uncommon, rare)
    armor_type = new_armor_type()
    armor_name = new_armor_name(armor_rarity, armor_type)
    # Generate Resistance values within a range.
    armor_resistance = int((15 + level * 0.5)
                           + (level * (random.randrange(-50, 50, 1)/1000)))
    # Generate the amount of additional stats
    if armor_rarity == "common":
        stat_amount = 1
    elif armor_rarity == "uncommon":
        stat_amount = random.randint(2, 3)
    elif armor_rarity == "rare":
        stat_amount = 4
    # Generate the stats
    bonus_health = 0
    bonus_energy = 0
    bonus_dexterity = 0
    for _ in range(stat_amount):
        if rng(1, 3):
            bonus_health = bonus_health + (int(math.sqrt(level)*5) + 10)
        elif rng(1, 2):
            bonus_energy = bonus_energy + (int(math.sqrt(level)*1.5) + 1)
        else:
            bonus_dexterity = bonus_dexterity + (int(math.sqrt(level)) + 5)
    # Calculate cost of armor
    armor_value = math.floor(level/10)*3 + 50 + random.randrange(-3, 3)
    # Packs the data into a dictionary to return
    armor_data = {
        "item": "armor",
        "level": level,
        "rarity": armor_rarity,
        "type": armor_type,
        "name": armor_name,
        "resistance": armor_resistance,
        "health": bonus_health,
        "energy": bonus_energy,
        "dexterity": bonus_dexterity,
        "value": armor_value
        }
    return armor_data


def print_armor_info(armor):
    '''Takes the data returned from new_armor() and prints it in a readable format'''
    if armor["name"] == "":
        print("\tArmor:\t\t", "None Equipped")
    else:
        print("\tArmor:\t\t", armor["name"], "("+str(armor["value"])+"g)")
        print("\t  Type:\t\t\t  ", armor["type"].capitalize())
        print("\t  Resistance:\t\t  ", armor["resistance"])
        if armor["health"] != 0:
            print("\t  Health:\t\t  ", armor["health"])
        if armor["energy"] != 0:
            print("\t  Energy:\t\t  ", armor["energy"])
        if armor["dexterity"] != 0:
            print("\t  Dexterity:\t\t  ", armor["dexterity"])


# Generate Rings
def new_ring_name(ring_rarity):
    '''Generates a ring name'''
    name = ring_rarity.capitalize()+" "
    ring_names = (
        "Coral",
        "Sapphire",
        "Opal",
        "Amethyst",
        "Topaz",
        "Ruby",
        "Diamond",
        "Gold",
        "Platinum",
        "Silver",
        "Emerald"
        )
    name += ring_names[random.randrange(0, len(ring_names))]+" Ring"
    return name


def new_ring(common=70, uncommon=20, rare=10, level=1):
    '''Generates a new ring based on the player's level'''
    ring_rarity = new_rarity(common, uncommon, rare)
    ring_name = new_ring_name(ring_rarity)
    # Generate Resistance values within a range.
    # Generate the amount of additional stats
    if ring_rarity == "common":
        stat_amount = 2
    elif ring_rarity == "uncommon":
        stat_amount = random.randint(3, 4)
    elif ring_rarity == "rare":
        stat_amount = random.randint(5, 6)
    # Generate the stats
    bonus_attack = 0
    bonus_health = 0
    bonus_energy = 0
    bonus_dexterity = 0
    for _ in range(stat_amount):
        if rng(1, 4):
            bonus_attack = bonus_attack + (int(math.sqrt(level)) + 2)
        elif rng(1, 3):
            bonus_health = bonus_health + (int(math.sqrt(level)*3) + 1)
        elif rng(1, 2):
            bonus_energy = bonus_energy + (int(math.sqrt(level)*1.5) + 1)
        else:
            bonus_dexterity = bonus_dexterity + (int(math.sqrt(level)) + 1)
    # Calculate cost of armor
    ring_value = math.floor(level/10)*3 + 50 + random.randrange(-3, 3)
    # Packs the data into a dictionary to return
    ring_data = {
        "item": "ring",
        "level": level,
        "rarity": ring_rarity,
        "name": ring_name,
        "health": bonus_health,
        "energy": bonus_energy,
        "dexterity": bonus_dexterity,
        "attack": bonus_attack,
        "value": ring_value
        }
    return ring_data


def print_ring_info(ring):
    '''Takes the data returned from new_ring() and prints it in a readable format'''
    if ring["name"] == "":
        print("\tRing:\t\t", "None Equipped")
    else:
        print("\tRing:\t\t", ring["name"], "("+str(ring["value"])+"g)")
        if ring["attack"] != 0:
            print("\t  Attack:\t\t  ", ring["attack"])
        if ring["health"] != 0:
            print("\t  Health:\t\t  ", ring["health"])
        if ring["energy"] != 0:
            print("\t  Energy:\t\t  ", ring["energy"])
        if ring["dexterity"] != 0:
            print("\t  Dexterity:\t\t  ", ring["dexterity"])


def new_enemy_name(enemy_data, boss = False):
    '''Generate enemy name based off armour type and if boss'''
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
    # Jobs based off weapon type and Boss
    if boss == True:
        name += " "+"Boss"
    else:
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