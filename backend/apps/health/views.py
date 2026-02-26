from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_health_status


class HealthCheckView(APIView):
    """Health check endpoint returning service and database status."""

    authentication_classes = []
    permission_classes = []

    def get(self, request: Request) -> Response:
        result = get_health_status()
        status_code = 200 if result["status"] == "healthy" else 503
        return Response(result, status=status_code)
