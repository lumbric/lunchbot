import re
import bs4
import logging
import requests
import datetime


URI = 'https://mensen.at/'
MENU_PARAMS = {
    'BOKU Wien Peter-Jordan-Straße': {
        'location_id': '6',
    },

    'BOKU Wien M-Cafe Mendel': {
        'location_id': '8',
    },
}


VEGY_TYPES = {
    'vegan': ':sweet_potato:',
    'vegetarisch': ':cucumber:',
}


LOGGER = logging.getLogger(__name__)


def read_page(uri, cookies=None):
    """Retrieve HTML for one Mensa location. Return HTML as str."""
    page = requests.get(uri, cookies=cookies)
    page.raise_for_status()
    return page.text


def parse_menu(page: str, date: datetime.date):
    """Parses ``page`` (html as string), tries to find the correct link for date, get the index
    and then parse the menu with this index.

    Found in custom.js on mensa.at:

    With the CSS selector '.weekdays .nav-item' one can find data.index:

    <li class="nav-item active" data-index="5">
        <a class="nav-link" href="">
            <span class="day-of-week">Fr</span>
            <span class="date">20.12.</span>
        </a>
    </li>

    Then find menu the menu via CSS selector:

    .menu-plan .menu-item-{index}

    Relevant JS part:

    $(document).on('click', '.weekdays .nav-item', function (e) {
        e.preventDefault();
        $(".menu-plan .menu-item").addClass("hide");
        $(".menu-plan .menu-item-" + $(this).data("index")).removeClass("hide");

    """
    menu = bs4.BeautifulSoup(page, 'html.parser')

    date_str = date.strftime('%d.%m.')
    date_idcs = {date_link.attrs['data-index']
                 for date_link in menu.select('.weekdays .nav-item')
                 if date_link.select('.date')[0].text == date_str}
    if len(date_idcs) != 1:
        raise RuntimeError(f"No unique menu found for date={date_str} (found entries with "
                           f"indices {date_idcs})")

    date_idx, = date_idcs

    menu_of_day = menu.select(f'.menu-plan .menu-item-{date_idx}')

    # first filter complete sections wrapped in <div class="menu-item ...>
    FILTER_SECTION_BLACKLIST_REGEX = (
        'Frühstück',
    )
    def is_blacklisted(meal):
        return any(meal.find_all(string=re.compile(pattern))
                   for pattern in FILTER_SECTION_BLACKLIST_REGEX)
    menu_of_day = [meal for meal in menu_of_day if not is_blacklisted(meal)]

    # now filter <p> tags, small unnecessary comments
    FILTER_BLACKLIST_REGEX = (
        #'Empfehlen Sie uns bitte weiter',
        #'Wir möchten',
        #'Unser Umweltzeichen',
        #'Produkte vom heimischen',
        #'Wir verwendent erstklassige',
        #'Unser Wochenangebot',
        #'in bisserl mehr sein',
        'Tagesteller',
        'Unser Wochenangebot',
        'Aus unserer My Mensa-Soup',
        'darauf hinweisen, dass wir vorwiegend Produkte vom',
        'Unser Umweltzeichen - welches wir in all',
        'Empfehlen Sie uns bitte weiter...',
        'M-Café',
        'Tages-Empfehlung',
        'Aus unserer My-Mensa Soup-Bar',
        'Angebot der Woche',
        'Herzlich Willkommen',
        'im M-Café Biotech!',
        'M-Cafe',
        'Herzlich Willkommen',
        'im M-Café Mendel',
        'Gerne verwöhnen wir euch mit verschiedenen,',
        'gefüllten Weckerln und Sandwiches,',
        'hausgemachtem Blechkuchen und',
        'täglich frisch gebackenem Gebäck!',
        'Darf´s ein bisserl mehr se',
        'im M-Café Mendel',
        'Täglich frischer',
        '\*\*\*',
        '\*',
    )

    for pattern in FILTER_BLACKLIST_REGEX:
        for meal in menu_of_day:
            for tag in meal.find_all(string=re.compile(pattern)):
                tag.parent.decompose()

    menu_of_day_items = []

    for vegy_type, v_symbol_name in VEGY_TYPES.items():
        for meal in menu_of_day:
            for v_image in meal.find_all('img', alt=vegy_type):
                v_symbol = menu.new_tag('p')
                v_symbol.string = v_symbol_name
                v_image.replace_with(v_symbol)

    # note: meal might contain multiple items/prices
    for meal in menu_of_day:
        # split by prices
        foods_prices = re.split('(€\s?\d+,\d+)', meal.text)
        foods = foods_prices[::2]
        prices = foods_prices[1::2]

        # replace new lines with spaces
        foods = [" ".join(food.split()) for food in foods]

        menu_of_day_items += [f"{food} {price}"
                              for food, price in zip(foods, prices)]

    return menu_of_day_items


def read_day_menu(date: datetime.date):
    menus = {}
    for name, menu_params in MENU_PARAMS.items():
        page = read_page(URI, cookies={'mensenExtLocation': menu_params['location_id']})

        try:
            menu = parse_menu(page=page, date=date)
        except Exception as e:
            LOGGER.error(f"Failed to parse menu for {name}: {e}")
        else:
            menus[name] = menu

    if not menus:
        raise RuntimeError("Could not parse any menu.")

    return menus


if __name__ == '__main__':
    day_menu = read_day_menu(datetime.date(2019, 12, 18))

    for location, menu in day_menu.items():
        print(f"{location}: ")
        for meal in menu:
            print("    ", meal)

