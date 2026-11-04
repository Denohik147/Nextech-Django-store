from django.contrib import admin 
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop.views import (
    home,
    category_detail, 
    catalog, 
    product_detail,
    toggle_favorite,
    toggle_comparison,
    favorites,
    comparison,  
    add_to_cart, 
    cart, 
    remove_from_cart, 
    update_cart, 
    register, 
    user_login, 
    user_logout,
    profile,
    checkout,
)    


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('catalog/', catalog, name='catalog'),

    path('product/<int:product_id>/', product_detail, name='product_detail'),

    path(
        'favorite/<int:product_id>/',
        toggle_favorite,
        name='toggle_favorite'
    ),

    path(
        'comparison/<int:product_id>/',
        toggle_comparison,
        name='toggle_comparison'
    ),

    path(
        'favorites/',
        favorites,
        name='favorites'
    ),

    path(
        'comparison/',
        comparison,
        name='comparison'
    ),

    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', update_cart, name='update_cart'),
    path('cart/', cart, name='cart'),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('profile/', profile, name='profile'),

    path('checkout/', checkout, name='checkout'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),

    path('api/', include('api.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT
)