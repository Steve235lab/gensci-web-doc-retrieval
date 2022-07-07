"""web_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from run_search import SEARCH_RUNNER
from django.http import HttpResponse
from database_new import DATABASE


def enable_undeadthread(request):
    import threading
    if DATABASE.undead_thread_on is False:
        threading.Thread(target=SEARCH_RUNNER.search_thread, daemon=True).start()
        DATABASE.undead_thread_on = True
        return HttpResponse("It works!")
    else:
        return HttpResponse("It's already running!")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign_up/', include('sign_up.urls')),
    path('sign_in/', include('sign_in.urls')),
    path('search/', include('search.urls')),
    path('undeadthread/', enable_undeadthread),
]

