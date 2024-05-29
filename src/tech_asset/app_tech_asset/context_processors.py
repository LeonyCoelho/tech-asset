from .models import GlobalSettings, Category, SubCategory, Sector, SubSector, RentalCompany

def global_settings(request):
    try:
        settings = GlobalSettings.objects.get(id=1)
    except GlobalSettings.DoesNotExist:
        settings = None
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    sectors = Sector.objects.all()
    subsectors = SubSector.objects.all()
    rental_companies = RentalCompany.objects.all()
    return {
        'global_settings': settings,
        'categories': categories,
        'subcategories': subcategories,
        'sectors': sectors,
        'subsectors': subsectors,
        'rental_companies': rental_companies
        }
