from rest_framework.generics import ListAPIView

from .models import FoodBank
from .serializers import FoodBankSerializer


class FoodBankListView(ListAPIView):
    queryset = FoodBank.objects.all()
    serializer_class = FoodBankSerializer
    authentication_classes = []
    permission_classes = []
