from django.urls import path
from tableResults import views

urlpatterns = [
    path('table/', views.TableView.as_view()),
]
