import pytest
import app
from controllers import chocolates

@pytest.fixture
def api(monkeypatch):
    test_chocolates = [
        {'id': 1, 'name': 'test chocolate one', 'country': 'test country one'},
        {'id': 2, 'name': 'test chocolate two', 'country': 'test country two'}
    ]
    monkeypatch.setattr(chocolates, "chocolates", test_chocolates)
    api = app.app.test_client()
    return api