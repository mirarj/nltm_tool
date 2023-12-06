from django.urls import path

from . import views

urlpatterns = [
    path("", views.editor, name="editor"),
    path('upload/', views.upload_file, name='upload_file'),
]