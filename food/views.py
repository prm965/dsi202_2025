from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Restaurant, MenuItem, CartItem

def home(request):
    query = request.GET.get("q", "")
    if query:
        menu_items = MenuItem.objects.filter(name__icontains=query)
    else:
        menu_items = MenuItem.objects.all()
    return render(request, "food/home.html", {"menu_items": menu_items})

def menu_detail(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    return render(request, "food/menu_detail.html", {"menu_item": menu_item})

def add_to_cart(request, item_id):
    if request.method == 'POST':
        menu_item = get_object_or_404(MenuItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # สมมุติคุณใช้ session cart
        cart = request.session.get('cart', {})
        cart[str(item_id)] = cart.get(str(item_id), 0) + quantity
        request.session['cart'] = cart

        return redirect('home')

@login_required
def add_to_cart(request, menu_item_id):
    item = get_object_or_404(MenuItem, id=menu_item_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, menu_item=item)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect(request.META.get('HTTP_REFERER'))  # หรือ 'view_cart'

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)
    return render(request, 'food/view_cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def remove_from_cart(request, cart_item_id):
    item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    item.delete()
    return redirect('view_cart')

@login_required
def decrease_quantity(request, cart_item_id):
    item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('view_cart')
