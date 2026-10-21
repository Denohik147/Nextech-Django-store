from .models import Category
from .models import Favorite, Comparison

def categories(request):
    return {
        'categories': Category.objects.all()
    }

def navbar_counts(request):
    favorite_count = 0 
    comparison_count = 0 
    cart_count = 0 

    if request.user.is_authenticated:
        favorite_count = Favorite.objects.filter(
            user=request.user
        ).count()

        comparison_count = Comparison.objects.filter(
            user=request.user
        ).count()

    cart = request.session.get('cart', {})

    cart_count = sum(cart.values())

    return {
        'favorite_count': favorite_count,
        'comparison_count': comparison_count,
        'cart_count': cart_count,
    }    