from django import forms
from .models import Category, Mark, Store, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ('name',)

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ('name', 'wilaya', 'address', 'image')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'available', 'mark', 'image')


# form to add cart element

QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 101)]

class AddCartElementForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=QUANTITY_CHOICES, coerce=int)

