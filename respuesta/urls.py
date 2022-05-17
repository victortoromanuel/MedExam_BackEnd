from django.urls import path
from respuesta import views

urlpatterns = [
    path('respuesta/', views.RespuestaView.as_view())
]