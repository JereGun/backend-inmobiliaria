import random
import string

def random_lower_string(length: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))

def random_string(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))

def random_email() -> str:
    return f"{random_lower_string(10)}@{random_lower_string(5)}.com"
