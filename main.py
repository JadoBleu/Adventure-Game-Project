#!/usr/bin/env python3
# Project 02 - Student Directed Project
'''
Name: Jefferson Wang
Crn: 75630
Semester Year: Fall 2020
'''

# Imports
from saveload import save_file, load_file, init_new_game
from housekeeping import clear_screen
from shop import shop
from adventure import adventure


def main_menu(SAVE_DATA):
    '''main menu to save, load, or exit game'''
    clear_screen()
    command = input("N = New Game\nL = Load Game\nX = Exit Game\n")
    if command.lower() == "n":
        clear_screen()
        confirm = input("Overwrite current save file?\nY = Yes\tN = No\n")
        if confirm.lower() == "y":
            clear_screen()
            SAVE_DATA = init_new_game()
            clear_screen()
            print("Created "+SAVE_DATA["name"]+"'s save file")
            town(SAVE_DATA)
        elif confirm.lower() == "n":
            main_menu(SAVE_DATA)
    elif command.lower() == "l":
        SAVE_DATA = load_file()
        clear_screen()
        print("Loaded "+SAVE_DATA["name"]+"'s save file")
        town(SAVE_DATA)
    elif command.lower() == "x":
        exit()
    else:
        main_menu(SAVE_DATA)


# Town options
def town(SAVE_DATA):
    '''Main town menu to visit shop, rest, adventure, or return to main menu'''
    print("You have arrived at the town.")
    command = input("S = Shop\nR = Rest(Save Game)\nA = Adventure\nM = Main Menu\n")
    if command.lower() == "s":
        clear_screen()
        SAVE_DATA = shop(SAVE_DATA)
        town(SAVE_DATA)
    elif command.lower() == "r":
        clear_screen()
        SAVE_DATA = rest(SAVE_DATA)
        town(SAVE_DATA)
    elif command.lower() == "a":
        clear_screen()
        SAVE_DATA = adventure(SAVE_DATA)
        town(SAVE_DATA)
    elif command.lower() == "m":
        clear_screen()
        main_menu(SAVE_DATA)
    else:
        clear_screen()
        town(SAVE_DATA)


def rest(SAVE_DATA):
    '''Restore user hp, energy, and saves game data'''
    command = input("Take a rest? This will overwrite the current save file. (Y = confirm)\n")
    if command.lower() == "y":
        SAVE_DATA["player_data"]["hp"] = SAVE_DATA["player_data"]["max_hp"]
        SAVE_DATA["player_data"]["energy"] = SAVE_DATA["player_data"]["max_energy"]
        save_file(SAVE_DATA)
    clear_screen()
    return SAVE_DATA


# Main Program initiator
SAVE_DATA = {}
main_menu(SAVE_DATA)
