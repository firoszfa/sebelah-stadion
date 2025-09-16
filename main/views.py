from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from main.models import Products
from main.forms import ProductForm

# Create your views here.
def show_main(request):
    products_list = Products.objects.all()
    
    context = {
        'app_name': 'Sebelah Stadion',
        'npm': 2406412972,          # ganti dengan NPM-mu
        'name': 'Firos Aqiela Zufa',   # ganti dengan namamu
        'class': 'PBP F',        # ganti dengan kelasmu
        'products_list': products_list,
    }
    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

def show_product(request, id):
    product = get_object_or_404(Products, pk=id)

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

def show_xml(request):
     product_list = Products.objects.all()
     xml_data = serializers.serialize("xml", product_list)
     return HttpResponse(xml_data, content_type="application/xml")
 
def show_json(request):
    product_list = Products.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, product_id):
    try:
        product_item = Products.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Products.DoesNotExist:
        return HttpResponse(status=404)
   

def show_json_by_id(request, product_id):
    try:
        product_item = Products.objects.get(pk=product_id)
        json_data = serializers.serialize("json", [product_item])
        return HttpResponse(json_data, content_type="application/json")
    except Products.DoesNotExist:
        return HttpResponse(status=404)