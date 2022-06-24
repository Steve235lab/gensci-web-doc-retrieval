from django.urls import path
from . import views

urlpatterns = [
    path('', views.search),
    path('history/', views.get_history),
    path('result/', views.get_result),
]
