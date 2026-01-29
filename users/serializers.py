from rest_framework import serializers

from .models import Payments, User
from .services import retrieve_stripe_session


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""

    class Meta:
        model = User
        fields = "__all__"


class PaymentsSerializer(serializers.ModelSerializer):
    """Сериализатор по платежам"""

    is_payments = serializers.SerializerMethodField()

    def get_is_payments(self, payment):  # Получения статуса платежа
        session_data = retrieve_stripe_session(payment.session_id)
        if session_data:
            print(session_data)  # Проверочный принт
            return session_data["payment_status"]
        else:
            return None

    class Meta:
        model = Payments
        fields = [
            "id",
            "date_payment",
            "amount",
            "method_payment",
            "session_id",
            "link",
            "user",
            "course_paid",
            "is_payments",
        ]
