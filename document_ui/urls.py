from django.urls import path

from . import views

urlpatterns = [
    # ex: /scanner/
    path("", views.upload_and_preview, name="index"),
]
