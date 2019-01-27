from datetime import datetime
from scrape_mensa import read_day_menu
from slack_api import post_menu


DIGITS = ('zero', 'one', 'two', 'three', 'four',
          'five', 'six', 'seven', 'eight', 'nine')


def format_menus(menus):
    """Prefix every menu item with a numbered emoji reaction.

    Parameters
    ----------
    menus : dict
        of the form {name: list of items} where name is the Mensa place
        and item is one meal with price as str

    """
    menu = ''
    idx = 0
    for name, items in menus.items():
        menu += f"\n*{name}*\n"
        menu += "".join(f":{poll_opt}: {item}\n"
                        for poll_opt, item in zip(DIGITS[idx:], items))
        idx += len(items)

    # menu contains a leading and trailing new line, but slack doesn't care

    return menu, DIGITS[:idx]


def main():
    day_menu = read_day_menu(date=datetime.today())
    post_menu(*format_menus(day_menu))


if __name__ == '__main__':
    main()
