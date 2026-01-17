from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from .models import Payments
from .serializers import PaymentsSerializer


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
