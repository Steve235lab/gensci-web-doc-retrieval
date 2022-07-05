from django.urls import path
from . import views

urlpatterns = [
    path('', views.search),
    path('history/', views.get_history),
    path('paper_info/', views.get_paper_info),
    path('clue_info/', views.get_clue_info),
    path('paper_details/', views.get_paper_details),
    path('download/', views.download_file),
]
