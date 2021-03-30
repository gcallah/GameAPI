"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

import os
import json
from flask import Flask
from flask_restx import Resource, Api, fields
from werkzeug.exceptions import NotFound
import textapp.text_app as ta

from API.db import fetch_games

app = Flask(__name__)
api = Api(app)

HELLO = 'hello'
AVAILABLE = 'Available endpoints:'
MAIN_MENU = "Main Menu"
MAIN_MENU_ROUTE = '/menus/main'

HEROKU_HOME = '/app'
GAME_HOME = os.getenv("GAME_HOME", HEROKU_HOME)

DATA_DIR = f'{GAME_HOME}/data'
MAIN_MENU_JSON = DATA_DIR + '/' + 'main_menu.json'
CREATE_GAME_JSON = DATA_DIR + '/' + 'create_game.json'


def load_from_file(file):
    print(f"Going to open {file}")
    try:
        with open(file) as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return None


@api.route('/hello')
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO: 'world'}


@api.route('/endpoints/list')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        epts = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {AVAILABLE: epts}


@api.route(MAIN_MENU_ROUTE)
class MainMenu(Resource):
    """
    This class returns the main menu for the game app.
    """
    @api.response(200, 'Success')
    @api.response(404, 'Not Found')
    def get(self):
        """
        The `get()` method will return the main menu.
        """
        main_menu = load_from_file(MAIN_MENU_JSON)
        if main_menu is None:
            raise (NotFound(f"{MAIN_MENU_JSON} not found."))
        return main_menu


@api.route('/games/list')
class Games(Resource):
    """
    This class supports fetching a list of all games.
    """
    def get(self):
        """
        This method returns all games.
        """
        return {ta.TYPE: ta.DATA,
                ta.TITLE: "Available games",
                ta.DATA: fetch_games()}


user = api.model("user", {
    "name": fields.String("User name.")
})


@api.route('/games/join/<int:game_id>')
class JoinGame(Resource):
    """
    This endpoint allows a user to join an existing game.
    """
    @api.expect(user)
    def put(self, game_id):
        """
        Allow `user` to join `game_id` as a player.
        """
        return "Game joined."


game = api.model("new_game", {
    "name": fields.String("Game name"),
    "max_players": fields.Integer("Maximum players")
})


@api.route('/games/create')
class CreateGame(Resource):
    """
    This class allows the user to create a new game.
    We will be passing in some sort of game object as a
    parameter. Details unknown at present.
    """
    @api.response(200, 'Success')
    @api.response(404, 'Not Found')
    def get(self):
        """
        This method gets the form needed to create a game.
        """
        create_form = load_from_file(CREATE_GAME_JSON)
        if create_form is None:
            raise (NotFound(f"{CREATE_GAME_JSON} not found."))
        return create_form

    @api.expect(game)
    def post(self):
        """
        This method creates a new game.
        """
        return "Game created."
