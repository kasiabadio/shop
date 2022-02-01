from .models import Kategoria, Produkt

def add_to_context(request):
    
    super_categories = Kategoria.objects.all().filter(id_nadkategorii=None)
        
    # create dictionary where we store subcategories     
    super_categories_dict = {}
    for category in super_categories:
        
        sub_categories = Kategoria.objects.all().filter(id_nadkategorii=category.id_kategorii)
        super_categories_dict[category] = sub_categories
        
    return {
            'products': Produkt.objects.all(), 
            'super_categories_dict': super_categories_dict,    
    }