import pytest
import requests

from lunchbot.scrape_mensa import parse_menu
from lunchbot.scrape_mensa import read_page
from lunchbot.scrape_mensa import MENU_PARAMS


def test_read_menu_page():
    # needs internet, needs menu to be online... hm...
    assert read_page(list(MENU_PARAMS.values())[0]['uri'])


def test_failing_read_menu_page():
    with pytest.raises(requests.exceptions.HTTPError, match="500 Server Error"):
        assert read_page('http://menu.mensen.at/WRONG_URI')


def test_parse_menu():
    pass
    #assert parse_menu()
