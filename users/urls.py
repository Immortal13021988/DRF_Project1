from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .apps import UsersConfig
from .views import PaymentsViewSet, UserCreateAPIView

app_name = UsersConfig.name

router = SimpleRouter()

router.register("", PaymentsViewSet)

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    # path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    # path("logout/", LogoutView.as_view(next_page="catalog:prod_list"), name="logout"),
    path(
        "login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]

urlpatterns += router.urls
