from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.models import User
from app_tech_asset.forms import CategoryForm, SubCategoryForm, SectorForm,SubSectorForm, RentalCompanyForm, AssetForm, GlobalForm, KitForm
from app_tech_asset.models import Category, SubCategory, Sector, SubSector , RentalCompany, Asset, AssetHistory, GlobalSettings, Kit, KitHistory
from django.core.paginator import Paginator
import qrcode
from io import BytesIO



# FOLLOWING VIEWS WILL HANDLE THE TEMPLATE RENDER
#================================================================================================

def home(request):
    asset_list = Asset.objects.all()
    sector_list = Sector.objects.all()
    subsector_list = SubSector.objects.all()
    sector_list_alt = Sector.objects.prefetch_related('subsector_set').all()
    subsector_list_alt = SubSector.objects.all()
    kit_list = Kit.objects.all()

    sectorform = SectorForm()
    subsectorform = SubSectorForm()
    kitform = KitForm()

    paginator = Paginator(asset_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'asset_list': asset_list,
        'sector_list': sector_list,
        'subsector_list': subsector_list,
        'sector_list_alt': sector_list_alt,
        'subsector_list_alt': subsector_list_alt,
        'kit_list': kit_list,
        'sectorform': sectorform,
        'subsectorform': subsectorform,
        'kitform': kitform,        
    }
    return render(request, 'home.html', context)

def list_asset(request):
    asset_list = Asset.objects.all()
    sector_list = Sector.objects.all()
    subsector_list = SubSector.objects.all()
    sector_list_alt = Sector.objects.prefetch_related('subsector_set').all()
    subsector_list_alt = SubSector.objects.all()
    kit_list = Kit.objects.all()

    sectorform = SectorForm()
    subsectorform = SubSectorForm()
    kitform = KitForm()

    paginator = Paginator(asset_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'asset_list': asset_list,
        'sector_list': sector_list,
        'subsector_list': subsector_list,
        'sector_list_alt': sector_list_alt,
        'subsector_list_alt': subsector_list_alt,
        'kit_list': kit_list,
        'sectorform': sectorform,
        'subsectorform': subsectorform,
        'kitform': kitform,        
    }
    return render(request, 'list_asset.html', context)

def preferences(request):
    categoryform = CategoryForm()
    subcategoryform = SubCategoryForm()
    sectorform = SectorForm()
    subsectorform = SubSectorForm()
    rentalcompanyform = RentalCompanyForm()
    globalform = GlobalForm()

    category_list = Category.objects.all()
    subcategory_list = SubCategory.objects.all()
    category_list_alt = Category.objects.prefetch_related('subcategory_set').all()
    subcategory_list_alt = SubCategory.objects.all()


    context = {
        'categoryform': categoryform,
        'subcategoryform': subcategoryform,
        'sectorform': sectorform,
        'subsectorform': subsectorform,
        'rentalcompanyform': rentalcompanyform,
        'globalform': globalform,
        'category_list': category_list,
        'subcategory_list': subcategory_list,
        'category_list_alt': category_list_alt,
        'subcategory_list_alt': subcategory_list_alt,
    }
    return render(request, 'preferences.html', context)

def filter_assets(request):
    assets = Asset.objects.all()

    name = request.GET.get('name')
    sector = request.GET.get('sector')
    subsector = request.GET.get('subsector')
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    rentalcompany = request.GET.get('rentalcompany')
    internalcode1 = request.GET.get('internalcode1')
    internalcode2 = request.GET.get('internalcode2')
    internalcode3 = request.GET.get('internalcode3')

    if name:
        assets = assets.filter(name__icontains=name)
    if sector:
        assets = assets.filter(sector__name__icontains=sector)
    if subsector:
        assets = assets.filter(subsector__name__icontains=subsector)
    if category:
        assets = assets.filter(category__name__icontains=category)
    if subcategory:
        assets = assets.filter(subcategory__name__icontains=subcategory)
    if rentalcompany:
        assets = assets.filter(rental_company__name__icontains=rentalcompany)
    if internalcode1:
        assets = assets.filter(internal_code1__icontains=internalcode1)
    if internalcode2:
        assets = assets.filter(internal_code2__icontains=internalcode2)
    if internalcode3:
        assets = assets.filter(internal_code3__icontains=internalcode3)

    context = {
        'assets': assets,
    }
    return render(request, 'filtered_assets.html', context)

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

def view_kit(request, id):
    kit = get_object_or_404(Kit, id=id)

    history_list = KitHistory.objects.filter(kit_id=kit).order_by('-modified')
    
    paginator = Paginator(history_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    asset_list = Asset.objects.all()
    sector_list = Sector.objects.all()
    subsector_list = SubSector.objects.all()
    sector_list_alt = Sector.objects.prefetch_related('subsector_set').all()
    subsector_list_alt = SubSector.objects.all()
    kit_list = Kit.objects.all()
    context = {
        'kit': kit,
        'asset_list': asset_list,
        'sector_list': sector_list,
        'subsector_list': subsector_list,
        'sector_list_alt': sector_list_alt,
        'subsector_list_alt': subsector_list_alt,
        'page_obj': page_obj,
        'kit_list': kit_list,
    }
    return render(request, 'view_kit.html', context)

def view_asset(request, id):
    # Recuperar o ativo existente
    asset = get_object_or_404(Asset, id=id)
    history_list = AssetHistory.objects.filter(asset_id=asset).order_by('-modified')
    
    paginator = Paginator(history_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
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
        
        return redirect('home')
    
    else:
        
        context = {
            'asset': asset,
            'page_obj': page_obj,
        }
        
        return render(request, 'view_asset.html', context)

def view_sector(request, id):
    sector = get_object_or_404(Sector, id=id)
    kits = sector.kit_set.all()  # Supondo que a relação entre Sector e Kit seja via `kit_set`
    assets = sector.asset_set.all()

    context = {
        'sector': sector,
        'kits': kits,
        'assets': assets,
    }
    return render(request, 'view_sector.html', context)

def view_subsector(request, id):
    subsector = get_object_or_404(SubSector, id=id)
    kits = subsector.kit_set.all()  # Supondo que a relação entre subSector e Kit seja via `kit_set`
    assets = subsector.asset_set.all()

    context = {
        'subsector': subsector,
        'kits': kits,
        'assets': assets,
    }
    return render(request, 'view_subsector.html', context)

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
    return render(request, 'view_asset_history.html', context)

# THE FOLLOWING VIEWS WILL HANDLE CRUD OPERATIONS
#=============================================================================================

# CATEGORIES ---------------------------------------------------------------------------------
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
            parent_category = subcategoryform.cleaned_data['parent']
            new_subcategory = SubCategory(name=subcategoryform.cleaned_data['Nova_SubCategoria'],parent=parent_category)
            new_subcategory.save()
            return HttpResponseRedirect("/preferences/")
    else:
        subcategoryform = SubCategoryForm()

# SECTOR -------------------------------------------------------------------------------------
def new_sector(request):
    if request.method == 'POST':
        sectorform = SectorForm(request.POST)
        if sectorform.is_valid():
            new_sector = Sector(name=sectorform.cleaned_data['Novo_Setor'])
            new_sector.save()            
            return JsonResponse({'success': True, 'sector': {'id': new_sector.id, 'name': new_sector.name}})
        else:
            return JsonResponse({'success': False, 'errors': sectorform.errors})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def delete_sector(request, id):
    sector = get_object_or_404(Sector, id=id)
    if request.method == 'POST':
        sector.delete() 
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


# SUBSECTOR --------------------------------------------------------------------------------------
def new_subsector(request):
    if request.method == 'POST':
        subsectorform = SubSectorForm(request.POST)
        if subsectorform.is_valid():
            parent_sector = subsectorform.cleaned_data['parent']
            new_subsector_name = subsectorform.cleaned_data['Novo_SubSetor']
            new_subsector = SubSector(name=new_subsector_name, parent=parent_sector)
            new_subsector.save()
            return JsonResponse({'success': True, 'subsector': {'id': new_subsector.id, 'name': new_subsector.name, 'parent_id': parent_sector.id}})
        else:
            return JsonResponse({'success': False, 'errors': subsectorform.errors})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def delete_subsector(request, id):
    subsector = get_object_or_404(SubSector, id=id)
    if request.method == 'POST':
        subsector.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

    
# KITS ---------------------------------------------------------------------------------------------
def new_kit(request):
    if request.method == 'POST':
        form = KitForm(request.POST)
        if form.is_valid():
            new_kit = form.save()
            selected_assets = form.cleaned_data['assets']
            
            # Atualizar setor e subsector dos assets selecionados
            for asset in selected_assets:
                asset.kit = new_kit
                asset.sector = new_kit.sectors
                asset.subsector = new_kit.subsectors
                asset.save()
            
            # Registrar histórico do kit
            KitHistory.objects.create(
                kit_id=new_kit,
                modification_type='Creation',
                user=request.user.username,
                name=new_kit.name,
                sector=new_kit.sectors.name if new_kit.sectors else '',
                subsector=new_kit.subsectors.name if new_kit.subsectors else '',
            )
            
            return redirect('home')
        else:
            return HttpResponse("Invalid form", status=400)
    else:
        return redirect('home')

def delete_kit(request, id):
    kit = get_object_or_404(Kit, id=id)
    if request.method == 'POST':
        kit.delete()
        return redirect('home')
    
def transfer_kit(request, id):
    kit = get_object_or_404(Kit, id=id)
    if request.method == 'POST':
        new_sector_id = request.POST.get('sector')
        new_subsector_id = request.POST.get('subsector')
        
        # Salvar o estado anterior do kit para registrar no histórico
        previous_sector = kit.sectors
        previous_subsector = kit.subsectors
        
        new_sector = None
        new_subsector = None

        if new_sector_id:
            new_sector = get_object_or_404(Sector, id=new_sector_id)
            kit.sectors = new_sector
            
        if new_subsector_id:
            new_subsector = get_object_or_404(SubSector, id=new_subsector_id)
            kit.subsectors = new_subsector
        else:
            kit.subsectors = None
            
        kit.save()

        for asset in kit.asset_set.all():
            previous_asset_sector = asset.sector
            previous_asset_subsector = asset.subsector
            asset.sector = new_sector
            if new_subsector_id:
                asset.subsector = new_subsector
            else:
                asset.subsector = None
            asset.save()

            # Criar registro no histórico do asset
            AssetHistory.objects.create(
                asset_id=asset,
                modification_type='Transfer',
                name=asset.name,
                category=asset.category.name if asset.category else '',
                modified=asset.modified,
                user=request.user.username,
                details=asset.details,
                sector=new_sector.name if new_sector else '',
                new_sector=new_sector.name if new_sector else '',
                previous_sector=previous_asset_sector.name if previous_asset_sector else '',
                subsector=new_subsector.name if new_subsector else '',
                new_subsector=new_subsector.name if new_subsector else '',
                previous_subsector=previous_asset_subsector.name if previous_asset_subsector else '',
                rental_company=asset.rental_company.name if asset.rental_company else '',
                internal_code1=asset.internal_code1,
                internal_code2=asset.internal_code2,
                internal_code3=asset.internal_code3,
                serial_number=asset.serial_number,
                brand=asset.brand,
                mac_address=asset.mac_address,
                windows_license=asset.windows_license,
                kit=kit.name
            )
        
        # Criar registro no histórico
        KitHistory.objects.create(
            kit_id=kit,
            modification_type='Transfer',
            name=kit.name,
            modified=kit.modified,
            user=request.user.username,
            sector=new_sector.name if new_sector else (previous_sector.name if previous_sector else ''),
            subsector=new_subsector.name if new_subsector else (previous_subsector.name if previous_subsector else ''),
            previous_sector=previous_sector.name if previous_sector else '',
            previous_subsector=previous_subsector.name if previous_subsector else '',
            new_sector=new_sector.name if new_sector else '',
            new_subsector=new_subsector.name if new_subsector else '',
        )
        
        return redirect('home')
    return redirect('home')

def edit_kit(request, id):
    kit = get_object_or_404(Kit, id=id)
    if request.method == 'POST':
        kit.name = request.POST.get('name')
        kit.save()
    KitHistory.objects.create(
        kit_id=kit,
        modification_type='Edit',
        user=request.user.username,
        modified=kit.modified
    )
    return redirect('home')

# RENTAL COMPANY ---------------------------------------------------------------------------------------
def new_rentalcompany(request):
    if request.method == 'POST':
        rentalcompanyform = RentalCompanyForm(request.POST)
        if rentalcompanyform.is_valid():
            new_rentalcompany = RentalCompany(name=rentalcompanyform.cleaned_data['Nova_Empresa'])
            new_rentalcompany.save()
            return HttpResponseRedirect("/preferences/")
    else:
        rentalcompanyform = RentalCompanyForm()

# ASSET ------------------------------------------------------------------------------------------------
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
            modification_type='Creation',
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

        return redirect('home')
    else:

        return render(request, 'new_asset.html')
    
def delete_asset(request, id):
    asset = get_object_or_404(Asset, id=id)
    if request.method == 'POST':
        asset.delete()
        return redirect('home')
    
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
            new_subsector = None
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
            windows_license=asset.windows_license,
            previous_sector=previous_sector,
            previous_subsector=previous_subsector,
            new_sector=new_sector,
            new_subsector=new_subsector,
        )
        
        return redirect('home')
    return redirect('home')

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
        
        return redirect('home')
    
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
  
# THE FOLLOWING VIEWS WILL HANDLE SOME GENERAL UTILITIES
#=============================================================================================

def get_sectors(request):
    sectors = Sector.objects.all()
    sector_list = [{'id': sector.id, 'name': sector.name} for sector in sectors]
    print(sector_list)
    return JsonResponse({'sectors': sector_list})

def get_subsectors(request, id):
    sector = get_object_or_404(Sector, id=id)
    subsectors = sector.subsector_set.all()
    subsector_list = [{'id': subsector.id, 'name': subsector.name} for subsector in subsectors]
    print(subsector_list)
    return JsonResponse({'subsectors': subsector_list})

def get_subsectors_by_parent(request):
    sector_id = request.GET.get('sector_id')
    subsectors = SubSector.objects.filter(parent_id=sector_id).values('id', 'name')
    return JsonResponse({'subsectors': list(subsectors)})

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(parent_id=category_id).values('id', 'name')
    return JsonResponse({'subcategories': list(subcategories)})
