'''Imports'''
import json


def save_file(save_data):
    '''save game data to save_file.json'''
    with open("save_file.json", "w") as save_json:
        json.dump(save_data, save_json, ensure_ascii=False, indent=4)
    save_json.close()


def load_file():
    '''load game data from save_file.json'''
    try:
        with open("save_file.json") as save_json:
            save_data = json.load(save_json)
        save_json.close()
    except:
        save_data = init_new_game()
    return save_data


def init_new_game():
    '''Initialize a new game data and overwrite save_file.json'''
    with open("save_default.json") as init_jason:
        save_data = json.load(init_json)
    init_json.close()
    save_data["name"] = input("Enter your name: ")
    
    # Overwrite save file
    save_file(save_data)
    return save_data
