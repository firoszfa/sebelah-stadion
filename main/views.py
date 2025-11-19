import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from main.models import Products
from django.contrib.auth.forms import UserCreationForm, UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core import serializers
from main.models import Products
from main.forms import ProductForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
import requests
import json

#flutter
def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    
@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        try:
            # 1. Parse Data
            data = json.loads(request.body)
            
            # 2. Validasi User (PENTING)
            # Jika user belum login di Flutter, request.user adalah AnonymousUser
            # Ini akan menyebabkan error saat save()
            if not request.user.is_authenticated:
                return JsonResponse({"status": "error", "message": "User not authenticated"}, status=401)

            # 3. Ambil Data
            title = strip_tags(data.get("title", ""))
            content = strip_tags(data.get("content", ""))
            category = strip_tags(data.get("category", ""))
            thumbnail = data.get("thumbnail", "")
            is_featured = data.get("is_featured", False)
            
            try:
                price = int(data.get("price", 0))
            except ValueError:
                price = 0

            try:
                stock = int(data.get("stock", 0))
            except ValueError:
                stock = 0
            
            user = request.user

            # 4. Simpan ke Database
            # PERHATIKAN: Gunakan nama Class yang benar (ProductEntry atau Product)
            new_product = Products( 
                name=title,
                description=content,
                category=category,
                thumbnail=thumbnail,
                price=price,
                stock=stock,
                is_featured=is_featured,
                user=user
            )
            new_product.save()

            return JsonResponse({"status": "success"}, status=200)
            
        except Exception as e:
            # 5. Print error ke Terminal agar terlihat penyebabnya
            print(f"ERROR create_product_flutter: {e}") 
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
            
    else:
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=401)

# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        products_list = Products.objects.all()
    else:
        products_list = Products.objects.filter(user=request.user)
    
    context = {
        'app_name': 'Sebelah Stadion',
        'npm': 2406412972,          # ganti dengan NPM-mu
        'name': 'Firos Aqiela Zufa',   # ganti dengan namamu
        'class': 'PBP F',        # ganti dengan kelasmu
        'logged_name': request.user.username,
        'products_list': products_list,
        'last_login': request.COOKIES.get('last_login', 'Never'),
        'filter_type': filter_type,
    }
    return render(request, "main.html", context)

@login_required(login_url='/login')
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

# def create_seller(request):
#     form = SellerForm(request.Post or None)
    
#     if form.is_valid() and request.method == "POST":
#         form.save()
#         return redirect('main:show_main')
    
#     context = {'form': form}
#     return render(request, "create_seller.html", context)
    

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Products, pk=id)

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

@login_required(login_url='/login')
def edit_product(request, id):
    product = get_object_or_404(Products, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

@login_required(login_url='/login')
def delete_product(request, id):
    try:
        product = get_object_or_404(Products, pk=id)
    except:
        return JsonResponse({'status': 'error', 'message': 'Product not found.'}, status=404)

    if request.method == 'POST':
        if product.user != request.user:
            return JsonResponse({'status': 'error', 'message': 'You are not authorized to delete this product.'}, status=403)
        
        product.delete()
        return JsonResponse({'status': 'success', 'message': 'Product deleted successfully!'}, status=200)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@csrf_exempt
@require_POST
def add_product_ajax(request):
    form = ProductForm(request.POST)

    if form.is_valid():
        product = form.save(commit=False)
        product.user = request.user
        product.save() 
        
        return JsonResponse({'status': 'success'}, status=201)
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        
@require_POST
def update_product_ajax(request, product_id):
    try:
        product = Products.objects.get(pk=product_id)
    except Products.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

    form = ProductForm(request.POST, instance=product)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

def show_xml(request):
     product_list = Products.objects.all()
     xml_data = serializers.serialize("xml", product_list)
     return HttpResponse(xml_data, content_type="application/xml")
 

def show_json(request):
    product_list = Products.objects.all()
    data = [
        {
            'id': str(product.id),
            'title': product.name,
            'content': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'price': product.price,
            'stock': product.stock,
            'is_featured': product.is_featured,
            'user_id': product.user_id,
            'user_username': product.user.username,
        }
        for product in product_list
    ]

    return JsonResponse(data, safe=False)

@login_required
def show_json_by_user(request):
    # Filter: Hanya ambil produk milik user yang sedang login
    product_list = Products.objects.filter(user=request.user)
    
    # Kita gunakan struktur data yang SAMA PERSIS dengan show_json
    data = [
        {
            'id': str(product.id),
            'title': product.name,
            'content': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'price': product.price,
            'stock': product.stock,
            'is_featured': product.is_featured,
            'user_id': product.user_id,
            'user_username': product.user.username,
        }
        for product in product_list
    ]

    return JsonResponse(data, safe=False)


def show_xml_by_id(request, id):
    try:
        product_item = Products.objects.filter(pk=id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Products.DoesNotExist:
        return HttpResponse(status=404)
   

def show_json_by_id(request, id):
    try:
        product = Products.objects.select_related('user').get(pk=id)

        data = {
            'id': str(product.id),
            'title': product.name,
            'content': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'price': product.price,
            'stock': product.stock,
            'is_featured': product.is_featured,
            'user_id': product.user_id,
            'user_username': product.user.username if product.user_id else None,
        }
        return JsonResponse(data)

    except Products.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@require_POST
def logout_ajax(request):
    logout(request)
    return JsonResponse({
        'status': 'success', 
        'message': 'You have been logged out.'
    })

@require_POST
def login_ajax(request):
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Login successful!'})
    
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

@require_POST
def register_ajax(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return JsonResponse({'status': 'success', 'message': 'Registration successful!'}, status=201)
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)