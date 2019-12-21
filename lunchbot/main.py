import re
from datetime import datetime

from lunchbot.scrape_mensa import read_day_menu
from lunchbot.slack_api import post_menu


def filter_malicious(text):
    """We don't want the mensa page to be able to allow arbitrary formating in our slack channel.
    emojis are allowed, but except of that only a very limited set of characters."""
    return re.sub(r"[^\w €\-,\(\)\:]", "", text)


def format_menus(menus):
    """Format dictionary of menu items for slack to one string.

    This function was originally intended to add numbered emoji icons before each meal, so one
    could vote for them, but this feature has been removed.

    Parameters
    ----------
    menus : dict
        of the form {name: list of items} where name is the Mensa place
        and item is one meal with price as str

    """
    # In theory this could be very large and produce a harmful message, but let's trust on slack
    # here and not care too much.

    menu = ''
    for name, items in menus.items():
        menu += f"\n*{filter_malicious(name)}*\n"
        menu += "".join(f" - {filter_malicious(item)}\n" for item in items)

    # menu contains a leading and trailing new line, but slack doesn't care

    return menu


def main():
    day_menu = read_day_menu(date=datetime.today())
    post_menu(format_menus(day_menu))


if __name__ == '__main__':
    main()
