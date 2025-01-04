import uuid

from pydantic import HttpUrl


def generate_recipe_id(url: HttpUrl) -> uuid.UUID:
    """
    Generate a deterministic UUID based on an HTTP URL.

    Args:
        url (HttpUrl): The URL to use as the basis for UUID generation.

    Returns:
        str: A UUID string.
    """
    namespace = uuid.UUID("12345678-1234-5678-1234-567812345678")  # Use a fixed namespace
    return uuid.uuid5(namespace, str(url))
