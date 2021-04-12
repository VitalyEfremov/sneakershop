from . import models
from datetime import datetime
from dateutil.relativedelta import relativedelta


class DBManager:
    @classmethod
    def get_products_for_main_page(cls, number_of_products):
        return models.Product.objects.filter(
            created_at__gte=datetime.now() - relativedelta(months=1)
        ).order_by('-created_at')[:number_of_products]

    @classmethod
    def get_all_products(cls):
        return models.Product.objects.all()
