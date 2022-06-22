from django.urls import path
import views

urlpatterns = [
    path('', views.sign_up),
    path('email_confirm/', views.email_confirm),
]
