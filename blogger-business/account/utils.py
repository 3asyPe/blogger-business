import datetime

from BloggerBusiness.utils import generate_random_key


def generate_password(length=8) -> str:
    '''
    Generates a random password having the specified length
    :length -> length of password to be generated. Defaults to 8
        if nothing is specified.
    :returns string <class 'str'>
    '''
    random_password = generate_random_key(length)
    return random_password


def create_date_object(day:str, month:str, year:str):
    date_str = f"{year}-{month}-{day}"
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date
