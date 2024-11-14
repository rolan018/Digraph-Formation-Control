def check_size(item, size):
    if item.shape != size:
        raise ValueError(f"item size must be: {size}")


def check_many_size(item1, item2, size):
    if item1.shape != size or item2.shape != size:
        raise ValueError(f"item1 or item2 size must be: {size}")
