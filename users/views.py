from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from shop.models import Order, OrderStatus, ProductsInOrder, ProductInCardInfo, Product, CardSummary
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(
                request,
                f'Account successfully created for {username}! Now you are able to login.')

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register_page.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated successfully!')
            return redirect('user-profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


class UsersOrderListView(ListView, LoginRequiredMixin):
    model = Order
    template_name = 'user_orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(DetailView, LoginRequiredMixin):
    model = Order
    template_name = 'order_detail.html'

    products_in_order_info = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products_in_order = ProductsInOrder.objects.filter(order_id=self.object.id).prefetch_related()
        additional_context = []

        summary = CardSummary(
            items_count=0,
            total_price=0.0
        )

        for product_in_order in products_in_order:
            product_info = ProductInCardInfo(
                pk=product_in_order.product.pk,
                image_url=product_in_order.product.image.url,
                title=product_in_order.product.title,
                size=product_in_order.product.size,
                brand=product_in_order.product.brand,
                price=product_in_order.price,
                quantity=product_in_order.quantity,
                total=product_in_order.total_sum
            )

            summary.items_count += product_info.quantity
            summary.total_price += product_info.total

            additional_context.append(product_info)

        context['products_in_order'] = additional_context
        context['summary'] = summary

        return context


def cancel_order(request, pk):
    order = Order.objects.get(id=pk)
    if order.user == request.user:
        cancel_status_id = OrderStatus.objects.get(title='Canceled').id
        order.status_id = cancel_status_id
        order.save()
    else:
        messages.error(request, message='You are not allowed to cancel this order')

    return redirect('user-orders')
