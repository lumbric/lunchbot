import re
import bs4
import requests


MENU_PARAMS = {
    'BOKU Wien Peter-Jordan-Straße': {
        'uri': 'http://menu.mensen.at/index/index/locid/65',
        'categories': ('category366', 'category367')
    },

    'BOKU Wien M-Cafe Mendel': {
        'uri': 'http://menu.mensen.at/index/index/locid/8',
        'categories': ('category226','category331')
    },

    # Maybe also useful as paramters:
    #http://menu.mensen.at/index/index/?locid=8&woy=4&year=2017
}


def read_page(uri):
    """Retrieve HTML for one Mensa location. Return HTML as str."""
    page = requests.get(uri)
    page.raise_for_status()
    return page.text


def parse_menu(page, date, categories):
    menu = bs4.BeautifulSoup(page, 'html.parser')

    # CSS selectors for interesting tags:
    #
    #   #speiseplan .day .date
    #   #speiseplan .day .day-of-week
    #   #speiseplan .day .day-content
    #   #speiseplan .day .day-content .category-content

    date_str = date.strftime('%d.%m.%Y')
    date_tag = menu.find(class_='date', string=date_str)
    if date_tag is None:
        raise RuntimeError(f"No menu found for date={date_str}")
    day_menu = date_tag.parent

    day_menu_food = bs4.Tag(name='div')

    for categorey in categories:
        day_menu_food.append(
            day_menu.find(id=categorey).find(class_='category-content')
        )

    FILTER_BLACKLIST_REGEX = (
        'Empfehlen Sie uns bitte weiter',
        'Wir möchten',
        'Unser Umweltzeichen',
        'Produkte vom heimischen',
        'Wir verwendent erstklassige',
        '\*\*\*',
        '\*',
    )

    for pattern in FILTER_BLACKLIST_REGEX:
        for tag in day_menu_food.find_all(string=re.compile(pattern)):
            tag.parent.decompose()

    # split by prices
    foods_prices = re.split('(€\s?\d+,\d+)', day_menu_food.text)
    foods = foods_prices[::2]
    prices = foods_prices[1::2]

    # replace new lines with spaces
    foods = [" ".join(food.split()) for food in foods]

    day_menu_food_str = "\n".join(
        f"{food} {price}" for food, price in zip(foods, prices))

    return day_menu_food_str


def read_day_menu(date):
    menus = ''
    for name, menu_params in MENU_PARAMS.items():
        page = read_page(menu_params['uri'])
        menu = parse_menu(page=page, date=date,
                          categories=menu_params['categories'])

        menus += f"**{name}**\n{menu}\n\n"
    return menus


if __name__ == '__main__':
    from datetime import datetime
    day_menu = read_day_menu(datetime(2019, 1, 29))
    print(day_menu)

