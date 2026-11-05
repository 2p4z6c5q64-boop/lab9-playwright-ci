import pytest
from playwright.sync_api import expect


def calculate(page, amount, zone="city"):
    page.fill("#amount", amount)
    page.select_option("#zone", zone)
    page.click("#calculate")


# 1-6: стоимость доставки в обычных и граничных случаях
@pytest.mark.parametrize(
    "amount, zone, expected",
    [
        ("1", "city", "Стоимость доставки: 300 ₽"),        # 1  минимум, город
        ("5000", "city", "Стоимость доставки: 300 ₽"),     # 2  середина, город
        ("9999", "city", "Стоимость доставки: 300 ₽"),     # 3  граница-1, город
        ("1", "region", "Стоимость доставки: 600 ₽"),      # 4  минимум, область
        ("5000", "region", "Стоимость доставки: 600 ₽"),   # 5  середина, область
        ("9999", "region", "Стоимость доставки: 600 ₽"),   # 6  граница-1, область
    ],
)
def test_paid_delivery(delivery_page, amount, zone, expected):
    calculate(delivery_page, amount, zone)
    expect(delivery_page.locator("#result")).to_have_text(expected)


# 7-8: граничное значение 10000 - доставка бесплатна
@pytest.mark.parametrize("zone", ["city", "region"])
def test_free_delivery_at_threshold(delivery_page, zone):
    calculate(delivery_page, "10000", zone)
    expect(delivery_page.locator("#result")).to_have_text("Доставка бесплатно")


# 9: сумма выше порога
def test_free_delivery_above_threshold(delivery_page):
    calculate(delivery_page, "10001", "region")
    expect(delivery_page.locator("#result")).to_have_text("Доставка бесплатно")


# 10-12: некорректный ввод
@pytest.mark.parametrize("amount", ["", "0", "abc"])
def test_invalid_input(delivery_page, amount):
    calculate(delivery_page, amount)
    expect(delivery_page.locator("#error")).to_have_text(
        "Введите целую сумму больше 0"
    )
    expect(delivery_page.locator("#result")).to_have_text("")
