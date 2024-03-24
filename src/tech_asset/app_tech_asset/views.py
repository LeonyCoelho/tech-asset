from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from app_tech_asset.forms import CategoryForm, SubCategoryForm, SectorForm,SubSectorForm, RentalCompanyForm, AssetForm
from app_tech_asset.models import Category, SubCategory, Sector,SubSector , RentalCompany, Asset


def home(request):
    return render(request, 'home.html')


def preferences(request):
    category_list = Category.objects.all()
    subcategory_list = SubCategory.objects.all()
    sector_list = Sector.objects.all()
    subsector_list = SubSector.objects.all()
    rentalcompany_list = RentalCompany.objects.all()
    categoryform = CategoryForm()
    subcategoryform = SubCategoryForm()
    sectorform = SectorForm()
    subsectorform = SubSectorForm()
    rentalcompanyform = RentalCompanyForm()
    context = {
        'categoryform': categoryform,
        'subcategoryform': subcategoryform,
        'sectorform': sectorform,
        'subsectorform': subsectorform,
        'rentalcompanyform': rentalcompanyform,

        'category_list':category_list,
        'subcategory_list':subcategory_list,
        'sector_list':sector_list,
        'subsector_list':subsector_list,
        'rentalcompany_list':rentalcompany_list,
    }
    return render(request, 'preferences.html', context)

def new_category(request):
    if request.method == 'POST':
        categoryform = CategoryForm(request.POST)
        if categoryform.is_valid():
            new_category = Category(name=categoryform.cleaned_data['Nova_Categoria'])
            new_category.save()
            return HttpResponseRedirect("/preferences/")
    else:
        categoryform = CategoryForm()

def new_subcategory(request):
    if request.method == 'POST':
        subcategoryform = SubCategoryForm(request.POST)
        if subcategoryform.is_valid():
            new_subcategory = SubCategory(name=subcategoryform.cleaned_data['Nova_SubCategoria'])
            new_subcategory.save()
            return HttpResponseRedirect("/preferences/")
    else:
        subcategoryform = SubCategoryForm()

def new_sector(request):
    if request.method == 'POST':
        sectorform = SectorForm(request.POST)
        if sectorform.is_valid():
            new_sector = Sector(name=sectorform.cleaned_data['Novo_Setor'])
            new_sector.save()
            return HttpResponseRedirect("/preferences/")
    else:
        sectorform = SectorForm()

def new_subsector(request):
    if request.method == 'POST':
        subsectorform = SubSectorForm(request.POST)
        if subsectorform.is_valid():
            new_subsector = Sector(name=subsectorform.cleaned_data['Novo_SubSetor'])
            new_subsector.save()
            return HttpResponseRedirect("/preferences/")
    else:
        subsectorform = SubSectorForm()

def new_rentalcompany(request):
    if request.method == 'POST':
        rentalcompanyform = RentalCompanyForm(request.POST)
        if rentalcompanyform.is_valid():
            new_rentalcompany = RentalCompany(name=rentalcompanyform.cleaned_data['Nova_Empresa'])
            new_rentalcompany.save()
            return HttpResponseRedirect("/preferences/")
    else:
        rentalcompanyform = RentalCompanyForm()


def list_asset(request):
    asset_list = Asset.objects.all()
    context = {
        'asset_list':asset_list,
        }
    return render(request, 'list_asset.html', context)

def new_asset(request):
    if request.method == 'POST':
        asset_form = AssetForm(request.POST)
        if asset_form.is_valid():
            asset = Asset(
                name=asset_form.cleaned_data['name'],
                category=asset_form.cleaned_data['category'],
                subcategory=asset_form.cleaned_data['subcategory'],
                sector=asset_form.cleaned_data['sector'],
                subsector=asset_form.cleaned_data['subsector'],
                rental_company=asset_form.cleaned_data['rental_company'],
                internal_code1=asset_form.cleaned_data['internal_code1'],
                internal_code2=asset_form.cleaned_data['internal_code2'],
                internal_code3=asset_form.cleaned_data['internal_code3'],
                serial_number=asset_form.cleaned_data['serial_number'],
                brand=asset_form.cleaned_data['brand'],
                mac_address=asset_form.cleaned_data['mac_address'],
                windows_license=asset_form.cleaned_data['windows_license']
            )
            asset.save()
            return HttpResponseRedirect("/list_asset/")
    else:
        asset_form = AssetForm()

    return render(request, 'new_asset.html', {'asset_form': asset_form})

def get_subsectors(request):
    sector_id = request.GET.get('sector_id')
    subsectors = SubSector.objects.filter(parent_id=sector_id).values('id', 'name')
    return JsonResponse({'subsectors': list(subsectors)})

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(parent_id=category_id).values('id', 'name')
    return JsonResponse({'subcategories': list(subcategories)})
