import datetime
import string
import random


LETTERS = string.ascii_letters
NUMBERS = string.digits


def generate_password(length=8) -> str:
    '''
    Generates a random password having the specified length
    :length -> length of password to be generated. Defaults to 8
        if nothing is specified.
    :returns string <class 'str'>
    '''
    random_password = generate_random_key(length)
    return random_password


def generate_random_key(length=None) -> str:
    if length is None:
        length = random.randint(30, 45)
    
    letters_and_numbers = f'{LETTERS}{NUMBERS}'

    # convert printable from string to list and shuffle
    letters_and_numbers = list(letters_and_numbers)
    random.shuffle(letters_and_numbers)

    # generate random key and convert to string
    random_key = random.choices(letters_and_numbers, k=length)
    random_key = ''.join(random_key)

    return random_key


def create_date_object(day:str, month:str, year:str):
    date_str = f"{year}-{month}-{day}"
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date
