from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from codes import services
from codes.serializers import BrandCodeInputSerializer, BrandCodeSerializer


class CodeView(APIView):
    """Get single BrandCode data."""

    @swagger_auto_schema(responses={"200": BrandCodeSerializer})
    def get(self, request, brand, format=None):
        """Get single code of a brand."""
        # TODO: using request token, derive the user data
        code = services.get_code_by_brand(brand=brand, assigned_to="TEMPUSER")
        serializer = BrandCodeSerializer(code)
        return Response(serializer.data)


class CodeAction(APIView):
    """Code model related CRUD actions."""

    def get(self, request, count: int, format=None):
        """Generate buffer code list."""
        result = services.generate_codes(no_of_codes=count)
        if result:
            return Response({"status": result}, status=status.HTTP_200_OK)
        else:
            return Response({"status": result}, status=status.HTTP_400_BAD_REQUEST)


class CodeList(APIView):
    """List or create code for a brand."""

    @swagger_auto_schema(
        request_body=BrandCodeInputSerializer, responses={"200": BrandCodeSerializer(many=True)}
    )
    def post(self, request, format=None):
        """Generate some codes to a brand."""
        request_data = request.data
        serializer = BrandCodeInputSerializer(data=request_data)
        if serializer.is_valid():
            count = request_data["count"]
            # remove key 'count'
            request_data.pop("count")
            codes = services.add_codes_to_brand(no_of_codes=count, data=request_data)

            # prepare the response
            serializer = BrandCodeSerializer(data=codes, many=True)
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
