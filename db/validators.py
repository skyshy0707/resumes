import re

def email_validator(self, field_name: str, value: str):
    assert re.match(r"^\S+@\S+\.\S+$", value), ValueError('Invalid email')
    return value