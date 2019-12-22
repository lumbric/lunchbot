from typing import Dict, List

import pytest


@pytest.fixture()
def menus() -> Dict[str, List[str]]:
    return {
        "mensa_a": ["spam", "eggs"],
        "mensa_b": ["eggs and spam"],
    }
