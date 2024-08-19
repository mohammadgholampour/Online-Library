# library/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, Cart, CartItem, Order
from .forms import AddToCartForm
from django.utils import timezone

def index(request):
    books = Book.objects.all()
    return render(request, 'library/index.html', {'books': books})

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    form = AddToCartForm()
    return render(request, 'library/book_detail.html', {'book': book, 'form': form})

@login_required
def add_to_cart(request, id):
    book = get_object_or_404(Book, id=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
            cart_item.quantity += form.cleaned_data['quantity']
            cart_item.save()
            return redirect('cart_detail')
    return redirect('book_detail', id=id)

@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'library/cart_detail.html', {'cart_items': cart_items})

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    
    order = Order.objects.create(user=request.user, total_price=total_price, created_at=timezone.now())
    order.items.set(cart_items)
    order.save()
    
    cart_items.delete()
    
    return render(request, 'library/checkout.html', {'order': order})
