from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import ProductForm
from .models import Product
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .services.products import get_products_by_category
from .models import Category
from django.core.cache import cache


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 10


class ContactView(TemplateView):
    template_name = 'catalog/contact.html'


@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm  # <-- Используем форму с валидацией
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        product = form.instance

        # Очищаем кеш для категории этого товара
        if product.category_id:
            cache_key = f"category_products:{product.category_id}"
            cache.delete(cache_key)

        return response

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.has_perm('catalog.can_unpublish_product'):
            return redirect('catalog:product_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.has_perm('catalog.can_unpublish_product'):
            return redirect('catalog:product_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)


@permission_required('catalog.can_unpublish_product', raise_exception=True)
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_published = False
    product.save()
    return redirect('catalog:product_detail', pk=product.pk)


def products_by_category(request, category_slug):
    # Сначала получаем объект категории (это обязательно, чтобы получить id)
    category = get_object_or_404(Category, slug=category_slug)

    # Формируем уникальный ключ кеша на основе ID категории
    cache_key = f"category_products:{category.id}"

    # Пытаемся получить данные из кеша
    products = cache.get(cache_key)

    if products is None:
        # Если в кеше нет — запрашиваем через сервис (он вернёт queryset)
        products = get_products_by_category(category_slug=category_slug)

        # Превращаем queryset в список, чтобы безопасно хранить в кеше
        # (некоторые бэкенды кэша плохо работают с живыми queryset)
        products_list = list(products)

        # Сохраняем в кеш: ключ, значение, TTL (например, 15 минут = 900 секунд)
        ttl = 60 * 15
        cache.set(cache_key, products_list, timeout=ttl)

        # Возвращаем список
        products = products_list

    context = {
        "category": category,
        "products": products,
    }
    return render(request, "catalog/products_by_category.html", context)
