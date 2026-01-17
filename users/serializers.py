from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Payments


class PaymentsSerializer(ModelSerializer):
    """Сериализатор по платежам"""

    class Meta:
        model = Payments
        fields = "__all__"

