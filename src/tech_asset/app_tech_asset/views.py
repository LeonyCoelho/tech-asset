from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.models import User
from app_tech_asset.forms import CategoryForm, SubCategoryForm, SectorForm,SubSectorForm, RentalCompanyForm, AssetForm, GlobalForm
from app_tech_asset.models import Category, SubCategory, Sector,SubSector , RentalCompany, Asset, AssetHistory, GlobalSettings
from django.core.paginator import Paginator
import qrcode
from io import BytesIO


def home(request):
    return render(request, 'home.html')


def preferences(request):
    categoryform = CategoryForm()
    subcategoryform = SubCategoryForm()
    sectorform = SectorForm()
    subsectorform = SubSectorForm()
    rentalcompanyform = RentalCompanyForm()
    globalform = GlobalForm()
    context = {
        'categoryform': categoryform,
        'subcategoryform': subcategoryform,
        'sectorform': sectorform,
        'subsectorform': subsectorform,
        'rentalcompanyform': rentalcompanyform,
        'globalform': globalform,
    }
    return render(request, 'preferences.html', context)
def global_settings(request):
    if request.method == 'POST':
        globalform = GlobalForm(request.POST)
        if globalform.is_valid():
            # Recupera ou cria a única instância de GlobalSettings
            global_settings, created = GlobalSettings.objects.get_or_create(id=1)
            
            # Atualiza os campos com os dados do formulário
            global_settings.name = globalform.cleaned_data['name']
            global_settings.internalcode01 = globalform.cleaned_data['internalcode01']
            global_settings.internalcode02 = globalform.cleaned_data['internalcode02']
            global_settings.internalcode03 = globalform.cleaned_data['internalcode03']
            global_settings.save()
            
            return redirect('/preferences/')
    else:
        # Tenta recuperar a instância existente ou cria uma instância vazia para o formulário
        try:
            global_settings = GlobalSettings.objects.get(id=1)
            globalform = GlobalForm(initial={
                'name': global_settings.name,
                'internalcode01': global_settings.internalcode01,
                'internalcode02': global_settings.internalcode02,
                'internalcode03': global_settings.internalcode03,
            })
        except GlobalSettings.DoesNotExist:
            globalform = GlobalForm()

    return render(request, 'global_settings.html', {'globalform': globalform})
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
    sector_list = Sector.objects.all()
    subsector_list = SubSector.objects.all()

    # Adicionando paginação
    paginator = Paginator(asset_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sector_list': sector_list,
        'subsector_list': subsector_list,
        
    }
    return render(request, 'list_asset.html', context)


def new_asset(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        sector_id = request.POST.get('sector')
        subsector_id = request.POST.get('subsector')
        rental_company_id = request.POST.get('rental_company')
        internal_code1 = request.POST.get('internal_code1')
        internal_code2 = request.POST.get('internal_code2')
        internal_code3 = request.POST.get('internal_code3')
        serial_number = request.POST.get('serial_number')
        brand = request.POST.get('brand')
        mac_address = request.POST.get('mac_address')
        windows_license = request.POST.get('windows_license')

        category = Category.objects.get(id=category_id)
        subcategory = SubCategory.objects.get(id=subcategory_id) if subcategory_id else None
        sector = Sector.objects.get(id=sector_id)
        subsector = SubSector.objects.get(id=subsector_id) if subsector_id else None
        rental_company = RentalCompany.objects.get(id=rental_company_id)

        asset = Asset.objects.create(
            name=name,
            category=category,
            subcategory=subcategory,
            sector=sector,
            subsector=subsector,
            rental_company=rental_company,
            internal_code1=internal_code1,
            internal_code2=internal_code2,
            internal_code3=internal_code3,
            serial_number=serial_number,
            brand=brand,
            mac_address=mac_address,
            windows_license=windows_license
        )

        AssetHistory.objects.create(
            asset_id=asset,
            modification_type='Criação',
            name=asset.name,
            category=asset.category.name,
            modified=asset.modified,
            user=request.user.username,
            details=asset.details,
            sector=asset.sector.name,
            rental_company=asset.rental_company.name,
            internal_code1=asset.internal_code1,
            internal_code2=asset.internal_code2,
            internal_code3=asset.internal_code3,
            serial_number=asset.serial_number,
            brand=asset.brand,
            mac_address=asset.mac_address,
            windows_license=asset.windows_license
        )

        return redirect('list_asset')
    else:

        return render(request, 'new_asset.html')
    
def delete_asset(request, id):
    asset = get_object_or_404(Asset, id=id)
    if request.method == 'POST':
        asset.delete()
        return redirect('list_asset')
    
def transfer_asset(request, id):
    asset = get_object_or_404(Asset, id=id)
    if request.method == 'POST':
        new_sector_id = request.POST.get('sector')
        new_subsector_id = request.POST.get('subsector')
        
        # Salvar o estado anterior do asset para registrar no histórico
        previous_sector = asset.sector
        previous_subsector = asset.subsector
        
        if new_sector_id:
            new_sector = get_object_or_404(Sector, id=new_sector_id)
            asset.sector = new_sector
        if new_subsector_id:
            new_subsector = get_object_or_404(SubSector, id=new_subsector_id)
            asset.subsector = new_subsector
        else:
            asset.subsector = None
        asset.save()
        
        # Criar registro no histórico
        AssetHistory.objects.create(
            asset_id=asset,
            modification_type='Transfer',
            name=asset.name,
            category=asset.category.name,
            modified=asset.modified,
            user=request.user.username,
            details=asset.details,
            sector=new_sector.name if new_sector_id else previous_sector.name,
            rental_company=asset.rental_company.name,
            internal_code1=asset.internal_code1,
            internal_code2=asset.internal_code2,
            internal_code3=asset.internal_code3,
            serial_number=asset.serial_number,
            brand=asset.brand,
            mac_address=asset.mac_address,
            windows_license=asset.windows_license
        )
        
        return redirect('list_asset')
    return redirect('list_asset')

def edit_asset(request, id):
    # Recuperar o ativo existente
    asset = get_object_or_404(Asset, id=id)
    
    if request.method == 'POST':
        # Processar o formulário enviado
        asset.name = request.POST.get('name')
        asset.rental_company = get_object_or_404(RentalCompany, id=request.POST.get('rental_company'))
        asset.internal_code1 = request.POST.get('internal_code1')
        asset.internal_code2 = request.POST.get('internal_code2')
        asset.internal_code3 = request.POST.get('internal_code3')
        asset.serial_number = request.POST.get('serial_number')
        asset.brand = request.POST.get('brand')
        asset.mac_address = request.POST.get('mac_address')
        asset.windows_license = request.POST.get('windows_license')
        
        asset.save()
        
        return redirect('list_asset')
    
    else:
        
        context = {
            'asset': asset,
        }
        
        return render(request, 'edit_asset.html', context)

def generate_qr_code(request, id):
    asset = get_object_or_404(Asset, pk=id)
    settings = GlobalSettings.objects.first()

    content_list = [
        f"ID: {asset.id}",
        f"{settings.internalcode01}: {asset.internal_code1}",
        f"Empresa: {asset.rental_company}",
        f"Categoria: {asset.category}" + (f" - {asset.subcategory}" if asset.subcategory else ""),
        f"Marca: {asset.brand}",
        f"Modelo: {asset.name}",
        f"Nº de Série: {asset.serial_number}",
        f"{settings.internalcode02}: {asset.internal_code2}",
        f"MAC Address: {asset.mac_address}"
    ]
    
    content = "\n".join(content_list)
    
    qr = qrcode.make(content)
    buffer = BytesIO()
    qr.save(buffer)
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='image/png')
    return response

def history(request, id):
    asset = get_object_or_404(Asset, id=id)
    history_list = AssetHistory.objects.filter(asset_id=asset).order_by('-modified')
    
    paginator = Paginator(history_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'asset': asset,
        'page_obj': page_obj,
    }
    return render(request, 'history.html', context)
    

    # =================== UTILITY ===================================

def get_subsectors(request):
    sector_id = request.GET.get('sector_id')
    subsectors = SubSector.objects.filter(parent_id=sector_id).values('id', 'name')
    return JsonResponse({'subsectors': list(subsectors)})

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(parent_id=category_id).values('id', 'name')
    return JsonResponse({'subcategories': list(subcategories)})
