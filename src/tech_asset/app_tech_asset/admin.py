from django.contrib import admin
from .models import CustomUser, GlobalSettings, Category, SubCategory, Sector,SubSector, RentalCompany, Asset, Kit, AssetQR, AssetHistory

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['full_name']

@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(SubSector)
class SubSectorAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(RentalCompany)
class RentalCompanyAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'sector', 'rental_company']

@admin.register(Kit)
class KitAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(AssetQR)
class AssetQRAdmin(admin.ModelAdmin):
    list_display = ['asset', 'qr_code']

@admin.register(AssetHistory)
class AssetHistoryAdmin(admin.ModelAdmin):
    list_display = ['asset_id', 'modification_type', 'name', 'category', 'modified', 'user', 'sector', 'rental_company', 'internal_code1', 'internal_code2', 'internal_code3', 'serial_number', 'brand', 'mac_address', 'windows_license']
