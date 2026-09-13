from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from tracker import views as tracker_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path("login/", auth_views.LoginView.as_view(template_name="tracker/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", tracker_views.register, name="register"),

    # Public
    path("", tracker_views.landing, name="landing"),
    path("demo/", tracker_views.demo, name="demo"),

    # App
    path("app/", include("tracker.urls")),
]
