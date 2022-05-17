from django.urls import path
from forgotpsw import views

urlpatterns = [
    path('forgotpsw/', views.ForgotpswView.as_view(), name='Contrasena_nueva'),
]

