from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from .models import (
    Product, 
    Category, 
    Order, 
    OrderItem, 
    Favorite, 
    Comparison,
    ProductParameter,
)

from .forms import RegistrationForm, LoginForm


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')

    if category_id:
        products = products.filter(category_id=category_id)

    search = request.GET.get('search')

    if search:
        products = products.filter(name__icontains=search)

    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories,
    })


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    categories = Category.objects.all()
    products = Product.objects.filter(category=category)

    search = request.GET.get('search')

    if search:
        products = products.filter(name_icontains=search)

    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories,
        'selected_category': category,
    })     
   

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegistrationForm()

    return render(request, 'shop/register.html', {'form': form})    


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.filter(
                email__iexact=email
            ).first()

            if user is not None:
                authenticated_user = authenticate(
                    username=user.username,
                    password=password
                )

                if authenticated_user is not None:
                    login(request, authenticated_user)
                    return redirect('home')

            form.add_error(
                None,
                'Неверный email или пароль'
            )

    else:
        form = LoginForm()

    return render(request, 'shop/login.html', {'form': form})                        


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    for order in orders:
        total = 0

        for item in order.items.all():
            total += item.price * item.quantity

        order.total = total     
    
    return render(request, 'shop/profile.html', {
        'orders': orders,
    })


def catalog(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    search = request.GET.get('search')

    if category_id:
        products = products.filter(category_id=category_id)

    if search:
        products = products.filter(name__icontains=search)    

    return render(request, 'shop/catalog.html', {
        'products': products,
        'categories': categories,
    })


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    categories = Category.objects.all()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'categories': categories,
    })


@login_required
def toggle_favorite(request, product_id):
    product = Product.objects.get(id=product_id)

    favorite = Favorite.objects.filter(
        user=request.user,
        product=product 
    ).first()

    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(
            user=request.user,
            product=product
        )

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def toggle_comparison(request, product_id):
    product = Product.objects.get(id=product_id)

    comparison = Comparison.objects.filter(
        user=request.user,
        product=product
    ).first()

    if comparison:
        comparison.delete()
    else:
        Comparison.objects.create(
            user=request.user,
            product=product
        )    
    return redirect(request.META.get('HTTP_REFERER', 'home'))
     

@login_required
def favorites(request):
    favorite_products = Favorite.objects.filter(
        user=request.user
    ).select_related('product')

    return render(request, 'shop/favorites.html', {
        'favorite_products': favorite_products, 
    })


@login_required
def comparison(request):
    comparison_products = Comparison.objects.filter(
        user=request.user
    ).select_related('product')

    return render(request, 'shop/comparison.html', {
        'comparison_products': comparison_products,
    })


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart = request.session.get('cart', {})

    product_id = str(product_id)

    current_quantity = cart.get(product_id, 0)

    if current_quantity < product.stock:
        cart[product_id] = current_quantity + 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})

    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)

        item_total = product.price * quantity
        total += item_total

        products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

    return render(request, 'shop/cart.html', {
        'products': products,
        'total': total,
    })    


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart 
    request.session.modified = True

    return redirect('cart')


def update_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        product = Product.objects.get(id=product_id)

        quantity = int(request.POST.get('quantity', 1))

        if quantity > product.stock:
            quantity = product.stock

        if quantity > 0: 
            cart[product_id] = quantity
        else:
            del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    order = Order.objects.create(
        user=request.user
    )

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)

        if quantity > product.stock:
            quantity = product.stock

        if quantity > 0:    
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            product.stock -= quantity
            product.save()

    request.session['cart'] = {}
    request.session.modified = True

    return redirect('profile')    