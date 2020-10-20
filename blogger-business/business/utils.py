from BloggerBusiness.utils import upload_image_path


def upload_image_path_business(*args, **kwargs):
    return upload_image_path(*args, **kwargs, prefix="business")