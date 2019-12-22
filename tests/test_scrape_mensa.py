from textwrap import dedent
from typing import  List, Tuple
import datetime

import requests
import pytest

from lunchbot.scrape_mensa import parse_menu, VEGY_TYPES
from lunchbot.scrape_mensa import read_page
from lunchbot.scrape_mensa import URI


def generate_test_html(
    days: List[datetime.date],
    items: List[Tuple[str, str]],
    day_index: int = 0,
):
    """Encapsulate all html generation logic, such that if the website changes, you
    only need to change this function.
    """
    navigation = "\n".join(dedent(f"""
        <ul class="weekdays">
            <li class="nav-item" data-index="{index}">
                <span class="date">{day.strftime("%d.%m.")}</span>
            </li>
        </ul>""")
        for index, day in enumerate(days)
    )

    menu = (
            '<div class="menu-plan">' +
            "\n".join(dedent(f"""
                <span class="menu-item-{day_index}">
                    {food}
                    € {price}
                </span>""")
                for food, price in items
            ) +
            '</div>'
    )

    return navigation + "\n\n" + menu


def test_read_menu_page():
    # needs internet, needs menu to be online... hm...
    assert read_page(URI)


def test_failing_read_menu_page():
    with pytest.raises(requests.exceptions.HTTPError, match="500 Server Error"):
        read_page('http://menu.mensen.at/WRONG_URI')


def test_parse_menu_basic(day):
    items = [
        ("Spam", "10,11"),
        ("Eggs and Spam", "3,40"),
    ]
    page = generate_test_html([day], items)
    assert (
        parse_menu(page, day)
        ==
        [f"{food} € {price}" for food, price in items]
    )


def test_parse_menu_finds_date(day):
    day_index = 7
    days = [day + datetime.timedelta(i) for i in range(10)]
    page = generate_test_html(
        days=days,
        items=[("Spam", "10,11")],
        day_index=day_index,
    )

    menu_items = parse_menu(page, days[day_index])

    assert len(menu_items) == 1


def test_parse_menu_ignores_hints(day):
    page = generate_test_html([day], items=[
        ("Herzlich Willkommen", ""),
        ("Spam", "10,11"),
        ("Tages - Empfehlung", ""),
    ])

    menu_items = parse_menu(page, day)

    assert len(menu_items) == 1


def test_parse_highlights_vegetarian(day):
    vegy_type = next(iter(VEGY_TYPES))

    page = generate_test_html([day], items=[
        (f'Falafel <img src="" alt="{vegy_type}"/>', "1,0"),
        ("Falafel in Leichenteilen", "2,0"),
    ])

    menu_items = parse_menu(page, day)

    assert VEGY_TYPES[vegy_type] in menu_items[0]
    assert VEGY_TYPES[vegy_type] not in menu_items[1]
