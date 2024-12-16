from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count
from django.views import View
from django.views.generic import TemplateView, ListView
from .models import Customer, Category, Product
from cart.forms import CartAddProductForm
from orders.models import Order
from .forms import ReviewForm
from django.db.models import Avg
from django.db.models.functions import Coalesce
from django.db import models



def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    reviews = product.reviews.all()
    review_form = ReviewForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                return redirect('shop:product_detail', id=product.id, slug=product.slug)
        else:
            return redirect('login')

    cart_product_form = CartAddProductForm()

    return render(request, 'product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'reviews': reviews,
        'review_form': review_form
    })

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    # Сортировка
    sort_by = request.GET.get('sort', 'name')  # по умолчанию сортируем по имени (A-Z)

    if sort_by == 'name':
        products = products.order_by('name')  # Сортировка от A до Я
    elif sort_by == 'rating':
        products = products.order_by('-rating')  # Сортировка по оценке (в убывающем порядке)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)

        # Получаем все категории (включая подкатегории) для выбранной категории
        all_categories = Category.objects.filter(parent=category) | Category.objects.filter(id=category.id)

        # Фильтруем товары по категориям
        products = products.filter(category__in=all_categories)

    return render(request,
                  'product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        # Получаем продукты с аннотированным средним рейтингом и количеством отзывов
        products = Product.objects.annotate(
            average_rating=Coalesce(Avg('reviews__rating'), 0, output_field=models.FloatField()),
            review_count=Count('reviews')
        ).filter(average_rating__gt=0)  # Фильтруем только те продукты, у которых есть рейтинг

        # Сортируем по среднему рейтингу и выбираем топ-3
        top_products = products.order_by('-average_rating')[:3]

        return render(request, 'index.html', {'products': top_products})


class CustomersListView(ListView):
    template_name = "customer.html"
    model = Customer
    context_object_name = "list_of_all_customers"


class OrdersListView(ListView):
    template_name = "orders.html"
    model = Order
    context_object_name = "list_of_all_orders"

    def get_queryset(self):
        return Order.objects.all()


class SearchView(ListView):
    template_name = "search.html"
    model = Order
    context_object_name = "list_of_all_orders"

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Order.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).order_by('-created')
