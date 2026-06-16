import random


def generate_barcode():
    barcode = random.randint(2000000000000, 2999999999999)
    result = str(barcode)
    return result


print(generate_barcode())
