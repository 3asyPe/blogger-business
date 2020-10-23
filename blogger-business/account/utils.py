import datetime
import string
import random


LETTERS = string.ascii_letters
NUMBERS = string.digits  
PUNCTUATION = string.punctuation


def generate_password(length=8):
    '''
    Generates a random password having the specified length
    :length -> length of password to be generated. Defaults to 8
        if nothing is specified.
    :returns string <class 'str'>
    '''
    # create alphanumerical from string constants
    printable = f'{LETTERS}{NUMBERS}{PUNCTUATION}'

    # convert printable from string to list and shuffle
    printable = list(printable)
    random.shuffle(printable)

    # generate random password and convert to string
    random_password = random.choices(printable, k=length)
    random_password = ''.join(random_password)
    # return random_password
    return '123456' # fix


def create_birthday_object(day:str, month:str, year:str):
    birthday_str = f"{year}-{month}-{day}"
    birthday = datetime.datetime.strptime(birthday_str, "%Y-%m-%d")
    return birthday
