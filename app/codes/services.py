import logging
import random
import string
from typing import List

from django.conf import settings

from codes.models import BrandCode, Code, CodeCursor


def generate_codes(no_of_codes: int) -> bool:
    """
    Generate new buffer codes.

    Arguments:
        no_of_codes: No of codes requied.

    Returns:
        Returns 'true' when action is completed.

    """
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


def get_last_code_position(brand: str) -> int:
    """
    Get last code position.

    Arguments:
        brand: Brand reference code

    Returns:
        The last code used from the buffer list.

    """
    cursor = CodeCursor.objects.last()
    if cursor:
        return cursor.last_code.id
    else:
        return 0


def add_codes_to_brand(no_of_codes: int, data: dict) -> List[BrandCode]:
    """
    Add codes to brand.

    Arguments:
        no_of_codes: No of codes required
        data: information to create codes for brand

    Returns:
        List of newly created code for the given brand

    """
    last_code_position = get_last_code_position(data["brand"])
    if last_code_position > 0:
        code_list = Code.objects.filter(
            id__gt=last_code_position,
            id__lte=last_code_position + no_of_codes,
        )
    else:
        code_list = Code.objects.filter(id__lte=no_of_codes)

    active_codes = []
    for code in code_list:
        data["code"] = code
        try:
            active_codes.append(BrandCode.objects.create(**data).id)
        except Exception as ex:
            logging.error(ex)

    return BrandCode.objects.filter(id__in=active_codes)
