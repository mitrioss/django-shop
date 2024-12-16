# forms.py
from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        initial=1,  # Значение по умолчанию
        widget=forms.Select(attrs={'class': 'form-control'})  # Добавляем класс для стилизации
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
