from django.db import models
from django.contrib.auth.models import User

# ================= SETTINGS ======================
class CustomUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name
class GlobalSettings(models.Model):
    name = models.CharField(null=True, max_length=50)

# ================== APP MAIN DATABASE ===============
class Category(models.Model):
    name = models.CharField(null=False, max_length=50)
    def __str__(self):
        return self.name
class SubCategory(models.Model):
    parent = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=50)
    def __str__(self):
        return self.name
class Sector(models.Model):
    name = models.CharField(null=False, max_length=50)
    def __str__(self):
        return self.name
class SubSector(models.Model):
    parent = models.ForeignKey(Sector, blank=True, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=50)
    def __str__(self):
        return self.name
class RentalCompany(models.Model):
    name = models.CharField(null=False, max_length=50)
    def __str__(self):
        return self.name
class Asset(models.Model):
    name = models.CharField(null=False, max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    modified = models.DateTimeField(auto_now_add=True)
    added = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    subsector = models.ForeignKey(SubSector, blank=True, on_delete=models.CASCADE)
    rental_company = models.ForeignKey(RentalCompany, on_delete=models.CASCADE)
    internal_code1 = models.CharField(null=True, max_length=50)
    internal_code2 = models.CharField(null=True, max_length=50)
    internal_code3 = models.CharField(null=True, max_length=50)
    serial_number = models.CharField(null=True, max_length=50)
    brand = models.CharField(null=True, max_length=50)
    mac_address = models.CharField(null=True, max_length=50)
    windows_license = models.CharField(null=True, max_length=50)
    def __str__(self):
        return self.name
class Kit(models.Model):
    assets = models.ManyToManyField(Asset)
    sectors = models.ManyToManyField(Sector)
    def __str__(self):
        return self.name
class AssetQR(models.Model):
    asset = models.OneToOneField(Asset , on_delete=models.CASCADE)
    qr_code = models.TextField(null=True)
    def __str__(self):
        return self.name
class AssetHistory(models.Model):
    asset_id = models.ForeignKey(Asset, on_delete=models.CASCADE)
    modification_type = models.CharField(null=False, max_length=50)
    name = models.CharField(null=False, max_length=50)
    category = models.CharField(null=False, max_length=50)
    modified = models.DateTimeField(auto_now_add=True)
    user = models.CharField(null=False, max_length=50)
    details = models.TextField(null=True)
    sector = models.CharField(null=False, max_length=50)
    rental_company = models.CharField(null=False, max_length=50)
    internal_code1 = models.CharField(null=True, max_length=50)
    internal_code2 = models.CharField(null=True, max_length=50)
    internal_code3 = models.CharField(null=True, max_length=50)
    serial_number = models.CharField(null=True, max_length=50)
    brand = models.CharField(null=True, max_length=50)
    mac_address = models.CharField(null=True, max_length=50)
    windows_license = models.CharField(null=True, max_length=50)
    def __str__(self):
        return self.name


