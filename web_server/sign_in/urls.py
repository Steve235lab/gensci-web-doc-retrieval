from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in),
    path('email_confirm/', views.email_confirm),
    path('reset_password/', views.reset_password),
]
