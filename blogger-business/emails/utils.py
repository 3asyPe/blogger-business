from BloggerBusiness.utils import generate_random_key


def create_activation_key(instance, Klass):
    key = generate_random_key()
    qs = Klass.objects.filter(key__iexact=key)
    while qs.exists():
        key = generate_random_key()
        qs = Klass.objects.filter(key=key)
    instance.key = key
    