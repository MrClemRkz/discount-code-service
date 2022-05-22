import logging
import random
import string

from django.conf import settings

from codes.models import Code


def generate_codes(no_of_codes: int) -> bool:
    """Generate new buffer codes."""
    created = 0
    while created < no_of_codes:
        code = "".join(
            random.choices(  # nosec bandit:B311
                string.ascii_letters + string.digits, k=int(settings.CODE_SIZE)
            )
        )
        try:
            Code.objects.create(code_value=code)
            created += 1
        except Exception as ex:
            logging.error(ex)

    return True
