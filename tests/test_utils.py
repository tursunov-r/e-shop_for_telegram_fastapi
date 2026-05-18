import pytest
from src.utils.calculate_delivery import calculate_delivery


@pytest.mark.parametrize(
    "weight,distance,expected", [(10, 40, 400), (1, 5, 135), (20, 10, 350)]
)
def test_calculate_delivery(weight, distance, expected):
    assert calculate_delivery(weight, distance) == expected


@pytest.mark.parametrize(
    "subtotal,total", [(10000, 8500), (7500, 6750), (5000, 4750)]
)
def test_calculate_totals(subtotal, total):
    assert calculate_total_price(subtotal) == total
