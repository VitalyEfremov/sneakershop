from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView

from sneakershop.settings import SESSION_EXPIRY_VALUE
from .db_manager import DBManager
from .forms import MakeOrderForm
from .models import (
    Product,
    ProductInCardInfo,
    CardSummary,
    Order,
    ProductsInOrder
)


def main_page(request: HttpRequest) -> HttpResponse:
    context = {
        'products': DBManager.get_products_for_main_page(number_of_products=3),
        'main_page_banner': '/media/common/main_page_banner.jpg'
    }
    return render(request, 'main_page.html', context)


@login_required
def card_page(request):
    context = {
        'products_in_card': []
    }
    summary = CardSummary(
        items_count=0,
        total_price=0.0
    )

    for product_id in request.session.get('products_in_card', {}).keys():
        try:
            product = Product.objects.get(id=product_id)

            quantity = request.session.get('products_in_card').get(product_id)
            product_info = ProductInCardInfo(
                pk=product.pk,
                image_url=product.image.url,
                title=product.title,
                size=product.size,
                brand=product.brand,
                price=product.price,
                quantity=quantity,
                total=quantity*product.price
            )

            summary.items_count += quantity
            summary.total_price += product_info.total

            context['products_in_card'].append(product_info)
        except KeyError:
            messages.error(request, f'Product with id {product_id} was not found')
    context['summary'] = summary

    return render(request, 'card.html', context)


@login_required
def add_product_to_card(request, pk):
    product_available = Product.objects.filter(id=pk).exists()
    product_key = str(pk)

    if not product_available:
        return HttpResponseNotFound(f'Product with id {pk} does not exist')

    if not request.session.get('products_in_card'):
        request.session['products_in_card'] = {}

    if not request.session['products_in_card'].get(product_key):
        request.session['products_in_card'][product_key] = 1
    else:
        request.session['products_in_card'][product_key] += 1

    request.session.set_expiry(SESSION_EXPIRY_VALUE)

    messages.success(request, f'Product has been added to card successfully!')
    return redirect('product-detail', pk)


@login_required
def delete_product_from_card(request, pk):
    product_available = Product.objects.filter(id=pk).exists()
    product_key = str(pk)

    if not product_available:
        return HttpResponseNotFound(f'Product with id {pk} does not exist')

    try:
        request.session['products_in_card'].pop(product_key)
    except KeyError:
        pass

    request.session.set_expiry(SESSION_EXPIRY_VALUE)

    return redirect('card-page')


@login_required
def increase_product_quantity(request, pk):
    product_available = Product.objects.filter(id=pk).exists()
    product_key = str(pk)

    if not product_available:
        return HttpResponseNotFound(f'Product with id {pk} does not exist')

    if not request.session.get('products_in_card'):
        request.session['products_in_card'] = {}
        return redirect('card-page')

    if not request.session['products_in_card'].get(product_key):
        return redirect('card-page')
    else:
        request.session['products_in_card'][product_key] += 1

    request.session.set_expiry(SESSION_EXPIRY_VALUE)

    return redirect('card-page')


@login_required
def decrease_product_quantity(request, pk):
    product_available = Product.objects.filter(id=pk).exists()
    product_key = str(pk)

    if not product_available:
        return HttpResponseNotFound(f'Product with id {pk} does not exist')

    if not request.session.get('products_in_card'):
        request.session['products_in_card'] = {}
        return redirect('card-page')

    if request.session['products_in_card'].get(product_key):
        if request.session['products_in_card'][product_key] != 1:
            request.session['products_in_card'][product_key] -= 1
        else:
            request.session['products_in_card'].pop(product_key)

        request.session.set_expiry(SESSION_EXPIRY_VALUE)

    return redirect('card-page')


@login_required
def order_page(request, order=Order()):
    total = 0
    for product_id in request.session.get('products_in_card', {}).keys():
        product = Product.objects.get(id=product_id)

        quantity = request.session.get('products_in_card').get(product_id)
        total += product.price * quantity

    if request.method == 'POST':
        order_form = MakeOrderForm(data=request.POST, instance=order)

        if order_form.is_valid():
            order_to_save = order_form.save(commit=False)
            order_to_save.user_id = request.user.pk
            order_to_save.total_sum = total
            order_to_save.status_id = int(request.POST['status_id'])
            order_to_save.save()

            for product_id in request.session.get('products_in_card'):
                quantity = request.session.get('products_in_card').get(product_id)
                product = Product.objects.get(id=product_id)

                ordered_product = ProductInCardInfo(
                    pk=product.pk,
                    image_url=product.image.url,
                    title=product.title,
                    size=product.size,
                    brand=product.brand,
                    price=product.price,
                    quantity=quantity,
                    total=quantity * product.price
                )

                product_in_order = ProductsInOrder(
                    order=order_to_save,
                    product=product,
                    quantity=ordered_product.quantity,
                    price=ordered_product.price,
                    total_sum=ordered_product.total
                )
                product_in_order.save()

            messages.success(request, f'Your order has been made successfully! Wait tail manager confirm it.')
            return redirect('user-orders')
    else:
        order_form = MakeOrderForm(data=request.POST, instance=order)

        context = {
            'order_form': order_form,
            'order_total': total
        }

        return render(request, 'make_order.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'


class ProductListView(ListView):
    model = Product
    template_name = 'catalog.html'
    context_object_name = 'products'
    ordering = ['-created_at']
    paginate_by = 6
