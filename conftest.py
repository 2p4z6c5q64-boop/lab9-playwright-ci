import pytest

BASE_URL = "http://127.0.0.1:8000/delivery.html"


@pytest.fixture
def delivery_page(page):
    """Открывает страницу расчета доставки."""
    page.goto(BASE_URL)
    return page
