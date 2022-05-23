import json

import pytest
from django.conf import settings

from codes import services
from codes.models import BrandCode, Code


@pytest.mark.django_db
class TestCode:
    """Test code module."""

    ENDPOINT = "/codes/"
    BRAND_REFERENCE = "adidas-newyork"

    def test_generate_codes(self, api_client):
        """Test gernerating codes."""
        assert Code.objects.count() == 0

        response = api_client().get(self.ENDPOINT + "generate/10")

        assert response.status_code == 200
        assert Code.objects.count() == 10

    def test_create_codes_for_brand(self, api_client):
        """Test create codes for brand."""
        # prepare codes
        services.generate_codes(no_of_codes=10)
        data = {
            "brand": self.BRAND_REFERENCE,
            "count": 5,
            "discount_type": "AMOUNT",
            "discount_value": 200.00,
        }
        response = api_client().post(self.ENDPOINT, data=data, format="json")

        assert response.status_code == 201
        assert (
            BrandCode.objects.filter(brand=self.BRAND_REFERENCE, is_active=True).count()
            == data["count"]
        )

    def test_get_a_code(self, api_client):
        """Test get a code."""
        services.generate_codes(no_of_codes=1)
        BrandCode.objects.create(
            code=Code.objects.first(), brand=self.BRAND_REFERENCE, discount_value=200.00
        )
        assert BrandCode.objects.filter(brand=self.BRAND_REFERENCE, is_active=True).count() > 0

        response = api_client().get(self.ENDPOINT + "apply/")
        json_response = json.loads(response.content)

        assert response.status_code == 200
        assert len(json_response["code"]) == settings.CODE_SIZE
