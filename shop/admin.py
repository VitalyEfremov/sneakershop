from django.contrib import admin

from shop import models

admin.site.register(models.Order)
admin.site.register(models.Product)
admin.site.register(models.ProductsInOrder)
admin.site.register(models.ProductsInStock)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductCategory)
admin.site.register(models.ShippingType)
admin.site.register(models.PaymentType)
admin.site.register(models.OrderStatus)
