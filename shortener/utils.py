import string

from django.utils.crypto import get_random_string

MAX_LENGTH = 10
ALLOWED_CHARS = string.ascii_letters + string.digits


def create_short_id(model_instance):
    """Create a short_id if it doesn't exist."""
    short_id = get_random_string(length=MAX_LENGTH, allowed_chars=ALLOWED_CHARS)
    model_class = model_instance.__class__
    if model_class.objects.filter(short_id=short_id).exists():
        return create_short_id(model_instance)
    return short_id
