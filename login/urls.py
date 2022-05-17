from django.urls import path
from login import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login_usuario'),
    path('login/<int:id>', views.LoginView.as_view(), name='login_usuario_id'),
]

