from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("upload/", views.upload_view, name="upload"),
    path("editor/", views.editor_view, name="editor"),
    path("clip/<str:uuid>/", views.detail_view, name="detail"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("explore/", views.explore_view, name="explore"),
    path("delete/<str:uuid>/", views.delete_view, name="delete"),
]
