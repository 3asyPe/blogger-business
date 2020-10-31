from BloggerBusiness.utils import upload_image_path


def upload_image_path_offer(*args, **kwargs):
    return upload_image_path(*args, **kwargs, prefix="offer")