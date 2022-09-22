from django.urls import path

from .views import ProfileUpdateAPI, UserListAPI, UserCreateAPI

app_name = "account"
urlpatterns = [
    # Home page.
    path("register", UserCreateAPI.as_view(), name="register"),
    path("list", UserListAPI.as_view(), name="list"),
    path("me", ProfileUpdateAPI.as_view(), name="update"),
]
