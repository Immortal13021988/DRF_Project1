from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .apps import UsersConfig
from .views import (PaymentsViewSet, UserCreateAPIView, UserDestroyAPIView,
                    UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView)

app_name = UsersConfig.name

router = SimpleRouter()

router.register("payments", PaymentsViewSet)

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("", UserListAPIView.as_view(), name="users_list"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="users_detail"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="users_update"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="users_delete"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    # path(
    #     "pay/", PaymentsCreateAPIView.as_view(), name="pay"
    # )  #  Вариант с PaymentsCreateAPIView не забыть добавить в импорт
]

urlpatterns += router.urls
