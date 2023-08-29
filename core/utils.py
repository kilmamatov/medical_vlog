import random
import string


def random_string(x: int = 10):
    return "".join(random.choices(string.hexdigits, k=x))
