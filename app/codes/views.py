from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from codes import services


class CodeAction(APIView):
    """Code model related CRUD actions."""

    def get(self, request, count: int, format=None):
        """Generate buffer code list."""
        result = services.generate_codes(no_of_codes=count)
        if result:
            return Response({"status": result}, status=status.HTTP_200_OK)
        else:
            return Response({"status": result}, status=status.HTTP_400_BAD_REQUEST)
