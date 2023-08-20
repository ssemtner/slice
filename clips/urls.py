from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload, name="upload"),
    path("editor/", views.editor, name="editor"),
    path("clip/<str:uuid>/", views.detail, name="detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
