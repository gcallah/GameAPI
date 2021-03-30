"""
This package provides a simple text interface to a GameAPI server.
It relies on the `text_menu` package, which is not yet on PyPi,
"""

import os
import requests

from API.endpoints import MAIN_MENU_ROUTE, MENU_URL
from textapp.text_app import get_single_opt, URL, METHOD
from textapp.text_app import TYPE, DATA, data_repr
from textapp.text_app import FORM, run_form, MENU
from textapp.text_app import SUBMIT, FLDS, DATA_TEXT

SUCCESS = 0

GAME_API_URL = "GAME_API_URL"
LOCAL_HOST = "http://127.0.0.1:8000"


def submit_form(session, server, form):
    if form[SUBMIT][METHOD] == 'post':
        print(f"Submitting {form[FLDS]}")
        session.post(f"{server}{form[SUBMIT][URL]}")


def display_data_page(session, server, data):
    print(f"\n{data_repr(data)[DATA_TEXT]}\n")
    if MENU_URL in data:
        run_menu(session, server, route=data[MENU_URL])


def run_menu(session, server, route=None, menu=None):
    """
    The caller must pass *either* `route` OR `menu`.
    """
    if menu is None:
        menu = session.get(f"{server}{route}")
    # at this point we should check for 404 etc.
    opt = get_single_opt(menu.json())
    if opt[URL]:
        if opt[METHOD] == 'get':
            result = session.get(f"{server}{opt[URL]}")
            ret = result.json()
            if ret[TYPE] == DATA:
                display_data_page(session, server, ret)
            elif ret[TYPE] == FORM:
                submit_form(session, server, run_form(ret))
            elif ret[TYPE] == MENU:
                run_menu(server, menu=ret)
    return SUCCESS


def main():
    server = os.getenv(GAME_API_URL, LOCAL_HOST)
    print(f"API server is {server}")
    session = requests.Session()
    run_menu(session, server, route=MAIN_MENU_ROUTE)


if __name__ == "__main__":
    main()
