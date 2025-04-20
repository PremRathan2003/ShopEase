from django import forms

from django.contrib.auth import get_user_model

from .models import Product

User = get_user_model()

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'unit_price', 'seller','image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter unit price'}),
            'seller': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter The name of the seller'}),
            'image': forms.FileInput(),
        }
        def __init__(self, *args, **kwargs):
            super(ProductForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
            self.fields['image'].widget.attrs['class'] = 'form-control'  # for file input