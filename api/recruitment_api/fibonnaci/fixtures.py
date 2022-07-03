from datetime import datetime
import pytest


@pytest.fixture
def time_tracker():
    tick = datetime.now()
    yield
    tack = datetime.now()
    diff = tack - tick
    print(f"\n runtime: {diff.total_seconds()}")
