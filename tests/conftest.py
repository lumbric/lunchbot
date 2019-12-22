from typing import Dict, List
import datetime

import pytest


@pytest.fixture()
def menus() -> Dict[str, List[str]]:
    return {
        "mensa_a": ["spam", "eggs"],
        "mensa_b": ["eggs and spam"],
    }


@pytest.fixture()
def day() ->  datetime.date:
    return datetime.date(2000, 1, 1)
