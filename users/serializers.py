from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Payments, User


class UserSerializer(ModelSerializer):
    """Сериализатор пользователя"""

    class Meta:
        model = User
        fields = "__all__"


class PaymentsSerializer(ModelSerializer):
    """Сериализатор по платежам"""

    class Meta:
        model = Payments
        fields = "__all__"
