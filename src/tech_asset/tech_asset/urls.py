from django.contrib import admin
from django.urls import path, include
from app_tech_asset import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_tech_asset.urls'),),
]
