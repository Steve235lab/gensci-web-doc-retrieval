from django.urls import path
import views

urlpatterns = [
    path('', views.sign_in),
]
