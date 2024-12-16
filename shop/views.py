from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from .models import Customer, Category, Product
from cart.forms import CartAddProductForm
from orders.models import Order
from .forms import ReviewForm



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
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'product/list.html', {'category': category,
                                        'categories': categories,
                                        'products': products})

class HomePageView(TemplateView):
    template_name = 'index.html'


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
