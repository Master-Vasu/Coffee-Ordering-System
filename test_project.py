import pytest
from TheCaffeineDiaries import add_items, remove_items, checkout, Order, Menu

@pytest.fixture
def order():
    return Order()

@pytest.fixture
def menu():
    return Menu()

def test_add_items(order, menu):
    item = menu.fetch_item(1)
    add_items(order, menu, 1, 1)
    assert order.items[0]["option"] == 1
    assert order.items[0]["coffee"] == item["coffee"]
    assert order.items[0]["rate"] == item["rate"]
    assert order.items[0]["quantity"] == 1
    assert order.items[0]["price"] == item["rate"]

def test_remove_items(order, menu):
    item = menu.fetch_item(1)
    order.add_item(1, item["coffee"], item["rate"], 2, item["rate"] * 2)
    remove_items(order, 1, 1)
    assert order.items[0]["quantity"] == 1
    assert order.items[0]["price"] == item["rate"]

def test_checkout(order, capsys):
    message = checkout(order)
    assert message == "No items to checkout"
