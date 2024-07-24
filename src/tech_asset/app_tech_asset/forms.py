from django import forms
from .models import Category, SubCategory, Sector, SubSector, RentalCompany, Asset, Kit, GlobalSettings

class GlobalForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'name'}))
    internalcode01 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    internalcode02 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
    internalcode03 = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(GlobalForm, self).__init__(*args, **kwargs)
        try:
            global_settings = GlobalSettings.objects.first()
            if global_settings:
                self.fields['name'].initial = global_settings.name
                self.fields['internalcode01'].initial = global_settings.internalcode01
                self.fields['internalcode02'].initial = global_settings.internalcode02
                self.fields['internalcode03'].initial = global_settings.internalcode03
        except GlobalSettings.DoesNotExist:
            pass

class CategoryForm(forms.Form):
    Nova_Categoria = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

class SubCategoryForm(forms.Form):
    Nova_SubCategoria = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    parent = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Selecione a Categoria"
    )
    Nova_SubCategoria = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Novo Subsetor'})
    )

class SectorForm(forms.Form):
    Novo_Setor = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Novo Setor'}))

class SubSectorForm(forms.Form):
    parent = forms.ModelChoiceField(
        queryset=Sector.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Selecione o Setor"
    )
    Novo_SubSetor = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Novo Subsetor'})
    )

class KitForm(forms.ModelForm):
    assets = forms.ModelMultipleChoiceField(
        queryset=Asset.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )

    class Meta:
        model = Kit
        fields = ['name', 'sectors', 'subsectors', 'assets']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Nome do Kit'}),
            'sectors': forms.Select(attrs={'class': 'form-control mb-3'}),
            'subsectors': forms.Select(attrs={'class': 'form-control mb-3'}),
        }
        
class RentalCompanyForm(forms.Form):
    Nova_Empresa = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

class AssetForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Selecione o Setor"
        )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Selecione o Setor"
        )
    sector = forms.ModelChoiceField(
        queryset=Sector.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Selecione o Setor"
    )
    subsector = forms.ModelChoiceField(
        queryset=SubSector.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Selecione o Setor"
    )
    rental_company = forms.ModelChoiceField(queryset=RentalCompany.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    internal_code1 = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    internal_code2 = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    internal_code3 = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    serial_number = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    brand = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mac_address = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    windows_license = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
