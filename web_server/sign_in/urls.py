from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in),
    path('reset_keywords/', views.reset_password),
]
