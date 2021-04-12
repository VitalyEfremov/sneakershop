from django.urls import path
from shop import views


urlpatterns = [
    path('', views.main_page, name='shop-main'),
    path('catalog/', views.ProductListView.as_view(), name='catalog'),
    path('product/<int:pk>/detail/', views.ProductDetailView.as_view(), name='product-detail'),
    path('card/', views.card_page, name='card-page'),
    path('product/add/<int:pk>', views.add_product_to_card, name='add-to-card'),
    path('card/decrease/<int:pk>', views.decrease_product_quantity, name='decrease_q'),
    path('card/increase/<int:pk>', views.increase_product_quantity, name='increase_q'),
    path('card/delete/<int:pk>', views.delete_product_from_card, name='delete_product_from_card'),
    path('make_order/', views.order_page, name='order_page'),
]
