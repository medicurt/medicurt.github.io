import random
import string

def random_lower_string(length: int = 40) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))

def random_bool():
    my_bool = random.randint(0,1)
    if my_bool:
        return True
    return False