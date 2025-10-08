from django.forms import ModelForm
from main.models import Products
from django import forms
from django.utils.html import strip_tags
class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields = ["name", "price", "description", "stock", "thumbnail", "category", "is_featured"]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Enter product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:ring-indigo-500 focus:border-indigo-500',
                'rows': 3,
                'placeholder': 'Enter product description'
            }),
            'category': forms.Select(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'e.g., 150000'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'e.g., 10'
            }),
            'thumbnail': forms.URLInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'https://example.com/image.jpg'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500'
            }),
        }
        
    def clean_name(self):
        # Ambil data dari field 'name'
        data = self.cleaned_data['name']
        # Bersihkan dari tag HTML dan kembalikan
        return strip_tags(data)

    def clean_description(self):
        data = self.cleaned_data['description']
        return strip_tags(data)
        
        
# class SellerForm(ModelForm):
#     #Nama, tanggal lahir, email, no telp, link socmed, password
    
#     class Meta:
#         model = Seller
#         fields = ["nama", "tanggal_lahir", "email", "no_telp", "sosmed", "password"]