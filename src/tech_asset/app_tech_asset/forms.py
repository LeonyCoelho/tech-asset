from django import forms
from .models import Category, SubCategory, Sector, SubSector, RentalCompany


class CategoryForm(forms.Form):
    Nova_Categoria = forms.CharField(max_length=50)

class SubCategoryForm(forms.Form):
    Nova_SubCategoria = forms.CharField(max_length=50)

class SectorForm(forms.Form):
    Novo_Setor = forms.CharField(max_length=50)

class SubSectorForm(forms.Form):
    Novo_SubSetor = forms.CharField(max_length=50)

class RentalCompanyForm(forms.Form):
    Nova_Empresa = forms.CharField(max_length=50)

class AssetForm(forms.Form):
    name = forms.CharField(max_length=50)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.all())
    sector = forms.ModelChoiceField(queryset=Sector.objects.all())
    subsector = forms.ModelChoiceField(queryset=SubSector.objects.all())
    rental_company = forms.ModelChoiceField(queryset=RentalCompany.objects.all())
    internal_code1 = forms.CharField(max_length=50, required=False)
    internal_code2 = forms.CharField(max_length=50, required=False)
    internal_code3 = forms.CharField(max_length=50, required=False)
    serial_number = forms.CharField(max_length=50, required=False)
    brand = forms.CharField(max_length=50, required=False)
    mac_address = forms.CharField(max_length=50, required=False)
    windows_license = forms.CharField(max_length=50, required=False)