from django import forms

from .models import Order


class MakeOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'receiver_first_name',
            'receiver_last_name',
            'phone',
            'shipping_type',
            'shipping_address',
            'payment_type',
            'datetime_shipping',
        ]
