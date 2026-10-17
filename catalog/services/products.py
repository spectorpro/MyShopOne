from ..models import Product

def get_products_by_category(category_id=None, category_slug=None):
    """
    Возвращает queryset продуктов для указанной категории.
    Можно передавать либо id, либо slug категории.
    """
    qs = Product.objects.all()
    if category_id:
        qs = qs.filter(category_id=category_id)
    elif category_slug:
        qs = qs.filter(category__slug=category_slug)
    return qs