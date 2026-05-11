def calculate_delivery(weight: float, distance: float) -> float:
    """
    function for calculating the delivery
    :param weight:
    :param distance:
    :return delivery price:
    """
    base_delivery = 100
    weight_price = weight * 10
    distance_price = distance * 5
    return base_delivery + weight_price + distance_price
