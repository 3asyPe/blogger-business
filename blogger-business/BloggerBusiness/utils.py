import random
import os


def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(filename)
    return name, ext


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
    