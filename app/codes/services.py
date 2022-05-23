import logging
import random
import string
from datetime import date
from typing import List

from django.conf import settings

from codes.models import BrandCode, Code, CodeCursor


def get_code_by_brand(brand: str, assigned_to: str) -> BrandCode:
    """
    Get avaialbe discount code for the given Brand.

    Arguments:
        brand: Brand reference

    Returns:
        BrandCode object.

    """
    code_list = BrandCode.objects.filter(
        brand=brand, is_active=True, is_redeemed=False, assigned_to=None
    )
    code_list = code_list.filter(expiration_date__isnull=True) | code_list.filter(
        expiration_date__lte=date.today()
    )
    if code_list.count() > 0:
        code = code_list.first()
        code.assigned_to = assigned_to
        code.save()

        return code


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


def set_cursor_position(code: int, brand: str) -> bool:
    """
    Set last code position.

    Arguments:
        code_position: last code position
        brand: Brand reference

    Returns:
        Boolean to indicate success of the function execution.

    """
    brand_data = CodeCursor.objects.filter(brand=brand)
    if brand_data.count() > 0:
        cursor = brand_data.last()
        cursor.last_code = code
    else:
        cursor = CodeCursor(brand=brand, last_code=code)

    try:
        cursor.save()
        return True
    except Exception as ex:
        logging.error(ex)
        return False


def add_codes_to_brand(no_of_codes: int, data: dict) -> List[BrandCode]:
    """
    Add codes to brand.

    Arguments:
        no_of_codes: No of codes required
        data: information to create codes for brand

    Returns:
        List of newly created code for the given brand

    """
    # get the last pulled code's position in the buffer code list.
    last_code_position = get_last_code_position(data["brand"])

    # get new set of codes from the buffer list
    if last_code_position > 0:
        code_list = Code.objects.filter(
            id__gt=last_code_position,
            id__lte=last_code_position + no_of_codes,
        )
    else:
        code_list = Code.objects.filter(id__lte=no_of_codes)

    # update the last pulled code's position of the buffer list.
    set_cursor_position(
        code=Code.objects.get(pk=last_code_position + no_of_codes), brand=data["brand"]
    )

    active_codes = []
    for code in code_list:
        data["code"] = code
        try:
            active_codes.append(BrandCode.objects.create(**data).id)
        except Exception as ex:
            logging.error(ex)

    return BrandCode.objects.filter(id__in=active_codes)
