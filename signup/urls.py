from django.urls import path
from signup import views

urlpatterns = [
    #path('signup/', views.HelloApiView.as_view()),
    path('registro/', views.RegistroUsuario.as_view()),
    path('signup/<pk>/', views.RegistroUsuarioUpdateDelete.as_view()),
    path('signup/', views.SignUpView.as_view(), name='registro_usuario'),
]

