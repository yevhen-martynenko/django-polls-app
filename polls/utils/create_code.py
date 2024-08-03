from random import choice
import string


def create_code(length):
    code = ''
    lowercase_characters = list(string.ascii_lowercase)
    uppercase_characters = list(string.ascii_uppercase)
    numbers_characters = list(string.digits)

    characters = lowercase_characters + uppercase_characters + numbers_characters

    for _ in range(length):
        code += choice(characters)

    return code
