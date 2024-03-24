from django.contrib import admin
from django.urls import path
from app_tech_asset import views

urlpatterns = [
    path('', views.home, name='home'),
    path('preferences/', views.preferences, name='preferences'),
    path('preferences/new_category/', views.new_category, name='new_category'),
    path('preferences/new_subcategory/', views.new_subcategory, name='new_subcategory'),
    path('preferences/new_sector/', views.new_sector, name='new_sector'),
    path('preferences/new_subsector/', views.new_subsector, name='new_subsector'),
    path('preferences/new_rentalcompany/', views.new_rentalcompany, name='new_rentalcompany'),

    path('asset/', views.list_asset, name='list_asset'),
    path('asset/new', views.new_asset, name='new_asset'),
    path('get_subsectors/', views.get_subsectors, name='get_subsectors'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('asset/list', views.list_asset, name='list_asset'),

]

