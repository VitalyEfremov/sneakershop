from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register-user'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'password-reset-confirm/<uidb64>/<token>',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'
    ),
    path('profile/', views.profile, name='user-profile'),

    path(
        'orders/',
        views.UsersOrderListView.as_view(template_name='user_orders.html'),
        name='user-orders'
    ),
    path(
        'order_details/<int:pk>',
        views.OrderDetailView.as_view(template_name='order_detail.html'),
        name='order-detail'
    ),
    path('cancel_order/<int:pk>', views.cancel_order, name='cancel-order'),
]
