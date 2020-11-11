'''Allows player interaction with shop to purchase items'''
# Imports
from housekeeping import clear_screen, rng
from equipment import new_weapon, new_armor, new_ring, \
                      print_weapon_info, print_armor_info, print_ring_info


# Shop items
def shop(SAVE_DATA):
    '''Generates new shop items as needed and prints out the menu for user selection'''
    if SAVE_DATA["shop_data"]["new_items"]:
        SAVE_DATA = new_shop_items(SAVE_DATA)
    # Print the item info for shop
    print("Gold:", SAVE_DATA["player_data"]["item_data"]["gold"])
    print("Which item do you wish to purchase?")
    print("0 =\tReturn to Town\n1 =\tHealing Potion(25g)\n2 =\tRessurection Scroll(50g)")
    print_shop(SAVE_DATA)
    command = input()
    if command != 0:
        shop_selection(command, SAVE_DATA)
    return SAVE_DATA


def print_shop(SAVE_DATA):
    '''Displays the shop's items based on type'''
    if SAVE_DATA["shop_data"]["item3"]:
        print("3 =", end="")
        if SAVE_DATA["shop_data"]["item3"]["item"] == "armor":
            print_armor_info(SAVE_DATA["shop_data"]["item3"])
        elif SAVE_DATA["shop_data"]["item3"]["item"] == "weapon":
            print_weapon_info(SAVE_DATA["shop_data"]["item3"])
        elif SAVE_DATA["shop_data"]["item3"]["item"] == "ring":
            print_ring_info(SAVE_DATA["shop_data"]["item3"])
    if SAVE_DATA["shop_data"]["item4"]:
        print("4 =", end="")
        if SAVE_DATA["shop_data"]["item4"]["item"] == "armor":
            print_armor_info(SAVE_DATA["shop_data"]["item4"])
        elif SAVE_DATA["shop_data"]["item4"]["item"] == "weapon":
            print_weapon_info(SAVE_DATA["shop_data"]["item4"])
        elif SAVE_DATA["shop_data"]["item4"]["item"] == "ring":
            print_ring_info(SAVE_DATA["shop_data"]["item4"])
    if SAVE_DATA["shop_data"]["item5"]:
        print("5 =", end="")
        if SAVE_DATA["shop_data"]["item5"]["item"] == "armor":
            print_armor_info(SAVE_DATA["shop_data"]["item5"])
        elif SAVE_DATA["shop_data"]["item5"]["item"] == "weapon":
            print_weapon_info(SAVE_DATA["shop_data"]["item5"])
        elif SAVE_DATA["shop_data"]["item5"]["item"] == "ring":
            print_ring_info(SAVE_DATA["shop_data"]["item5"])


def new_shop_items(SAVE_DATA):
    '''Generate new items set of items to be sold in the shop'''
    lvl = SAVE_DATA["player_data"]["level"]
    if rng(25):
        SAVE_DATA["shop_data"]["item3"] = new_ring(100, 0, 0, lvl)
    elif rng(35, 75):
        SAVE_DATA["shop_data"]["item3"] = new_weapon(100, 0, 0, lvl)
    else:
        SAVE_DATA["shop_data"]["item3"] = new_armor(100, 0, 0, lvl)

    if rng(25):
        SAVE_DATA["shop_data"]["item4"] = new_ring(100, 0, 0, lvl)
    elif rng(35, 75):
        SAVE_DATA["shop_data"]["item4"] = new_weapon(100, 0, 0, lvl)
    else:
        SAVE_DATA["shop_data"]["item4"] = new_armor(100, 0, 0, lvl)

    if rng(25):
        SAVE_DATA["shop_data"]["item5"] = new_ring(100, 0, 0, lvl)
    elif rng(35, 75):
        SAVE_DATA["shop_data"]["item5"] = new_weapon(100, 0, 0, lvl)
    else:
        SAVE_DATA["shop_data"]["item5"] = new_armor(100, 0, 0, lvl)
    # Turns new_items flag off
    SAVE_DATA["shop_data"]["new_items"] = False
    return SAVE_DATA


def shop_selection(command, SAVE_DATA):
    ''' allows the player to select which item they wish
        to buy while checking for sufficient gold.'''
    # Buying items
    if command == "0":
        clear_screen()
        return SAVE_DATA
    if command == "1":
        clear_screen()
        print("Gold:", SAVE_DATA["player_data"]["item_data"]["gold"])
        print("Potions:", SAVE_DATA["player_data"]["item_data"]["potions"])
        command = input("How many Healing Potions(25g) do you wish to buy?\n")
        try:
            command = int(command)
        except TypeError:
            clear_screen()
            print("Enter a number")
            shop(SAVE_DATA)
        cost = (SAVE_DATA["shop_data"]["item1"]["value"]) * command
        if check_gold(cost, SAVE_DATA):
            SAVE_DATA["player_data"]["item_data"]["gold"] -= cost
        else:
            no_gold()
    if command == "2":
        clear_screen()
        print("Gold:", SAVE_DATA["player_data"]["item_data"]["gold"])
        print("Scrolls:", SAVE_DATA["player_data"]["item_data"]["scrolls"])
        command = input("How many Resurrection Scrolls(50g) do you wish to buy?")
        try:
            command = int(command)
        except TypeError:
            clear_screen()
            print("Enter a number")
            shop(SAVE_DATA)
        cost = SAVE_DATA["shop_data"]["item2"]["value"] * command
        if check_gold(cost, SAVE_DATA):
            SAVE_DATA["player_data"]["item_data"]["gold"] -= cost
        else:
            no_gold()
    if command == "3":
        SAVE_DATA = buy_item("item3", SAVE_DATA)
    if command == "4":
        SAVE_DATA = buy_item("item4", SAVE_DATA)
    if command == "5":
        SAVE_DATA = buy_item("item5", SAVE_DATA)
    clear_screen()
    shop(SAVE_DATA)


def buy_item(item_num, SAVE_DATA):
    '''check which item it is, display current equipped counterpart and give option to replace'''
    if check_gold(SAVE_DATA["shop_data"][item_num]["value"], SAVE_DATA):
        clear_screen()
        if SAVE_DATA["shop_data"][item_num]["item"] == "ring":
            print("Currently equipped rings:\n1 = ")
            print_ring_info(SAVE_DATA["player_data"]["item_data"]["ring1"])
            print("2 = ")
            print_ring_info(SAVE_DATA["player_data"]["item_data"]["ring2"])
            print("New ring = ")
            print_ring_info(SAVE_DATA["shop_data"][item_num])
            command = input("Which Ring do you wish to replace? (Press C to Cancel)\n")
            if command == "1":
                SAVE_DATA = update_stats(SAVE_DATA, SAVE_DATA["shop_data"][item_num], "ring1")
                SAVE_DATA["player_data"]["item_data"]["gold"] -= \
                    SAVE_DATA["shop_data"][item_num]["value"]
                SAVE_DATA["player_data"]["item_data"]["ring1"] = \
                    SAVE_DATA["shop_data"][item_num]
                SAVE_DATA["shop_data"][item_num] = None
            elif command == "2":
                SAVE_DATA = update_stats(SAVE_DATA, SAVE_DATA["shop_data"][item_num], "ring2")
                SAVE_DATA["player_data"]["item_data"]["gold"] -= \
                    SAVE_DATA["shop_data"][item_num]["value"]
                SAVE_DATA["player_data"]["item_data"]["ring2"] = \
                    SAVE_DATA["shop_data"][item_num]
                SAVE_DATA["shop_data"][item_num] = None
        else:
            if SAVE_DATA["shop_data"][item_num]["item"] == "armor":
                print("Currently equipped armor:")
                print_armor_info(SAVE_DATA["player_data"]["item_data"]["armor"])
                print("Replace with this new armor?")
                print_armor_info(SAVE_DATA["shop_data"][item_num])
                command = input("\nY = Confirm\n")
                if command.lower() == "y":
                    SAVE_DATA = update_stats(SAVE_DATA, SAVE_DATA["shop_data"][item_num], "armor")
                    SAVE_DATA["player_data"]["item_data"]["gold"] -= \
                        SAVE_DATA["shop_data"][item_num]["value"]
                    SAVE_DATA["player_data"]["item_data"]["armor"] = \
                        SAVE_DATA["shop_data"][item_num]
                    SAVE_DATA["shop_data"][item_num] = None
            elif SAVE_DATA["shop_data"][item_num]["item"] == "weapon":
                print("Currently equipped weapon:")
                print_weapon_info(SAVE_DATA["player_data"]["item_data"]["weapon"])
                print("Replace with this new weapon?")
                print_weapon_info(SAVE_DATA["shop_data"][item_num])
                command = input("\nY = Confirm\n")
                if command.lower() == "y":
                    SAVE_DATA["player_data"]["item_data"]["gold"] -= \
                        SAVE_DATA["shop_data"][item_num]["value"]
                    SAVE_DATA["player_data"]["item_data"]["weapon"] = \
                        SAVE_DATA["shop_data"][item_num]
                    SAVE_DATA["shop_data"][item_num] = None
        clear_screen()
        return SAVE_DATA
    else:
        no_gold()
        return SAVE_DATA


def update_stats(SAVE_DATA, new_item, old_equipment_item):
    '''update player stats with item bonus stats
    removes old item stats
    adds new item stats
    * returns SAVE_DATA'''
    # energy
    SAVE_DATA["player_data"]["stats"]["energy"] -= SAVE_DATA["player_data"]["item_data"][old_equipment_item]["energy"]
    SAVE_DATA["player_data"]["stats"]["energy"] += new_item["energy"]
    # health
    SAVE_DATA["player_data"]["stats"]["health"] -= SAVE_DATA["player_data"]["item_data"][old_equipment_item]["health"]
    SAVE_DATA["player_data"]["stats"]["health"] += new_item["health"]
    
    # dexterity
    SAVE_DATA["player_data"]["stats"]["dexterity"] -= SAVE_DATA["player_data"]["item_data"][old_equipment_item]["dexterity"]
    SAVE_DATA["player_data"]["stats"]["dexterity"] += new_item["dexterity"]
    # attack
    if new_item["item"] == "ring":
        SAVE_DATA["player_data"]["stats"]["attack"] -= SAVE_DATA["player_data"]["item_data"][old_equipment_item]["attack"]
        SAVE_DATA["player_data"]["stats"]["attack"] += new_item["attack"]
    return SAVE_DATA


def check_gold(cost, SAVE_DATA):
    '''Checks the cost of the item against the player's gold balance'''
    if cost > SAVE_DATA["player_data"]["item_data"]["gold"]:
        return False
    else:
        return True


def no_gold():
    '''to do when cost of item wanted is greater that gold balance'''
    clear_screen()
    print("Not enough gold")
    return

