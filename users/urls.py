from django.urls import path

from .apps import UsersConfig
from .views import PaymentsViewSet
from rest_framework.routers import SimpleRouter

app_name = UsersConfig.name

router = SimpleRouter()

router.register("", PaymentsViewSet)

urlpatterns = [
    # path("register/", RegisterView.as_view(), name="register"),
    # path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    # path("logout/", LogoutView.as_view(next_page="catalog:prod_list"), name="logout"),
]

urlpatterns += router.urls
