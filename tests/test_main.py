import pytest
from lunchbot.main import format_menus
from lunchbot.main import filter_malicious


def test_filter_malicious():
    good_strings = [
        'BOKU Wien M-Cafe Mendel',
        'Käse-Leberkäse-Semmel € 2,50',
        'Wok Gemüse in Koi Soy Sauce :cucumber: mit Reis (A,L,D,F) € 5,00'
    ]
    for good_string in good_strings:
        assert filter_malicious(good_string) == good_string
    assert filter_malicious('\\evilcommand') == 'evilcommand'
    assert filter_malicious('*evilcommand*') == 'evilcommand'


def test_format_menus(menus):
    assert (
        format_menus(menus)
        ==
        '\n*mensa_a*\n - spam\n - eggs\n\n*mensa_b*\n - eggs and spam\n'
    )