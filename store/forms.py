from django import forms
from .models import Product,ProductImage,Variation

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','category','description', 'slug','price', 'stock','image']

class AdditionalImageForm(forms.ModelForm):
    class Meta:
        model=ProductImage
        fields=['addimage']

class VariantForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ['variation_category','variation_value','product','stock','image']
