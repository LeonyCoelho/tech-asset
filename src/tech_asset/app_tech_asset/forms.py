from django import forms
from .models import Category, SubCategory, Sector, SubSector, RentalCompany, Asset

class GlobalForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    internalcode01 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    internalcode02 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    internalcode03 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))

class CategoryForm(forms.Form):
    Nova_Categoria = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

class SubCategoryForm(forms.Form):
    Nova_SubCategoria = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

class SectorForm(forms.Form):
    Novo_Setor = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

class SubSectorForm(forms.Form):
    Novo_SubSetor = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

class RentalCompanyForm(forms.Form):
    Nova_Empresa = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

class AssetForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.all(), required=False,  widget=forms.Select(attrs={'class': 'form-select'}))
    sector = forms.ModelChoiceField(queryset=Sector.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    subsector = forms.ModelChoiceField(queryset=SubSector.objects.all(), required=False,  widget=forms.Select(attrs={'class': 'form-select'}))
    rental_company = forms.ModelChoiceField(queryset=RentalCompany.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    internal_code1 = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    internal_code2 = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    internal_code3 = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    serial_number = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    brand = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mac_address = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    windows_license = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
