'''Random: Battle, Abandoned camp encounter'''
# Imports
import math
import random
import json
from housekeeping import clear_screen, rng
from equipment import new_armor, new_weapon, new_ring, new_enemy_name, \
                      print_armor_info, print_weapon_info, print_ring_info, \
                      new_damage_type, new_method_type, new_ability, print_ability_info
from shop import update_stats


def integer_input(min = 1, max = 999999):
    '''input until selection is integer and in range start and stop inclusive'''
    selection = input()
    selection_ok = False
    while not selection_ok:
        try:
            selection = int(selection)
        except:
            selection = input()
            continue
        if selection >= min and selection <= max:
            selection_ok = True
        else: 
            selection = input()
    return selection


def adventure(SAVE_DATA):
    '''chooses an encounter based on rng'''
    if rng(90):
        SAVE_DATA = battle(SAVE_DATA)
    else:
        SAVE_DATA = encounter(SAVE_DATA)
    SAVE_DATA["shop_data"]["new_items"] = True
    return SAVE_DATA


def encounter(SAVE_DATA):
    ''' Randomly find gold, potions, and scrolls in this encounter'''
    clear_screen()
    name = ("bandit", "adventurer", "mercenary")
    name_plural = ("bandits", "adventurers", "mercenaries")
    print("You stumbled upon an abandoned "
          + name[random.randrange(0, len(name))]+" Camp")
    print("You look around and found some items the "
          + name_plural[random.randrange(0, len(name_plural))]+" left behind.")
    gold = random.randrange(SAVE_DATA["player_data"]["level"],
                            SAVE_DATA["player_data"]["level"] * 3) + 10
    potions = 0
    scrolls = 0
    for _ in range(3):
        if rng(35):
            potions += 1
    if rng(25):
        scrolls += 1
    print("\n\tYou picked up:")
    print("\t\t"+str(gold)+" gold")
    SAVE_DATA["player_data"]["item_data"]["gold"] += gold
    if potions != 0:
        print("\t\t"+str(potions)+" recovery potions")
        SAVE_DATA["player_data"]["item_data"]["potions"] += potions
    if scrolls != 0:
        print("\t\t"+str(scrolls)+" resurection scrolls")
        SAVE_DATA["player_data"]["item_data"]["scrolls"] += scrolls
    SAVE_DATA = gain_exp(3, SAVE_DATA)
    clear_screen()
    return SAVE_DATA


def gain_exp(exp, SAVE_DATA):
    '''checks to see if a level up has been attained.'''
    SAVE_DATA["player_data"]["exp"] += exp
    max_exp = get_max_exp(SAVE_DATA["player_data"]["level"])
    print("\n\tYou gained:\n\t\t"+str(exp)+" experience")
    if SAVE_DATA["player_data"]["exp"] > max_exp:
        SAVE_DATA["player_data"]["level"] += 1
        SAVE_DATA["player_data"]["exp"] -= max_exp
        input("\n\tYou have leveled up!!"
              "\n\tHp and Energy have been replenished"
              "\n\nPress Enter to continue\n")
        SAVE_DATA = level_up(SAVE_DATA)
    else:
        SAVE_DATA["player_data"]["exp"] += exp
        input("\nPress Enter to continue.\n")
    return SAVE_DATA


def get_max_exp(lvl):
    '''calculate the max hp required for leveling up to the next level'''
    return int(50 + math.pow(lvl, 0.9) * 6)


def level_up(SAVE_DATA):
    '''recalculate max stats based on leveling up'''
    points = 3
    health = attack = energy = 0
    clear_screen()
    while points > 0:
        temp = 0
        print("You can increase the following stats "+str(points)+" times:")
        print("\nH = Health(+"+str(health)
              + ")\nA = Attack(+"+str(attack)
              + ")\nE = Energy(+"+str(energy) + ")\n")
        command = input()
        if command.lower() == "h":
            try:
                temp = int(input("How many points do you want to add to health? ("
                                 + str(points) + " points available)\n"))
                if temp <= points:
                    health += temp
                    points -= temp
            except Exception:
                clear_screen()
                print("Choose a number up to the amount of points available")
                continue
        elif command.lower() == "a":
            try:
                temp = int(input("How many points do you want to add to attack? ("
                                 + str(points)+" points available)\n"))
                if temp <= points:
                    attack += temp
                    points -= temp
            except Exception:
                clear_screen()
                print("Choose a number up to the amount of points available")
                continue
        elif command.lower() == "e":
            try:
                temp = int(input("How many points do you want to add to energy? ("
                                 + str(points)+" points available)\n"))
                if temp <= points:
                    energy += temp
                    points -= temp
            except Exception:
                clear_screen()
                print("Choose a number up to the amount of points available")
                continue
        else:
            clear_screen()
            continue
        clear_screen()
    clear_screen()
    print("You have chosen to increase the following stats:")
    print("\nH = Health(+"+str(health)
          + ")\nA = Attack(+"+str(attack)
          + ")\nE = Energy(+"+str(energy) + ")\n")
    command = input("Y = Continue\nN = Redistribute points\n")
    if command.lower() == "y":
        SAVE_DATA["player_data"]["stats"]["health"] += health + 1
        SAVE_DATA["player_data"]["stats"]["attack"] += attack + 1
        SAVE_DATA["player_data"]["stats"]["energy"] += energy + 1
    else:
        level_up(SAVE_DATA)
    # Recalculate hp and energy, and refill to max
    SAVE_DATA["player_data"]["max_hp"] = \
        int(new_max_hp(SAVE_DATA["player_data"]["level"])) + \
        SAVE_DATA["player_data"]["stats"]["health"]
    SAVE_DATA["player_data"]["hp"] = SAVE_DATA["player_data"]["max_hp"]
    
    SAVE_DATA["player_data"]["max_energy"] = \
        int(new_max_energy(SAVE_DATA["player_data"]["level"])) + \
        SAVE_DATA["player_data"]["stats"]["energy"]
    SAVE_DATA["player_data"]["energy"] = SAVE_DATA["player_data"]["max_energy"]
    clear_screen()
    return SAVE_DATA


def new_max_hp(level):
    return round(math.pow(level, 0.91) + 50)


def new_max_energy(level):
    return round(math.pow(level, 0.85) + 5)


def battle(SAVE_DATA):
    '''battle menu display and selection'''
    ENEMY_DATA = generate_enemies(SAVE_DATA)
    try:
        enemy_total_hp = ENEMY_DATA["enemy1"]["hp"] \
                         + ENEMY_DATA["enemy2"]["hp"] \
                         + ENEMY_DATA["enemy3"]["hp"]
    except:
        enemy_total_hp = ENEMY_DATA["enemy1"]["hp"]
    clear_screen()
    while SAVE_DATA["player_data"]["hp"] != 0 and enemy_total_hp != 0:
        print_battle_menu(SAVE_DATA, ENEMY_DATA)
        print(""+"―"*80)
        print("\nChoose an action")
        print("\t1 = Attack")
        try:
            print("\t2 = "+SAVE_DATA["player_data"]["ability_data"]["ability1"]["name"])
        except:
            pass
        try:
            print("\t3 = "+SAVE_DATA["player_data"]["ability_data"]["ability2"]["name"])
        except:
            pass
        print("\t4 = Use Recovery Potion (" \
              +str(SAVE_DATA["player_data"]["item_data"]["potions"])+")\n"
              "\t5 = Run Away")
        print("\n"+"―"*80+"\n")
        selection = integer_input(1, 5)
        if selection == 1:
            ENEMY_DATA = player_attack(SAVE_DATA, ENEMY_DATA)
            SAVE_DATA["player_data"]["energy"] += SAVE_DATA["player_data"]["item_data"]["weapon"]["energy"]
            if SAVE_DATA["player_data"]["energy"] > SAVE_DATA["player_data"]["max_energy"]:
                SAVE_DATA["player_data"]["energy"] = SAVE_DATA["player_data"]["max_energy"]
        elif selection == 2:
            if SAVE_DATA["player_data"]["energy"] >= SAVE_DATA["player_data"]["ability_data"]["ability1"]["energy"]:
                ENEMY_DATA = player_ability("1", SAVE_DATA, ENEMY_DATA)
                SAVE_DATA["player_data"]["ability_data"]["ability1"]["experience"] += 1
                SAVE_DATA["player_data"]["energy"] -= SAVE_DATA["player_data"]["ability_data"]["ability1"]["energy"]
            else:
                clear_screen()
                print("Not enough Energy")
                continue
        elif selection == 3:
            if SAVE_DATA["player_data"]["energy"] >= SAVE_DATA["player_data"]["ability_data"]["ability2"]["energy"]:
                ENEMY_DATA = player_ability("2", SAVE_DATA, ENEMY_DATA)
                SAVE_DATA["player_data"]["ability_data"]["ability2"]["experience"] += 1
                SAVE_DATA["player_data"]["energy"] -= SAVE_DATA["player_data"]["ability_data"]["ability2"]["energy"]
            else:
                clear_screen()
                print("Not enough Energy")
                continue
        elif selection == 4:
            if SAVE_DATA["player_data"]["item_data"]["potions"] != 0:
                SAVE_DATA = use_potion(SAVE_DATA)
            else:
                clear_screen()
                print("You have no more potions. Choose another action")
                continue
        elif selection == 5:
            clear_screen()
            print("Y = Return to town")
            print("Type any other key to return to battle")
            choice = input()
            clear_screen()
            if choice.lower() == "y":
                return SAVE_DATA
            else:
                continue
        enemy_attack(SAVE_DATA, ENEMY_DATA)
        # check to see if enemy has been defeated
        enemy_total_hp = ENEMY_DATA["enemy1"]["hp"]
        try:
            enemy_total_hp += ENEMY_DATA["enemy2"]["hp"]
            enemy_total_hp += ENEMY_DATA["enemy3"]["hp"]
        except:
            pass
        if enemy_total_hp == 0:
            SAVE_DATA = victory(SAVE_DATA, ENEMY_DATA)
        # check to see if player has been defeated
        elif SAVE_DATA["player_data"]["hp"] == 0:
            SAVE_DATA = defeat(SAVE_DATA)
    return SAVE_DATA


def generate_enemies(SAVE_DATA, boss = False):
    '''generate a random set of enemies to fight'''
    ENEMY_DATA = {"enemy1":{"boss": "N"}}
    # Generate number of enemies(1:60%, 2:30%, 3:10%)
    enemies = ["enemy1"]
    if rng(10):
        enemies.append("enemy2")
        enemies.append("enemy3")
    elif rng(30):
        enemies.append("enemy2")
    if rng(5):
        boss = True
        ENEMY_DATA["enemy1"]["boss"] = "Y"
    for x in enemies:
        # Generate a set of equipment for each enemy
        ENEMY_DATA[x] = {}
        if boss:
            ENEMY_DATA[x]["level"] =  SAVE_DATA["player_data"]["level"] + random.randint(3, 5)
            ENEMY_DATA[x]["weapon"] = new_weapon(0, 100, 0, ENEMY_DATA[x]["level"])
            ENEMY_DATA[x]["armor"] = new_armor(0, 100, 0, ENEMY_DATA[x]["level"])
            ENEMY_DATA[x]["ring"] = new_ring(0, 100, 0, ENEMY_DATA[x]["level"])
            ENEMY_DATA[x]["max_hp"] = new_max_hp(ENEMY_DATA[x]["level"]) * 1.5
        else:
            ENEMY_DATA[x]["level"] = SAVE_DATA["player_data"]["level"] + random.randint(-2, 2)
            ENEMY_DATA[x]["weapon"] = new_weapon(100, 0, 0, ENEMY_DATA[x]["level"])
            ENEMY_DATA[x]["armor"] = new_armor(100, 0, 0, ENEMY_DATA[x]["level"])
            ENEMY_DATA[x]["ring"] = new_ring(100, 0, 0, ENEMY_DATA[x]["level"])
            ENEMY_DATA[x]["max_hp"] = new_max_hp(ENEMY_DATA[x]["level"])
        ENEMY_DATA[x]["hp"] = ENEMY_DATA[x]["max_hp"]
        ENEMY_DATA[x]["name"] = new_enemy_name(ENEMY_DATA[x], boss)
        ENEMY_DATA[x]["dexterity"] = 80 + ENEMY_DATA[x]["armor"]["dexterity"] + \
                                     ENEMY_DATA[x]["ring"]["dexterity"]                        
        boss = False
    return ENEMY_DATA


def print_battle_menu(SAVE_DATA, ENEMY_DATA):
    '''Display current battle info'''
    print(""+"―"*80)
    # Enemy2
    try:
        if ENEMY_DATA["enemy2"]:
            print("\t\t\t\t\t\t\t\t   o  \n"
                  "\t\t\t\t\t\t\t\t  /|\ \n"
                  "\t\t\t\t\t\t\t\t  / \ \n"
                  "\t\t\t\t\t\t\t"+ENEMY_DATA["enemy2"]["name"], " (lvl "
            +str(ENEMY_DATA["enemy2"]["level"])+")")
            print("\t\t\t\t\t\t\t HP:   "+str(ENEMY_DATA["enemy2"]["hp"])+"/"
                  +str(ENEMY_DATA["enemy2"]["max_hp"])+"\n")
    except:
        pass
    # Enemy1
    print("\t   o  \t\t\t\t\t\t\t   o  \n"
          "\t  /|\ \t\t\t\t\t\t\t  /|\ \n"
          "\t  / \ \t\t\t\t\t\t\t  / \ ")
    print(""+SAVE_DATA["name"]+" (lvl "+str(SAVE_DATA["player_data"]["level"])
          +")\t\t\t\t\t\t"+ENEMY_DATA["enemy1"]["name"], " (lvl "
          +str(ENEMY_DATA["enemy1"]["level"])+")")
    print(" HP:     "+str(SAVE_DATA["player_data"]["hp"])+"/"
          +str(SAVE_DATA["player_data"]["max_hp"])
          +"\t\t\t\t\t\t HP:   "+str(ENEMY_DATA["enemy1"]["hp"])+"/"
          +str(ENEMY_DATA["enemy1"]["max_hp"]))
    print(" Energy: "+str(SAVE_DATA["player_data"]["energy"])+"/"
          +str(SAVE_DATA["player_data"]["max_energy"]))
	# Enemy3
    try:
        if ENEMY_DATA["enemy3"]:
            print("\t\t\t\t\t\t\t\t   o  \n"
                  "\t\t\t\t\t\t\t\t  /|\ \n"
                  "\t\t\t\t\t\t\t\t  / \ \n"
                  "\t\t\t\t\t\t\t"+ENEMY_DATA["enemy3"]["name"], " (lvl "
            +str(ENEMY_DATA["enemy3"]["level"])+")")
            print("\t\t\t\t\t\t\t HP:   "+str(ENEMY_DATA["enemy3"]["hp"])+"/"
                  +str(ENEMY_DATA["enemy3"]["max_hp"]))
    except:
        pass
    return


def player_attack(SAVE_DATA, ENEMY_DATA, ability_level = 0, method = "basic"):
    '''Player chooses target
    * returns ENEMY_DATA'''
    multiplier = 1
    clear_screen()
    print_battle_menu(SAVE_DATA, ENEMY_DATA)
    print(""+"―"*80)
    print("\nChoose a target to attack")
    try:
        if ENEMY_DATA["enemy2"]["hp"] > 0:
            print("\t1: "+ ENEMY_DATA["enemy2"]["name"])
    except:
        pass
    if ENEMY_DATA["enemy1"]["hp"] > 0:
        print("\t2: "+ ENEMY_DATA["enemy1"]["name"])
    try:
        if ENEMY_DATA["enemy3"]["hp"] > 0:
            print("\t3: "+ ENEMY_DATA["enemy3"]["name"])
    except:
        pass
    print("\n"+"―"*80+"\n")
    selection = integer_input(1,3)
    clear_screen()
    enemy = ["enemy2", "enemy1", "enemy3"]
    target = enemy[selection-1]
    if method != "basic":
        if method == "splash":
            try:
                for x in enemy:
                    
                    if x != target:
                        multiplier = 0.75 + (ability_level*0.1)
                    else:
                        multiplier = 1.5 + (ability_level*0.1)
                    damage = round(damage_taken(
                        SAVE_DATA["player_data"]["item_data"]["weapon"],
                        SAVE_DATA["player_data"]["stats"]["attack"],
                        SAVE_DATA["player_data"]["stats"]["dexterity"],
                        ENEMY_DATA[x]["armor"]
                        ) * multiplier)
                    ENEMY_DATA[x]["hp"] -= damage
                    if ENEMY_DATA[x]["hp"] <= 0:
                        ENEMY_DATA[x]["hp"] = 0
                    print(ENEMY_DATA[x]["name"],"has taken", damage, 
                        SAVE_DATA["player_data"]["item_data"]["weapon"]["type"], "damage from", SAVE_DATA["name"])
            except:
                multiplier = 1.5 + (ability_level*0.1)
                damage = round(damage_taken(
                    SAVE_DATA["player_data"]["item_data"]["weapon"],
                    SAVE_DATA["player_data"]["stats"]["attack"],
                    SAVE_DATA["player_data"]["stats"]["dexterity"],
                    ENEMY_DATA["enemy1"]["armor"]
                    ) * multiplier)
                ENEMY_DATA["enemy1"]["hp"] -= damage
                if ENEMY_DATA["enemy1"]["hp"] <= 0:
                    ENEMY_DATA["enemy1"]["hp"] = 0
                print(ENEMY_DATA["enemy1"]["name"],"has taken", damage, 
                    SAVE_DATA["player_data"]["item_data"]["weapon"]["type"], "damage from", SAVE_DATA["name"])
        elif method == "single":
            multiplier = 2 + (ability_level*0.1)
            damage = round(damage_taken(
                SAVE_DATA["player_data"]["item_data"]["weapon"],
                SAVE_DATA["player_data"]["stats"]["attack"],
                SAVE_DATA["player_data"]["stats"]["dexterity"],
                ENEMY_DATA[target]["armor"]
                ) * multiplier)
            ENEMY_DATA[target]["hp"] -= damage
            if ENEMY_DATA[targetr]["hp"] <= 0:
                ENEMY_DATA[target]["hp"] = 0
            print(ENEMY_DATA[target]["name"],"has taken", damage, 
                SAVE_DATA["player_data"]["item_data"]["weapon"]["type"], "damage from", SAVE_DATA["name"])


    else:
        damage = round(damage_taken(
                    SAVE_DATA["player_data"]["item_data"]["weapon"],
                    SAVE_DATA["player_data"]["stats"]["attack"],
                    SAVE_DATA["player_data"]["stats"]["dexterity"],
                    ENEMY_DATA[target]["armor"]
                    ) * multiplier)
        ENEMY_DATA[target]["hp"] -= damage
        if ENEMY_DATA[target]["hp"] <= 0:
            ENEMY_DATA[target]["hp"] = 0
        print(ENEMY_DATA[target]["name"],"has taken", damage, 
            SAVE_DATA["player_data"]["item_data"]["weapon"]["type"], "damage from", SAVE_DATA["name"])
    return ENEMY_DATA


def player_ability(x, SAVE_DATA, ENEMY_DATA):
    '''Player chooses ability and target
    x is which ability to be used
    * returns ENEMY_DATA'''
    ability = "ability"+x 
    ENEMY_DATA = player_attack(
                        SAVE_DATA,
                        ENEMY_DATA,
                        SAVE_DATA["player_data"]["ability_data"][ability]["level"],
                        SAVE_DATA["player_data"]["ability_data"][ability]["method"]
                    )

    
    return ENEMY_DATA


def enemy_attack(SAVE_DATA, ENEMY_DATA):
    '''Enemy attacks player
    * returns SAVE_DATA'''
    for x in ENEMY_DATA:
        damage = damage_taken(
                    ENEMY_DATA[x]["weapon"],
                    ENEMY_DATA[x]["ring"]["attack"],
                    ENEMY_DATA[x]["ring"]["dexterity"],
                    SAVE_DATA["player_data"]["item_data"]["armor"]
                 )
        SAVE_DATA["player_data"]["hp"] -= damage
        print(SAVE_DATA["name"],"has taken", damage, 
          ENEMY_DATA[x]["weapon"]["type"], "damage from", ENEMY_DATA[x]["name"])
    if SAVE_DATA["player_data"]["hp"] < 0:
        SAVE_DATA["player_data"]["hp"] = 0
    return SAVE_DATA


def damage_taken(weapon_data, bonus_attack, bonus_dexterity, armor_data):
    '''calculate the damage taken based on 
       attack_data, bonus_attack, bonus_dexterity and armor_data
    * returns hp_reduction'''
    # armor type = [resistant(+15% resist), weak(-105% resist)]
    resistance = {
        "plate": ["slash","magic"],
        "leather": ["impact", "spirit"],
        "chain": ["magic", "impact"],
        "robe": ["spirit", "slash"]
    }
    attack_type = weapon_data["type"] 
    armor_type = armor_data["type"]
    multiplier = 0
    if attack_type == resistance[armor_type][0]:
        multiplier = .15
    elif attack_type == resistance[armor_type][1]:
        multiplier = -.1
    
    attack_amount = attack_value(weapon_data, bonus_attack, bonus_dexterity)
    damage_resistance = defense_value(armor_data)
    hp_reduction = round(attack_amount * (1-(damage_resistance + multiplier)))
    return hp_reduction


def defense_value(armor_data):
    '''calculate damage resistance 
    with diminishing returns nearing 75% damage resistance
    before type resistance
    * returns damage_reduction'''
    resistance = armor_data["resistance"]
    damage_resistance = round(0.5 * resistance / (resistance + 100) + 0.25, 4)
    return damage_resistance


def if_hit(dexterity):
    '''calculate if the hit succeeded based on dexterity
    0 dexterity provides 80% accuracy
    with diminishing returns nearing 100% hit rate
    * returns boolean'''
    hit_rate =  round(0.2 * dexterity/(dexterity + 100), ) * 100 + 80
    return rng(hit_rate)


def calculate_crit(dexterity):
    '''calculate if the hit is a critical strike
    each 100% critical strike gives 25% additional damage
    returns crit_multiplier'''
    crit = rng(dexterity % 100)
    if crit:
        crit_multiplier = 1 + ((math.floor(dexterity/100)+1) * 0.25)
    else:
        crit_multiplier = 1 + (math.floor(dexterity/100) * 0.25)
    return crit_multiplier


def attack_value(weapon_data, bonus_attack, bonus_dexterity):
    '''calculate damage value of attack, accuracy and critical multipliers.
       (random(min, max)) + bonus_attack)
    * returns damage_amount'''
    if if_hit(bonus_dexterity):
        damage_amount = (random.randint(weapon_data["min"], weapon_data["max"])
                        + bonus_attack) * calculate_crit(bonus_dexterity)
    else:
        damage_amount = 0
    return damage_amount


def use_potion(SAVE_DATA):
    '''Uses a potion to recover 50% hp'''
    SAVE_DATA["player_data"]["item_data"]["potions"] -= 1
    potion_amt = round(SAVE_DATA["player_data"]["max_hp"] / 2)
    recovered = potion_amt
    if potion_amt > SAVE_DATA["player_data"]["max_hp"] \
                    -SAVE_DATA["player_data"]["hp"]:
        recovered = SAVE_DATA["player_data"]["max_hp"] \
                    -SAVE_DATA["player_data"]["hp"]
    SAVE_DATA["player_data"]["hp"] += recovered
    clear_screen()
    print(SAVE_DATA["name"]+" uses a potion to recover "+str(recovered)+" hp")
    return SAVE_DATA


def victory(SAVE_DATA, ENEMY_DATA):
    '''calculates victory rewards
    * returns SAVE_DATA'''
    print("\n\t\tVICTORY!")
    input("\n\tPress Enter to continue")
    clear_screen()
    # gain exp based on enemy levels
    exp_gain = get_max_exp(ENEMY_DATA["enemy1"]["level"])
    try:
        exp_gain = get_max_exp(ENEMY_DATA["enemy2"]["level"])
        exp_gain = get_max_exp(ENEMY_DATA["enemy3"]["level"])
    except:
        pass
    exp_gain = round(exp_gain * 0.05)
    SAVE_DATA = gain_exp(exp_gain, SAVE_DATA)
    input("\n\tPress Enter to continue")
    clear_screen()
    # check if ability leveled up
    abilities = ["ability1","ability2"]
    for x in abilities:
        max_exp = (50 + (SAVE_DATA["player_data"]["ability_data"][x]["level"])*5)
        if SAVE_DATA["player_data"]["ability_data"][x]["experience"] > max_exp:
            SAVE_DATA["player_data"]["ability_data"][x]["experience"] -= max_exp
            # increase energy cost
            SAVE_DATA["player_data"]["ability_data"][x]["energy"] += 3 * SAVE_DATA["player_data"]["ability_data"][x]["level"]
            # increase level of ability
            SAVE_DATA["player_data"]["ability_data"][x]["level"] += 1
            print("Your "+SAVE_DATA["player_data"]["ability_data"][x]["name"]+" has leveled up.")
    input("\n\tPress Enter to continue")
    clear_screen()
    # gain gold based on player level and number of enemies
    gold_earned = random.randrange(exp_gain*50, exp_gain*150)
    SAVE_DATA["player_data"]["item_data"]["gold"] += gold_earned
    print("You have earned "+str(gold_earned)+" gold")
    input("\n\tPress Enter to continue")
    clear_screen()
    # gain item drop based on enemy level
    print("You have found")
    if rng(25):
        item_drop = new_ring(70, 20, 10, SAVE_DATA["player_data"]["level"])
        print_ring_info(item_drop)
        item_drop_type = "ring"
    elif rng(35, 75):
        item_drop = new_weapon(70, 20, 10, SAVE_DATA["player_data"]["level"])
        print_weapon_info(item_drop)
        item_drop_type = "weapon"
    else:
        item_drop = new_armor(70, 20, 10, SAVE_DATA["player_data"]["level"])
        print_armor_info(item_drop)
        item_drop_type = "armor"
    input("\n\tPress Enter to continue")
    clear_screen()
    # Check to see if player will keep the new item
    looping = True
    while looping:
        command = input("Do you wish to replace your current item?(Y/N)")
        if command.lower() == "y":
            if item_drop_type == "ring":
                print("Currently equipped rings:\n1 = ")
                print_ring_info(SAVE_DATA["player_data"]["item_data"]["ring1"])
                print("2 = ")
                print_ring_info(SAVE_DATA["player_data"]["item_data"]["ring2"])
                print("New ring = ")
                print_ring_info(item_drop)
                command = input("Which Ring do you wish to replace? (Enter 'C' to Cancel)\n")
                if command == "1":
                    SAVE_DATA = update_stats(SAVE_DATA, item_drop, "ring1")
                    SAVE_DATA["player_data"]["item_data"]["ring1"] = item_drop
                    looping = False
                elif command == "2":
                    SAVE_DATA = update_stats(SAVE_DATA, item_drop, "ring2")
                    SAVE_DATA["player_data"]["item_data"]["ring2"] = item_drop
                    looping = False
                else:
                    continue
            elif item_drop_type == "weapon":
                print("Currently equipped weapon:")
                print_weapon_info(SAVE_DATA["player_data"]["item_data"]["weapon"])
                print("Replace with this new weapon?")
                print_weapon_info(item_drop)
                command = input("\nY = Confirm\n")
                if command.lower() == "y":
                    SAVE_DATA["player_data"]["item_data"]["weapon"] = item_drop
                    looping = False
            elif item_drop_type == "armor":
                print("Currently equipped armor:")
                print_armor_info(SAVE_DATA["player_data"]["item_data"]["armor"])
                print("Replace with this new armor?")
                print_armor_info(item_drop)
                command = input("\nY = Confirm\n")
                if command.lower() == "y":
                    SAVE_DATA["player_data"]["item_data"]["armor"] = item_drop  
                    SAVE_DATA = update_stats(SAVE_DATA, item_drop, "armor")
                    looping = False
        else: # command not y
            print("You will exchange the dropped item for "+str(item_drop["value"])+" gold")
            command = input("\nY = Confirm\n")
            if command.lower() == "y":
                SAVE_DATA["player_data"]["item_data"]["gold"] += item_drop["value"]
                looping = False
            else:
                continue
    # gain ability tome based on boss drops
    if ENEMY_DATA["enemy1"]["boss"] == "Y":
        SAVE_DATA = ability_tome(SAVE_DATA)
    return SAVE_DATA


def defeat(SAVE_DATA):
    '''check if player wishes to accept defeat or use a resurrection scroll
    * returns SAVE_DATA'''
    clear_screen()
    selection = ""
    while selection.lower != "e" or selection.lower() != "r":
        print("Your hp has fallen to 0\n")
        if SAVE_DATA["player_data"]["item_data"]["scrolls"] > 0:
            print("\tR = Resurrect with 25% hp ("+str(SAVE_DATA["player_data"]["item_data"]["scrolls"]) \
                  +" Ressurection Scrolls available)\n")
        print("\tE = End battle and return to town")
        selection = input()
        if selection.lower() == "r":
            # resurrect
            SAVE_DATA["player_data"]["item_data"]["scrolls"] -= 1
            SAVE_DATA["player_data"]["hp"] = round(SAVE_DATA["player_data"]["max_hp"] * 0.25)
            clear_screen()
            print("You have have been resurrected with "+str(SAVE_DATA["player_data"]["hp"])+" hp")
            return SAVE_DATA
        elif selection.lower() == "e":
            # go to town
            pass
    return SAVE_DATA


def ability_tome(SAVE_DATA):
    '''gives the option to replace the current ability, 
    or consume the tome for ability experience
    * returns SAVE_DATA'''
    ability = new_ability()
    print("You have found an ability tome")
    input("Press Enter to continue\n")
    looping = True
    while looping:
        looping = False
        clear_screen()
        print("Currently known abilities:\n1 = ")
        print_ability_info(SAVE_DATA["player_data"]["ability_data"]["ability1"])
        print("2 = ")
        print_ability_info(SAVE_DATA["player_data"]["ability_data"]["ability2"])
        print("New ability = ")
        print_ability_info(ability)
        print("You can consume this ability tome to:")
        command = input("\tR = replace an existing ability?\n\tL = level up an ability\n")
        if command.lower() == "r":
            # replace an ability
            choice = input("Which ability do you wish to replace?(Press C to Cancel)\n")
            if choice == "1":
                # replace ability1
                SAVE_DATA["player_data"]["ability_data"]["ability1"] = ability
            elif choice == "2":
                # replace ability2
                SAVE_DATA["player_data"]["ability_data"]["ability2"] = ability
            else:
                looping = True
        elif command.lower() == "l":
            # level up an ability
            choice = input("Which ability do you wish to level?(Press C to Cancel)\n")
            if choice == "1":
                # level ability1
                SAVE_DATA["player_data"]["ability_data"]["ability1"]["energy"] += 3 * SAVE_DATA["player_data"]["ability_data"]["ability1"]["level"]
                SAVE_DATA["player_data"]["ability_data"]["ability1"]["level"] += 1
            elif choice == "2":
                # level ability2
                SAVE_DATA["player_data"]["ability_data"]["ability2"]["energy"] += 3 * SAVE_DATA["player_data"]["ability_data"]["ability2"]["level"]
                SAVE_DATA["player_data"]["ability_data"]["ability2"]["level"] += 1
            else:
                looping = True
    return SAVE_DATA


if __name__ == "__main__":
    '''load game data from save_file.json'''
    with open("save_file.json") as save_json:
        SAVE_DATA = json.load(save_json)
    save_json.close()
    battle(SAVE_DATA)
    # ability_tome(SAVE_DATA)