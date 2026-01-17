from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import Payments, User
from .serializers import PaymentsSerializer, UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentsViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]  # Фильтр для поиска filters.SearchFilter
    filterset_fields = (
        "method_payment",
        "lesson_paid",
        "course_paid",
    )
    ordering_fields = ("date_payment",)
    # search_fields Для поиска
