from django.urls import path

from user import views

app_name = "user"  # pylint: disable=invalid-name

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("api_token/", views.CreateTokenView.as_view(), name="api_token"),
    path("me/", views.ManageUserView.as_view(), name="me"),
]
