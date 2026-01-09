from .apps import UsersConfig
from django.urls import path

app_name = UsersConfig.name

#
# urlpatterns = [
#     path("register/", RegisterView.as_view(), name="register"),
#     path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
#     path("logout/", LogoutView.as_view(next_page="catalog:prod_list"), name="logout"),
# ]
