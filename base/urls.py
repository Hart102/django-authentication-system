from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_login, name="login"),
    path("register/", views.user_registration, name="register"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/<str:pk>/", views.user_profile, name="profile"),
    path("update_profile/<str:pk>/", views.user_update_profile, name="update_profile"),
    path("delete/<str:pk>/", views.delete_account, name="delete_account"),
]