import string
import random
import os

from datetime import datetime
from googleapiclient.discovery_cache.base import Cache


LETTERS = string.ascii_letters
NUMBERS = string.digits


class MemoryCache(Cache):
    _CACHE = {}

    def get(self, url):
        return MemoryCache._CACHE.get(url)

    def set(self, url, content):
        MemoryCache._CACHE[url] = content


def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(filename)
    return name, ext


def parse_isoformat_time(isof_time: str) -> datetime:
    isof_time = isof_time.replace('Z', '+00:00')
    date = datetime.fromisoformat(isof_time)
    return date


def upload_image_path(instance, filename, prefix):
    print(f"instance-{instance}")
    print(f"filename-{filename}")
    print(f"prefix-{prefix}")
    new_filename = random.randint(1, 11928301)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f"{prefix}/{new_filename}/{final_filename}"


def querydict_to_dict(query_dict):
    data = {}
    for key in query_dict.keys():
        v = query_dict.getlist(key)
        if len(v) == 1:
            v = v[0]
        data[key] = v
    return data
    

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
