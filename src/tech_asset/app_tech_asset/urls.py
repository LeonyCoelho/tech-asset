from django.contrib import admin
from django.urls import path
from app_tech_asset import views

urlpatterns = [
    path('', views.home, name='home'),
    path('preferences/', views.preferences, name='preferences'),
    path('preferences/global_settings/', views.global_settings, name='global_settings'),
    path('preferences/new_category/', views.new_category, name='new_category'),
    path('preferences/new_subcategory/', views.new_subcategory, name='new_subcategory'),
    path('preferences/new_sector/', views.new_sector, name='new_sector'),
    path('preferences/sector/delete/<int:id>/', views.delete_sector, name='delete_sector'),
    path('preferences/new_subsector/', views.new_subsector, name='new_subsector'),
    path('preferences/new_rentalcompany/', views.new_rentalcompany, name='new_rentalcompany'),

    path('filter_assets', views.filter_assets, name='filter_assets'),

    path('asset/', views.list_asset, name='list_asset'),
    path('asset/list', views.list_asset, name='list_asset'),
    path('asset/new', views.new_asset, name='new_asset'), 
    path('asset/view/<int:id>/', views.view_asset, name='view_asset'),
    path('asset/delete/<int:id>/', views.delete_asset, name='delete_asset'),
    path('asset/transfer/<int:id>/', views.transfer_asset, name='transfer_asset'),
    path('asset/history/<int:id>/', views.history, name='history_asset'),
    path('asset/edit/<int:id>/', views.edit_asset, name='edit_asset'),
    path('asset/generate_qr_code/<int:id>/', views.generate_qr_code, name='generate_qr_code'),
 
    path('kit/new/', views.new_kit, name='new_kit'),
    path('kit/view/<int:id>', views.view_kit, name='view_kit'),
    path('kit/delete/<int:id>/', views.delete_kit, name='delete_kit'),
    path('kit/transfer/<int:id>/', views.transfer_kit, name='transfer_kit'),
 
    path('get_subsectors/', views.get_subsectors, name='get_subsectors'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),

]

