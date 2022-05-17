from django.urls import path
from formulario import views

urlpatterns = [
    path('formulario/', views.FormularioView.as_view())
]