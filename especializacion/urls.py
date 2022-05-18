from django.urls import path
from especializacion import views

urlpatterns = [
    path('especializacion/', views.EspecializacionView.as_view())
]