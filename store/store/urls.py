"""
URL configuration for store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from products.views import *

urlpatterns = [ 
    path('admin/', admin.site.urls), 
    path('', home, name='index'), 
    path('FOURSEASON/about', about, name='index2'), 
    path('FOURSEASON/profile', profile, name='index3'), 
    path('FOURSEASON/catalog', catalog, name='index4'), 
    path('FOURSEASON/reservation/<int:number_id>/', reservation_number, name='reservation_number'), # Изменено 
    path('FOURSEASON/reservation_successfully/', reservation_successfully, name='reservation_successfully'), 
    path('FOURSEASON/authorization', authorization, name='index7'), 
    path('FOURSEASON/registration', registration, name='index8'), 
    path('custom_logout/', custom_logout, name='custom_logout'), 
    path('update_number/', update_room, name='update_number'),
    path('delete_number/<int:number_id>/', delete_number, name='delete_number'),
    path('FOURSEASON/catalog/addNumber', add_number, name='index9'),
    path('add/', add_hotel_number, name='add_hotel_number'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 