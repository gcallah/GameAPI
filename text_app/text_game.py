
"""
This package provides a simple text interface to a GameAPI server.
It relies on the `text_menu` package, which is not yet on PyPi,
so for now we use it as a submodule.
"""

import os
import requests

from source.endpoints import MAIN_MENU_ROUTE
from text_menu.text_menu.text_menu import run_menu

GAME_API_URL = "GAME_API_URL"
LOCAL_HOST = "http://127.0.0.1:8000"


def main_menu(session, api_server):
    menu = session.get(f"{api_server}{MAIN_MENU_ROUTE}")
    run_menu(menu_data=menu.json())


def main():
    api_server = os.getenv(GAME_API_URL, LOCAL_HOST)
    print(f"API server is {api_server}")
    session = requests.Session()
    print(session)
    main_menu(session, api_server)


if __name__ == "__main__":
    main()
