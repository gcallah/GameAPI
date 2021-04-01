"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""
import os
import json

HEROKU_HOME = '/app'
GAME_HOME = os.getenv("GAME_HOME", HEROKU_HOME)

DATA_DIR = f'{GAME_HOME}/data'
MAIN_MENU_JSON = DATA_DIR + '/' + 'main_menu.json'
GAMES_MENU_JSON = DATA_DIR + '/' + 'games_menu.json'
CREATE_GAME_JSON = DATA_DIR + '/' + 'create_game.json'
CREATE_GAME_MENU_JSON = DATA_DIR + '/' + 'create_game_menu.json'
GAMES_JSON = DATA_DIR + '/' + 'games.json'


def load_from_file(file):
    """
    Right now we store all of our data in ordinary files.
    But let's hide that fact inside this module.
    """
    print(f"Going to open {file}")
    try:
        with open(file) as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return None


def get_games():
    """
    A function to return all games in the database.
    Soon we probably need a flag to get just active games.
    """
    return load_from_file(GAMES_JSON)


def get_games_menu():
    """
    Fetch the games menu.
    """
    return load_from_file(GAMES_MENU_JSON)


def get_create_game_menu():
    """
    Fetch the create game menu.
    """
    return load_from_file(CREATE_GAME_MENU_JSON)


def get_main_menu():
    """
    Fetch the main menu.
    """
    return load_from_file(MAIN_MENU_JSON)


def get_create_game():
    """
    Returns the form for creating a game.
    """
    return load_from_file(CREATE_GAME_JSON)
