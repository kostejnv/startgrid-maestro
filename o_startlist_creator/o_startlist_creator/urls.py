"""o_startlist_creator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from .views import get_event, solve_event

ROOT_URI = 'api/'
def get_full_request_URI(partially_request:str)-> str:
    return ROOT_URI+partially_request


urlpatterns = [
    path(get_full_request_URI('admin/'), admin.site.urls),
    path(get_full_request_URI('get_event'), get_event),
    path(get_full_request_URI('solve'), solve_event),
]
