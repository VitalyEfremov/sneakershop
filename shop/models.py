from dataclasses import dataclass

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


@dataclass
class ProductInCardInfo:
    pk: int
    image_url: str
    title: str
    size: float
    brand: str
    price: float
    quantity: int
    total: float


@dataclass
class CardSummary:
    items_count: int
    total_price: float


class ProductCategory(models.Model):
    title = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title',)


class ProductBrand(models.Model):
    title = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title',)


class Product(models.Model):
    title = models.CharField(max_length=50, null=False)
    price = models.FloatField(max_length=50, null=False)
    brand = models.ForeignKey(
        ProductBrand,
        on_delete=models.DO_NOTHING
    )
    description = models.TextField(max_length=2048)
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.DO_NOTHING
    )
    image = models.ImageField(default='products/thumbnails/default_thumbnail.png', upload_to='products/thumbnails')
    created_at = models.DateTimeField(auto_now_add=True)
    size = models.FloatField(
        choices=(
            (38.0, 38.0),
            (38.5, 38.5),
            (39.0, 39.0),
            (39.5, 39.5),
            (40.0, 40.0),
            (40.5, 40.5),
            (41.0, 41.0),
            (41.5, 41.5),
            (42.0, 42.0),
            (42.5, 42.5),
            (43.0, 43.0),
            (43.5, 43.5),
            (44.0, 44.0),
            (44.5, 44.5),
        ),
        default=41.5
    )

    def __str__(self):
        return f'{self.brand} {self.title} {self.size}'

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ('title', 'brand',)


class ProductsInStock(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING
    )
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.product.title} {self.quantity}'


class ShippingType(models.Model):
    title = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title',)


class PaymentType(models.Model):
    title = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title',)


class OrderStatus(models.Model):
    title = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )

    phone = PhoneNumberField()
    receiver_first_name = models.CharField(max_length=50, verbose_name='First name')
    receiver_last_name = models.CharField(max_length=50, verbose_name='Last name')

    datetime_posted = models.DateTimeField(auto_now_add=True)

    shipping_type = models.ForeignKey(
        ShippingType,
        on_delete=models.DO_NOTHING,
        verbose_name="Order shipping type",
    )

    shipping_address = models.CharField(max_length=255)
    datetime_shipping = models.DateTimeField(verbose_name='Date of delivery', default=timezone.now)
    post_code = models.CharField(max_length=6, verbose_name='Post code')

    payment_type = models.ForeignKey(
        PaymentType,
        on_delete=models.DO_NOTHING,
        verbose_name='Order payment type',
    )

    total_sum = models.FloatField(verbose_name='Order total sum')

    status = models.ForeignKey(
        OrderStatus,
        on_delete=models.DO_NOTHING,
        verbose_name='Order status'
    )

    def __str__(self):
        return (
            f'Order by {self.user.username}, '
            f'delivery on {self.datetime_shipping}, '
            f'made on {self.datetime_posted}, '
            f'status {self.status}'
        )


class ProductsInOrder(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='order'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        null=False,
        verbose_name='product'
    )
    quantity = models.IntegerField(null=False)
    price = models.FloatField(verbose_name='Price for 1 item')
    total_sum = models.FloatField(verbose_name='Total sum for product')

    class Meta:
        unique_together = ('order', 'product')
