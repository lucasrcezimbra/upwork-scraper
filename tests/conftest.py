import json
from pathlib import Path

import pytest


@pytest.fixture
def contact_info_fake():
    # TODO: create DriverMock that always return initial_state_fake or registered
    filepath = Path.cwd() / 'tests' / 'mocks' / 'contact_info.json'
    with open(filepath) as f:
        return json.load(f)
