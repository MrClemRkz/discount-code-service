import pytest

from codes.models import Code


class TestCode:
    """Test code module."""

    ENDPOINT = "/codes/"

    @pytest.mark.django_db
    def test_generate_codes(self, api_client):
        """Test gernerating codes."""
        assert Code.objects.count() == 0

        response = api_client().get(self.ENDPOINT + "generate/10")

        assert response.status_code == 200
        assert Code.objects.count() == 110
