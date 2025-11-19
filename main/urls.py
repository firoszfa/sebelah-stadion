from django.urls import path
from main.views import show_main, create_product, add_product_ajax, update_product_ajax, show_product, delete_product, edit_product, show_xml, show_json, show_json_by_user, show_xml_by_id, show_json_by_id, register,login_user, logout_user, login_ajax, register_ajax, logout_ajax, proxy_image, create_product_flutter
#from main.views import  create_seller

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product/', create_product, name='create_product'),
    path('product/<uuid:id>/', show_product, name='show_product'),
    path('product/<uuid:id>/edit/', edit_product, name='edit_product'),
    path('product/<uuid:id>/delete/', delete_product, name='delete_product'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<uuid:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<uuid:id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('add-product-ajax/', add_product_ajax, name='add_product_ajax'),
    path('update-product-ajax/<uuid:product_id>/', update_product_ajax, name='update_product_ajax'),
    path('api/login/', login_ajax, name='login_ajax'),
    path('api/register/',register_ajax, name='register_ajax'),
    path('api/logout/', logout_ajax, name='logout_ajax'),
    path('proxy-image/', proxy_image, name='proxy_image'),
    path('create-flutter/', create_product_flutter, name='create_product_flutter'),
    path('json-by-user/', show_json_by_user, name='show_json_by_user'),
    #path('create-seller/', create_seller, name='create_seller')
]