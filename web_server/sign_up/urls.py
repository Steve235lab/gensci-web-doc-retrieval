from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_up),
    path('email_confirm/', views.email_confirm),
]
