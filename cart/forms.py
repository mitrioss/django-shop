from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(
        initial=1,  # Значение по умолчанию
        min_value=1,  # Минимум 1
        max_value=20,  # Максимум 20
        widget=forms.HiddenInput()  # Скрытое поле для передачи данных
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)