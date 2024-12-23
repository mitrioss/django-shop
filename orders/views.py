from django.core.checks import messages
from django.urls import reverse
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.shortcuts import render, redirect


def order_create(request):
    cart = Cart(request)

    if not cart:  # Проверка, если корзина пуста
        messages.Error(request, "Ваша корзина пуста")
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистить корзину
            cart.clear()
            # запустить асинхронное задание
            order_created.delay(order.id)
            # задать заказ в сеансе
            request.session['order_id'] = order.id
            # перенаправить к платежу
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreateForm()
    return render(request,
                  'order/create.html',
                  {'cart': cart, 'form': form})
