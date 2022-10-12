from django.shortcuts import get_object_or_404, render

from cart.models import CartItem
from category.models import Category
from .models import Product
from cart.views import _cart_id

def store(request, category_slug=None):
    # Agar kategory slug bo'sh bo'lsa
    if category_slug == None:
        # Faqat sotuvda bo'lgan ma'lumotlar filteri
        products = Product.objects.filter(is_available=True)
    else:
        # Noto'g'ri ma'lumot kiritlsa yani ("slug") 404 xatolik beradi
        categories = get_object_or_404(Category, slug=category_slug)

        # Bu kategory ga tegishli bo'lgan hamma mahsulotni chiqarib beradi
        products = Product.objects.filter(is_available=True, category=categories)

    context = {
        'products': products,
        # Product sonini berivormiz
        'product_count': products.count()
    }
    return render(request, 'store.html', context)




def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
    cart_in = CartItem.objects.filter(cart__session_id=_cart_id(request)).exists()
    context = {
        'product': product,
        'cart_in': cart_in
    }
    return render(request, 'product_detail.html', context)